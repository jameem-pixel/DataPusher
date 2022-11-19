import sys
import requests
import concurrent.futures
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from .import models as server_models
from .import serializers as server_serializers

HTTP_REST_MESSAGES = {"200": _("Success"),
                      "400": _("Failed"),
                      "401": _("Authentication Failed"),
                      "500": _("Internal server error")}


def build_response(status, message, data=dict(), errors=dict()):
    try:
        return Response({'status_code': status, 'message': message, 'data':data,'errors': errors}, status=status)
    except Exception as e:
        print('Exception :', e)


def get_account_list(request):
    result = False
    msg = 'Error'
    data = dict()
    try:
        account_list = server_models.Account.objects.filter(datamode='A')
        serializer = server_serializers.AccountListSerializer(account_list, many=True)
        result, msg, data = True, 'Success', serializer.data
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return result, msg, data


def create_account(request):
    result = False
    msg = 'Error'
    data = dict()
    try:
        pDict = request.POST.copy()
        serializer = server_serializers.AccountCreateUpdateSerializer(data=pDict)
        if serializer.is_valid():
            serializer.save()
            result, msg = True, 'Account Created Successfully'
        else:
            data = serializer.errors
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return result, msg, data


def update_account(request, account_id, mode):
    result = False
    msg = 'Error'
    data = dict()
    try:
        if mode == 'edit':
            account = server_models.Account.objects.filter(account_id=account_id, datamode='A').first()
            if account:
                pDict = request.POST.copy()
                serializer = server_serializers.AccountCreateUpdateSerializer(instance=account, data=pDict)
                if serializer.is_valid():
                    serializer.save()
                    result, msg = True, 'Account Updated Successfully'
                else:
                    data = serializer.errors
        elif mode == 'delete':
            account = server_models.Account.objects.filter(account_id=account_id, datamode='A').first()
            if account:
                account.datamode = 'D'
                account.save()
                destionations = server_models.Destination.objects.filter(account=account, datamode='A')
                destionations.update(datamode='D')
                result, msg = True, 'Account Deleted Successfully'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return result, msg, data


def get_destination_list(request, account_id=None):
    result = False
    msg = 'Error'
    data = dict()
    try:
        if account_id:
            destination_list = server_models.Destination.objects.filter(account__account_id=account_id, datamode='A')
        else:
            destination_list = server_models.Destination.objects.filter(datamode='A')
        serializer = server_serializers.DestinationListSerializer(destination_list, many=True)
        result, msg, data = True, 'Success', serializer.data
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return result, msg, data


def create_destination(request):
    result = False
    msg = 'Error'
    data = dict()
    try:
        pDict = request.POST.copy()
        serializer = server_serializers.DestinationCreateSerializer(data=pDict)
        if serializer.is_valid():
            serializer.save()
            result, msg = True, 'Destination Created Successfully'
        else:
            data = serializer.errors
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return result, msg, data


def update_destination(request, destination_id, mode):
    result = False
    msg = 'Error'
    data = dict()
    try:
        if mode == 'edit':
            destination = server_models.Destination.objects.filter(id=destination_id, datamode='A').first()
            if destination:
                pDict = request.POST.copy()
                serializer = server_serializers.DestinationCreateSerializer(instance=destination, data=pDict)
                if serializer.is_valid():
                    serializer.save()
                    result, msg = True, 'Destination Updated Successfully'
                else:
                    data = serializer.errors
        elif mode == 'delete':
            destination = server_models.Destination.objects.filter(id=destination_id, datamode='A').first()
            if destination:
                destination.datamode = 'D'
                destination.save()
                result, msg = True, 'Destination Deleted Successfully'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return result, msg, data


def send_incoming_data(request):
    result = False
    msg = 'Error'
    data = list()
    try:
        pDict = request.POST.copy()
        account = server_models.Account.objects.filter(app_secert_token=request.META.get('HTTP_X_AUTHORIZATION'), datamode='A').first()
        if account:
            destinations = server_models.Destination.objects.filter(account=account, datamode='A')
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(send_data, destionation.destination, destionation.http_method, destionation.headers) for destionation in destinations]
                for f in concurrent.futures.as_completed(results):
                    data.append(f.result())
            result, msg = True, 'Data Sent'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return result, msg, data


def send_data(url, method, headers):
    data = dict()
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
            response = response.json()
            data[url] = response
        else:
            response = requests.post(url, headers=headers)
            data[url] = response
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('e :', (exc_traceback.tb_lineno, e))
    return data