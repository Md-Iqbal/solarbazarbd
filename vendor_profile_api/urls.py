from django.urls import path
from vendor_profile_api import views

urlpatterns = [
    path('vendor-list/', views.VendorList.as_view(), name='vendor_list'),
    # path('vendor-bank-account-list/', views.VendorBankAccountList.as_view(), name='vendor_bank_account_list'),
    path('supplier-list/', views.SupplierList.as_view(), name='supplier_list'),

    path('supplier-details/<int:pk>/', views.SupplierDetails.as_view(), name='supplier_details'),

]
