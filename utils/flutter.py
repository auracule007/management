import requests
from django.conf import settings
from rest_framework.response import Response
import uuid

def initiate_payment(amount, email, enrollment_id,user_id, first_name, last_name, phone):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLUTTER_SECRET_KEY}"
        
    }
    
    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount), 
        "currency": "USD",
        "redirect_url": "http:/127.0.0.1:8000/api/enrollment/confirm-payment/?enrollment_id=" + str(enrollment_id),
        "meta": {
            "consumer_id": user_id,
            "consumer_mac": str(uuid.uuid4()) #generate 
        },
        "customer": {
            "email": email,
            "phonenumber": phone,
            "name": f'{first_name} {last_name}'
        },
        "customizations": {
            "title": "Pied Piper Payments",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
        }
    }
    

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        return Response(response_data)
    
    except requests.exceptions.RequestException as err:
        print("the payment didn't go through", err)
        return Response({"error": str(err)}, status=500)
        