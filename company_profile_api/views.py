from rest_framework import generics

# Create your views here.
from .models import *
from .serializers import *


class AboutUsList(generics.ListCreateAPIView):
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.filter()


class AboutUsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.filter()


class SpecialTeamList(generics.ListCreateAPIView):
    serializer_class = SpecialTeamSerializer
    queryset = SpecialTeam.objects.filter().order_by('priority')


class SpecialTeamDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SpecialTeamSerializer
    queryset = SpecialTeam.objects.filter().order_by('priority')


class ContactUSList(generics.ListCreateAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.filter()


class ContactUsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.filter()


class PoliciesList(generics.ListCreateAPIView):
    serializer_class = CompanyPolicySerializer
    queryset = CompanyPolicy.objects.filter()


class PoliciesDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyPolicySerializer
    queryset = CompanyPolicy.objects.filter()


class FaqList(generics.ListCreateAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.filter()


class FaqDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.filter()
