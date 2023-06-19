from django.urls import path

from user_auth import views

urlpatterns = [
    path('login-and-registration/', views.LoginAndRegistration.as_view(), name='customer-list'),

]
