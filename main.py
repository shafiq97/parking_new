import json
import time
from collections import OrderedDict
import cv2
import requests
import mysql.connector
from datetime import datetime

API_TOKEN = '46569c6bbf83ec3257068d20a74113e420598687'

# Database connection setup
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'parking_db'
}

# Track detected plates
detected_plates = {}

def perform_ocr(image):
    _, image_encoded = cv2.imencode('.jpg', image)
    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        files=dict(upload=image_encoded.tobytes()),
        data=dict(regions='fr'),  # Adjust the regions as needed
        headers={'Authorization': 'Token ' + API_TOKEN}
    )
    
    result = response.json(object_pairs_hook=OrderedDict)
    if result['results']:
        num = result['results'][0]['plate']
        characters = result['results'][0]['candidates'][0]['plate']
        return num, characters
    return 'Unknown', 'Unknown'

def store_or_update_record(plate_number, extracted_characters):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    check_in_time = datetime.now()
    check_out_time = check_in_time  # For updating the checkout time
    other_fields = "Any other necessary info"

    # Check if there's an existing record with a null checkout time
    query_check = """
    SELECT id FROM parking_records
    WHERE plate_number = %s AND check_out_time IS NULL
    """
    cursor.execute(query_check, (plate_number,))
    result = cursor.fetchone()

    if result:
        # Update the checkout time
        query_update = """
        UPDATE parking_records
        SET check_out_time = %s
        WHERE id = %s
        """
        cursor.execute(query_update, (check_out_time, result[0]))
    else:
        # Insert a new record
        query_insert = """
        INSERT INTO parking_records (plate_number, extracted_characters, check_in_time, check_out_time, other_fields)
        VALUES (%s, %s, %s, NULL, %s)
        """
        cursor.execute(query_insert, (plate_number, extracted_characters, check_in_time, other_fields))

    conn.commit()
    cursor.close()
    conn.close()

def main():
    cap = cv2.VideoCapture(0)
    previous_plate = 'Unknown'

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        plate_number, extracted_characters = perform_ocr(frame)

        if plate_number == 'Unknown' and previous_plate != 'Unknown' and previous_plate in detected_plates:
            store_or_update_record(previous_plate, detected_plates[previous_plate]['extracted_characters'])
            del detected_plates[previous_plate]
        
        if plate_number != 'Unknown':
            detected_plates[plate_number] = {'extracted_characters': extracted_characters}
        
        previous_plate = plate_number
        
        # Display the OCR results on the frame
        cv2.putText(frame, f'Number Plate: {plate_number}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Characters: {extracted_characters}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show the frame
        cv2.imshow('Number Plate Detection', frame)
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
