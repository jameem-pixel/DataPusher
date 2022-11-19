from rest_framework import serializers
from .import models as server_models


class AccountListSerializer(serializers.ModelSerializer):
    destinations = serializers.SerializerMethodField(read_only=True)

    def get_destinations(self, data):
        destination_list = server_models.Destination.objects.filter(account=data, datamode="A")
        return AccountDestinationSerializer(destination_list, many=True).data

    class Meta:
        model = server_models.Account
        fields = ['email_id', 'account_name', 'account_id', 'app_secert_token', 'website', 'destinations', 'created_on', 'updated_on']


class AccountCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = server_models.Account
        exclude = ['app_secert_token']


class AccountDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = server_models.Destination
        fields = ['destination', 'http_method']


class DestinationListSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField(read_only=True)

    def get_account(self, data):
        return {'account_name':data.account.account_name, 'account_id':data.account.account_id}

    class Meta:
        model = server_models.Destination
        fields = ['account' ,'destination', 'http_method', 'headers', 'created_on', 'updated_on']


class DestinationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = server_models.Destination
        fields = '__all__'