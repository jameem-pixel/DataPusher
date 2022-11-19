from functools import wraps
from .import api
from .import models as server_models
from rest_framework import status


def incoming_data_decorator(function):
  @wraps(function)
  def wrapper_func(request, *args, **kwargs):
        if request.method != 'POST' or request.META.get('CONTENT_TYPE') != 'application/json':
            message = "Invalid Data"
            return api.build_response(status.HTTP_400_BAD_REQUEST, message, data=dict(), errors=dict())

        elif 'HTTP_X_AUTHORIZATION' not in request.META or not server_models.Account.objects.filter(app_secert_token=request.META.get('HTTP_X_AUTHORIZATION'), datamode='A').exists():
            message = "Un Authenticated"
            return api.build_response(status.HTTP_400_BAD_REQUEST, message, data=dict(), errors=dict())
        else:
            return function(request, *args, **kwargs)
  return wrapper_func