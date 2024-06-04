from flask import Flask, request, jsonify
import mysql.connector
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/payments', methods=['POST'])
def add_payment():
    data = request.json
    app.logger.debug(f"Received data: {data}")
    
    # Perform validation on the received data if necessary
    required_fields = ['name', 'vehicalNumber', 'slotId', 'slotName', 'parkingTimeInMin', 'amount', 'floor']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        app.logger.error(f"Missing fields: {missing_fields}")
        return jsonify({'error': f'Missing data: {missing_fields}'}), 400

    try:
        # Connect to your MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="parking_db"
        )

        cursor = db_connection.cursor()

        # Insert the payment data into the database
        sql = "INSERT INTO payments (name, vehical_number, slot_id, slot_name, parking_time_in_minutes, amount, floor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (data['name'], data['vehicalNumber'], data['slotId'], data['slotName'], data['parkingTimeInMin'], data['amount'], data['floor'])
        cursor.execute(sql, values)

        # Commit changes to the database
        db_connection.commit()

        # Close cursor and database connection
        cursor.close()
        db_connection.close()

        # Return a success message
        return jsonify({'message': 'Payment added successfully'}), 200

    except mysql.connector.Error as err:
        # Log the error
        app.logger.error(f"Database error: {err}")
        return jsonify({'error': str(err)}), 500

    except Exception as e:
        # Log any other exceptions
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    app.logger.debug(f"Received data: {data}")
    
    # Perform validation on the received data if necessary
    if not all(k in data for k in ('userId', 'email', 'studentId', 'licenseNumber', 'licensePlate')):
        return jsonify({'error': 'Missing data'}), 400

    try:
        # Connect to your MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="parking_db"
        )

        cursor = db_connection.cursor()

        # Insert the user data into the database
        sql = "INSERT INTO users (user_id, email, student_id, license_number, license_plate) VALUES (%s, %s, %s, %s, %s)"
        values = (data['userId'], data['email'], data['studentId'], data['licenseNumber'], data['licensePlate'])
        cursor.execute(sql, values)

        # Commit changes to the database
        db_connection.commit()

        # Close cursor and database connection
        cursor.close()
        db_connection.close()

        # Return a success message
        return jsonify({'message': 'User registered successfully'}), 200

    except mysql.connector.Error as err:
        # Log the error
        app.logger.error(f"Database error: {err}")
        return jsonify({'error': str(err)}), 500

    except Exception as e:
        # Log any other exceptions
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
