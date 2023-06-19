"""fortune_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = \
    [
        path('admindev/', admin.site.urls),
        path('login/', obtain_auth_token, name='api_token_auth'),
        path('', include('shop.urls')),
        path('vendor/', include('vendor.urls')),
        # path('user-auth/', include('user_auth.urls')),
        path('user-auth/', include('user_auth.urls')),
        path('superadmin/', include('superadmin.urls')),
        path('business-agent/', include('business_agent.urls')),

        # API URLs
        path('api/v1/customer/', include('customer_profile_api.urls')),
        path('api/v1/vendor/', include('vendor_profile_api.urls')),
        path('api/v1/company/', include('company_profile_api.urls')),
        path('api/v1/inventory/', include('inventory_api.urls')),
        path('api/v1/delivery/', include('delivery_module_api.urls')),
        path('api/v1/order/', include('customer_order_api.urls')),
        path('api/v1/superadmin_api/', include('superadmin_api.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
