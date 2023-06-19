from rest_framework import serializers

from user_auth.serializers import UserInfoSerializer
from .models import *


class CustomerProfileSerializer(serializers.ModelSerializer):
    # user_info = UserInfoSerializer(source='user', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')
        depth = 4


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = (
            'id',
            'user',
            'created',
            'updated',
        )


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class CustomerAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'
        read_only_fields = (
            'id',
            'user',
            'created',
            'updated',
        )
