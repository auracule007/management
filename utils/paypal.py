import requests
import json
from decouple import config
from django.conf import settings
from rest_framework.response import Response
import uuid


# def initate_pay(amount, order_id):
#     paypal_url = settings.PAYPAL_BASE_URL
#     url = paypal_url + "/v2/checkout/orders"
#     data = {
#         "intent": "CAPTURE",
#         "purchase_units": [
#             {
#                 "reference_id": str(uuid.uuid4()),
#                 "amount": {"currency_code": "USD", "value": str(amount)},
#             }
#         ],
#         "payment_source": {
#             "paypal": {
#                 "experience_context": {
#                     "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
#                     "brand_name": "Learning Management",
#                     "locale": "en-US",
#                     "user_action": "PAY_NOW",
#                     "return_url": "http:/127.0.0.1:8000/register/ordercourse/confirm-payment/?order_id=" + order_id,
#                     # "cancel_url": "https://example.com/cancelUrl",
#                 }
#             }
#         },
#     }
#     # access token
#     base_url = paypal_url
#     token_url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
#     token_payload = {"grant_type": "client_credentials"}
#     token_headers = {"Accept": "application/json", "Accept-Language": "en_US"}
#     token_response = requests.post(
#         token_url, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET), data=token_payload, headers=token_headers
#     )

#     if token_response.status_code != 200:
#         return Response({'error':'Failed to authenticate with PayPal API'})

#     access_token = token_response.json().get("access_token")
#     headers = {
#         "Content-Type": "application/json",
#         # "PayPal-Request-Id": str(uuid.uuid4()),
#         "Authorization": f"Bearer{access_token}",
#     }

#     try:
#         response = requests.post(url, headers=headers, data=data)
#         print(response.content)
#         response_data = response.json()
#         return Response(response_data)

#     except requests.exceptions.RequestException as err:
#         print("the payment didn't go through", err)
#         return Response({"error": str(err)}, status=500)

def initate_pay(amount, order_id):
    """Initiates a PayPal payment for the specified amount and order ID.

    Args:
        amount (float): The payment amount in USD.
        order_id (str): The unique order ID for reference.

    Returns:
        dict: The response data from PayPal API, or an error response.
    """

    paypal_url =settings.PAYPAL_BASE_URL
    token_url = f"{paypal_url}/v1/oauth2/token"
    order_url = f"{paypal_url}/v2/checkout/orders"

    # Access token request
    token_payload = {"grant_type": "client_credentials"}
    token_headers = {"Accept": "application/json", "Accept-Language": "en-US"}
    try:
        token_response = requests.post(
            token_url,
            auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
            data=token_payload,
            headers=token_headers,
            timeout=10  # Adjust timeout if needed
        )
    except requests.exceptions.RequestException as err:
        return Response({"error": f"Failed to obtain access token: {err}"}, status=500)

    if token_response.status_code != 200:
        return Response({"error": "Failed to authenticate with PayPal API"}, status=token_response.status_code)

    access_token = token_response.json()["access_token"]

    # Order creation request
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": str(uuid.uuid4()),
                "amount": {"currency_code": "USD", "value": str(amount)},
            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                    "brand_name": "Learning Management",
                    "locale": "en-US",
                    "user_action": "PAY_NOW",
                    "return_url": f"http://127.0.0.1:8000/register/ordercourse/confirm-payment/?order_id={order_id}",
                    # ... other experience context details
                }
            }
        },
    }
    headers = {
        "Content-Type": "application/json",
        # "PayPal-Request-Id": str(uuid.uuid4()),  # Optional
        "Authorization": f"Bearer {access_token}",
    }
    try:
        order_response = requests.post(order_url, headers=headers, data=order_data, timeout=10)
    except Exception as err:
        print(err)

def make_paypal_payment(amount, order_id):
    # Set up PayPal API credentials
    client_id = settings.PAYPAL_ID
    secret = settings.PAYPAL_SECRET
    url = settings.PAYPAL_BASE_URL
    # Set up API endpoints
    base_url = url
    token_url = base_url + "/v1/oauth2/token"
    payment_url = base_url + "/v1/payments/payment"

    # Request an access token
    token_payload = {"grant_type": "client_credentials"}
    token_headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    token_response = requests.post(
        token_url, auth=(client_id, secret), data=token_payload, headers=token_headers
    )

    if token_response.status_code != 200:
        return Response({'error':'Failed to authenticate with PayPal API'})

    access_token = token_response.json()["access_token"]

    # Create payment payload
    payment_payload = {
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [
            {
                "amount": {"total": str(amount), "currency": "USD"},
                "description": "Vulnvision scan & protect ",
            }
        ],
        "redirect_urls": {
            "return_url": "http:/127.0.0.1:8000/register/ordercourse/confirm-payment/?order_id="
            + order_id,
            "cancel_url": "http:/127.0.0.1:8000/register/ordercourse/",
        },
    }

    # Create payment request
    payment_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        payment_response = requests.post(
            payment_url, json=payment_payload, headers=payment_headers
        )
        payment_response_data = payment_response.json()
        payment_id = payment_response.json()["id"]
        approval_url = next(
            link["href"]
            for link in payment_response.json()["links"]
            if link["rel"] == "approval_url"
        )
        data = {
            "message": "payment link",
            "payment_id": payment_id,
            "approval_url": approval_url,
            "response": payment_response_data,
        }
        return Response(data)
        # if payment_response.status_code != 201:
        #     return Response({"error": 'Failed to create PayPal payment.'}, status=201)
        # else:
        #     payment_id = payment_response.json()['id']
        #     approval_url = next(link['href'] for link in payment_response.json()['links'] if link['rel'] == 'approval_url')
        #     data = {
        #         "message": "payment link",
        #         "payment_id":payment_id,
        #         "approval_url":approval_url,
        #         "response": payment_response_data
        #     }
        #     return Response(data)
    except requests.exceptions.RequestException as err:
        print("the payment didn't go through", err)
        return Response({"error": str(err)}, status=500)


def verify_paypal_payment(payment_id):
    # Set up PayPal API credentials
    client_id = config("PAYPAL_ID")
    secret = config("PAYPAL_SECRET")
    url = config("PAYPAL_BASE_URL")

    # Set up API endpoints
    base_url = url
    token_url = base_url + "/v1/oauth2/token"
    payment_url = base_url + "/v1/payments/payment"

    # Request an access token
    token_payload = {"grant_type": "client_credentials"}
    token_headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    token_response = requests.post(
        token_url, auth=(client_id, secret), data=token_payload, headers=token_headers
    )

    if token_response.status_code != 200:
        raise Exception("Failed to authenticate with PayPal API.")

    access_token = token_response.json()["access_token"]

    # Retrieve payment details
    payment_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payment_details_url = f"{payment_url}/{payment_id}"
    payment_details_response = requests.get(
        payment_details_url, headers=payment_headers
    )

    if payment_details_response.status_code != 200:
        raise Exception("Failed to retrieve PayPal payment details.")

    payment_status = payment_details_response.json()["state"]
    if payment_status == "approved":
        # Payment is successful, process the order
        # Retrieve additional payment details if needed
        payer_email = payment_details_response.json()["payer"]["payer_info"]["email"]
        # ... process the order ...
        return True
    else:
        # Payment failed or was canceled
        return False
