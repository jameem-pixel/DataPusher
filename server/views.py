from rest_framework import serializers
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from .decorators import incoming_data_decorator
from django.utils.decorators import method_decorator
from . import api
from . import models


class AccountView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        message = None
        try:
            result, msg, data = api.get_account_list(request)
            if result:
                message = api.HTTP_REST_MESSAGES['200']
                return api.build_response(status.HTTP_200_OK, message, data=data, errors=dict())
            else:
                return api.build_response(status.HTTP_400_BAD_REQUEST, message, data=data, errors=dict())
        except Exception as e:
            print('Exception :', e)
            message = api.HTTP_REST_MESSAGES['500']
            return api.build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=dict(), errors=dict())
        
    def post(self, request, account_id=None, mode=None, *args, **kwargs):
        result = False
        message = None
        try:
            if account_id and mode:
                result, msg, data = api.update_account(request, account_id, mode)
            else:
                result, msg, data = api.create_account(request)

            if result:
                message = msg
                return api.build_response(status.HTTP_200_OK, message, data={}, errors=dict())
            else:
                return api.build_response(status.HTTP_400_BAD_REQUEST, message, data=data, errors=dict())
        except Exception as e:
            print('Exception :', e)
            message = api.HTTP_REST_MESSAGES['500']
            return api.build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=dict(), errors=dict())


class DestinationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, account_id=None, *args, **kwargs):
        message = None
        try:
            if account_id:
                result, msg, data = api.get_destination_list(request)
            else:
                result, msg, data = api.get_destination_list(request, account_id)
            if result:
                message = api.HTTP_REST_MESSAGES['200']
                return api.build_response(status.HTTP_200_OK, message, data=data, errors=dict())
            else:
                return api.build_response(status.HTTP_400_BAD_REQUEST, message, data=data, errors=dict())
        except Exception as e:
            print('Exception :', e)
            message = api.HTTP_REST_MESSAGES['500']
            return api.build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=dict(), errors=dict())
        
    def post(self, request, destination_id=None, mode=None, *args, **kwargs):
        result = False
        message = None
        try:
            if destination_id and mode:
                result, msg, data = api.update_destination(request, destination_id, mode)
            else:
                print(request.headers, print(type(request.META)))
                result, msg, data = api.create_destination(request)

            if result:
                message = msg
                return api.build_response(status.HTTP_200_OK, message, data={}, errors=dict())
            else:
                return api.build_response(status.HTTP_400_BAD_REQUEST, message, data=data, errors=dict())
        except Exception as e:
            print('Exception :', e)
            message = api.HTTP_REST_MESSAGES['500']
            return api.build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=dict(), errors=dict())


class IncomingDataView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(incoming_data_decorator, name='dispatch')
    def post(self, request, *args, **kwargs):
        result = False
        message = None
        try:
            result, msg, data = api.send_incoming_data(request)
            if result:
                message = msg
                return api.build_response(status.HTTP_200_OK, message, data={}, errors=dict())
            else:
                return api.build_response(status.HTTP_400_BAD_REQUEST, message, data=data, errors=dict())
        except Exception as e:
            print('Exception :', e)
            message = api.HTTP_REST_MESSAGES['500']
            return api.build_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=dict(), errors=dict())