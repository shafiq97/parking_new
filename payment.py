from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/create-bill', methods=['POST'])
def create_bill():
    data = request.json

    some_data = {
        'userSecretKey': 'alk2vfq0-9uxw-cnmf-je7l-nxnmp9cojlp8',
        'categoryCode': 'pwxbgjun',
        'billName': data['billName'],
        'billDescription': data['billDescription'],
        'billPriceSetting': 0,
        'billPayorInfo': 1,
        'billAmount': 100,
        'billReturnUrl': data['billReturnUrl'],
        'billCallbackUrl': data['billCallbackUrl'],
        'billExternalReferenceNo': data['billExternalReferenceNo'],
        'billTo': data['billTo'],
        'billEmail': data['billEmail'],
        'billPhone': data['billPhone'],
        'billSplitPayment': 0,
        'billPaymentChannel': '0',
        'billContentEmail': 'Thank you for purchasing our product!',
        'billChargeToCustomer': 1,
        'billExpiryDate': data['billExpiryDate'],
        'billExpiryDays': data['billExpiryDays']
    }

    response = requests.post('https://dev.toyyibpay.com/index.php/api/createBill', data=some_data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5001)
