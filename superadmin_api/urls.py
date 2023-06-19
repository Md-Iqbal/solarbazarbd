
from django.urls import path

from superadmin_api import views

urlpatterns = [

    path('static-files-upload/', views.StaticFileList.as_view()),
    path('static-files-details/<pk>/', views.StaticFileDetails.as_view()),
    path('main-slider-list/', views.MainSliderList.as_view()),
    path('main-slider-upload-details/<pk>/', views.MainSliderDetails.as_view()),


#*************moved brand api url

    path('brand-list/', views.BrandList.as_view(), name='brand_list'),
    path('brand-details/<int:pk>/', views.BrandDetails.as_view(), name='brand_details'),




    ]
