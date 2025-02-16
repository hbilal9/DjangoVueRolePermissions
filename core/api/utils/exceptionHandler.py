from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print("Custom exception handler called")

    if response is not None and isinstance(exc, ValidationError):
        response.data = {
            'message': 'Invalid data',
            'errors': response.data
        }
        response.status_code = 422

    return response