from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    keys = list(response.data)
    if response is not None:
        response.data = {
            "data":response.data,
            "message":response.data[keys[0]][0],
            "success":False
        }
    return response
