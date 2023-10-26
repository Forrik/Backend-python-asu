from collections.abc import Mapping
from typing import Any
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from api.exceptions import BussinesLogicException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    if isinstance(exc, IntegrityError):
        if 'unique constraint' in str(exc.args).lower():
            return Response({"error": "Заявка уже существует"}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            raise exc # Not the unique error we were expecting
    elif isinstance(exc, BussinesLogicException):
        return Response({"error": exc.message, "details": exc.details}, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, ValidationError):
        return Response({"error": exc.message}, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, ObjectDoesNotExist):
        return Response({"error": "Требуемая связанная сущность не найдена"}, status=status.HTTP_404_NOT_FOUND)

    # return Response({"error": "Заявка уже существует"}, status=status.HTTP_400_BAD_REQUEST) 
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response