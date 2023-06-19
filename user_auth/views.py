from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class LoginAndRegistration(TemplateView):
    template_name = 'login-and-register.html'