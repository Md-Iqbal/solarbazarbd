
from django.urls import path

from company_profile_api import views

urlpatterns = [

    path('aboutus-list/', views.AboutUsList.as_view()),
    path('aboutus-details/<pk>/', views.AboutUsDetails.as_view()),
    path('special-team-list/', views.SpecialTeamList.as_view()),
    path('special-team-details/<pk>/', views.SpecialTeamDetails.as_view()),
    path('contactus-list/', views.ContactUSList.as_view()),
    path('contactus-details/<pk>/', views.ContactUsDetails.as_view()),
    path('policies-list/', views.PoliciesList.as_view()),
    path('policies-details/<pk>/', views.PoliciesDetails.as_view()),
    path('faq-list/', views.FaqList.as_view()),
    path('faq-details/<pk>/', views.FaqDetails.as_view()),
    # path('main-slider-list/', views.MainSliderList.as_view()),
    # path('main-slider-upload-details/<pk>/', views.MainSliderDetails.as_view()),



    ]