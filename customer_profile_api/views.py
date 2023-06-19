from django.shortcuts import render
import json
from django.http import JsonResponse
# Create your views here.
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_auth.permissions import IsAdmin, IsCustomer
from .serializers import *


class CustomerList(generics.ListAPIView):
    """
    endpoint for viewing customer list
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        queryset = CustomerProfile.objects.all()
        return queryset


class CustomerProfileCreate(generics.CreateAPIView):
    """
    endpoint for creating customer profile
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = CustomerProfile.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        customerdata = CustomerProfile.objects.filter(user=user)
        # if user is superuser
        if not user.is_admin:
            raise ValidationError(
                'Superuser can not create a customer profile'
            )
        elif customerdata.exists():
            raise ValidationError('customer profile already exists')
        else:
            serializer.save(user=user)


class CustomerProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for updating or deleting the customer profile
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)
    serializer_class = CustomerProfileUpdateSerializer
    queryset = CustomerProfile.objects.all()
    lookup_field = 'user'


class CustomerAddressCreate(generics.CreateAPIView):
    """
    endpoint for creating customer profile
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)
    serializer_class = CustomerAddressSerializer
    queryset = CustomerAddress.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        customerdata = CustomerAddress.objects.filter(user=user)
        # if user is superuser
        if user.is_admin:
            raise ValidationError(
                'Superuser can not create a customer profile'
            )
        elif customerdata.exists():
            raise ValidationError('customer profile already exists')
        else:
            serializer.save(user=user)


class CustomerAddressDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for updating or deleting the customer profile
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsCustomer)
    serializer_class = CustomerAddressUpdateSerializer
    queryset = CustomerAddress.objects.all()
    lookup_field = 'user'
