from rest_framework import serializers

from inventory_api.models import Supplier
from .models import *

User = settings.AUTH_USER_MODEL


class PatchModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PatchModelSerializer, self).__init__(*args, **kwargs)


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ('id', 'user',)


# class VendorBankAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VendorBankAccount
#         fields = '__all__'
#         read_only_fields = ('id',)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('id', 'vendor')

