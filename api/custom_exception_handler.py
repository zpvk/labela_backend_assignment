from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 404:
            # Customize the response for 404 errors
            custom_data = {'detail': 'Not found'}
            response.data = custom_data
            response.status_code = status.HTTP_404_NOT_FOUND
        else:
            # For other exceptions, include the status code in the response data
            response.data['status_code'] = response.status_code
    
    return response