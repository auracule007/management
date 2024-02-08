from django.conf import settings
from rest_framework.response import Response
import uuid
import requests


def initate_pay(amount, order_id):
    url =  "https://sandbox.paypal.com/v2/checkout/orders"
    order_data = {
        "intent": "CAPTURE",
        "application_context": {
            "brand_name": "My Company",
            "shipping_preference": "NO_SHIPPING",
        },
        "purchase_units": [
            {
                "reference_id": str(uuid.uuid4()),
                "amount": {"currency_code": "USD", "value": str(amount)},
            }
        ],
        "return_urls": {
            "return_url": f"http:/127.0.0.1:8000/register/ordercourse/confirm-payment/?order_id={order_id}",          
            "cancel_url": "http:/127.0.0.1:8000/register/ordercourse/",
        },
    }

    headers = {
        "Content-Type": "application/json",
        "PayPal-Request-Id":str(uuid),
        "Authorization": f"Bearer {settings.PAYPAL_CLIENT_ID}",
    }

    try:
        response = requests.post(url,headers=headers,        json=order_data)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        print("the payment didn't go through", err)
        return Response({"error": str(err)}, status=500)


# if response.status_code == 201:
#     order_id = response.json().get("id")
#     return Response({"order_id": order_id})
# else:
#     error_message = response.json().get("message")
#     return Response({"error": error_message}, status=500)


# data = '{ "intent": "CAPTURE", "purchase_units": [ { "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b", "amount": { "currency_code": "USD", "value": "100.00" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "shipping_preference": "SET_PROVIDED_ADDRESS", "user_action": "PAY_NOW", "return_url": "https://example.com/returnUrl", "cancel_url": "https://example.com/cancelUrl" } } } }'

# response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, data=data)
