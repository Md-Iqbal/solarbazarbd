from django.shortcuts import render
from .serializers import *
from rest_framework import generics

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import TemplateView, View
from .models import *
from company_profile_api.models import ContactUs

# Create your views here.


class StaticFileList(generics.ListCreateAPIView):
    serializer_class = StaticFilesSerializer
    queryset = StaticFiles.objects.filter()


class StaticFileDetails(generics.RetrieveDestroyAPIView):
    serializer_class = StaticFilesSerializer
    queryset = StaticFiles.objects.filter()


class MainSliderList(generics.ListCreateAPIView):
    serializer_class = MainSliderSerializer
    queryset = MainSlider.objects.filter()


class MainSliderDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MainSliderSerializer
    queryset = MainSlider.objects.filter()


#**************moved brand api

class BrandList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

    # def perform_create(self, serializer):
    #     vendor = Vendor.objects.get(user=self.request.user)
    #     serializer.save(vendor=vendor)
class BrandDetails(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()







