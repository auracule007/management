from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


# For serializers
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (InvalidToken, TokenError)):
        response.data = {"message": "Validation failed", "errors": response.data}

    if isinstance(exc, AuthenticationFailed):
        response.data = {"message": "Validation failed", "errors": response.data}

    if isinstance(exc, ValidationError):
        response.data = {"message": "Validation failed", "errors": response.data}

    return response
