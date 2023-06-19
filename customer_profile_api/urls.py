from django.urls import path

from customer_profile_api import views

urlpatterns = [
    path('customer-profile-list/', views.CustomerList.as_view(), name='customer-list'),
    path('customer-profile-create/', views.CustomerProfileCreate.as_view(), name='customer-profile-create'),
    path('customer-profile-details/<int:user>/', views.CustomerProfileDetails.as_view(), name='customer-profile-details'),
    path('customer-address-create/', views.CustomerAddressCreate.as_view(), name='customer-address-create'),
    path('customer-address-details/<int:user>/', views.CustomerAddressDetails.as_view(), name='customer-address-details'),
]
