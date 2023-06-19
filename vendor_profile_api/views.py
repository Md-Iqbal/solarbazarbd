from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)

# from user_profile.serializers import (
#     CustomerProfileSerializer, RestaurantOwnerProfileSerializer
# )
from user_auth.permissions import IsAdmin
from .models import *
from vendor_profile_api.serializers import *

from user_auth.models import User


# Create your views here.


class SupplierList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SupplierSerializer

    def get_queryset(self):
        try:
            v_id = self.request.user.id
            queryset = Supplier.objects.filter(vendor__id=v_id)
            return queryset
        except:
            raise ValidationError('You do not have access')


    def vendor_check(self):
        try:
            queryset = Supplier.objects.filter(vendor_id=self.request.user.id)
        except:
            raise ValidationError('You do not have access')

    def perform_create(self, serializer):
        vendor = Vendor.objects.get(id=self.request.user.id)
        serializer.save(vendor=vendor)


class SupplierDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    # def perform_create(self, serializer):
    #     vendor = Vendor.objects.get(user=self.request.user)
    #     serializer.save(vendor=vendor)


class VendorList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    def perform_create(self, serializer):
        u_email = self.request.data['email']
        u_pass = self.request.data['password']
        if User.objects.filter(email=u_email).exists():
            raise ValidationError('Vendor exists with this email. Please try with another one')
        else:
            if serializer.is_valid():
                u = User.objects.create(username=u_email, email=u_email, is_vendor=True)
                u.set_password(u_pass)
                u.save()
            else:
                u=None
            serializer.save(user=u)
