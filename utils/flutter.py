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
        "currency": "NGN",
        "redirect_url": "http://localhost:3000/verify-payment?enrollment_id=" + str(enrollment_id),
        # "redirect_url": f"http:/127.0.0.1:8000/api/enrollment/confirm-payment/?enrollment_id={str(enrollment_id)}&status={status}&transaction_id={transaction_id}&tx_ref={tx_ref}",
        # "redirect_url": "https://codedexteracademy.onrender.com/api/enrollment/confirm-payment/?enrollment_id=" + str(enrollment_id),
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
        # response_data['confirm_payment_endpoint'] = f"https://codedexteracademy.onrender.com/api/enrollment/confirm-payment/?enrollment_id={enrollment_id}"
        return Response(response_data)
    
    except requests.exceptions.RequestException as err:
        print("the payment didn't go through", err)
        return Response({"error": str(err)}, status=500)
        