from django.contrib import admin
from django.urls import path

from inventory_api import views

urlpatterns = [
    path('product-categories/', views.ProductCategoryList.as_view(), name="product-categories"),
    path('departments/', views.DepartmentList.as_view(), name="department_list"),
    path('department-details/<pk>/', views.DepartmentDetail.as_view(), name="department_details"),
    path('products/', views.ProductList.as_view(), name='product'),
    path('product-create/', views.ProductCreate.as_view(), name='product-create'),
    path('product-details/<pk>/', views.ProductDetail.as_view(), name='product-details'),
    path('product-category-details/<pk>/', views.ProductCategoryDetail.as_view(), name='product-category-details'),
    path('product-subcategories/', views.ProductSubCategoryList.as_view(), name='product-subcategories'),
    path('product-subcategory-details/<pk>/', views.ProductSubCategoryDetail.as_view(), name='product-subcategory-details'),
    path('product-minicategories/', views.ProductMiniCategoryList.as_view(), name='product-minicategories'),
    path('product-minicategory-details/<pk>/', views.ProductMiniCategoryDetail.as_view(), name='product-minicategory-details'),

    path('product-warranty/', views.ProductWarrantyList.as_view(), name='product-warranty'),
    path('update-warranty/<int:pk>/', views.ProductWarrantyUpdate.as_view(), name='update-warranty'),

    path('promocodes/', views.PromoCodeList.as_view()),
    path('promocode/<int:pk>/', views.PromoCodeDetail.as_view()),
    path('promocode/<str:code>/', views.PromoCodeData.as_view()),

    path('purchase-list/', views.PurchaseListCreateView.as_view()),
    path('purchase-details/<int:pk>/', views.PurchaseDetails.as_view()),
    path('get-product-details/<str:code>/', views.GETProductDetail.as_view()),


    path('search-all-product/', views.search_all_product, name='search_all_product'),
    path('filter-categorized-product/<slug:slug>/', views.filter_categorized_product, name='search_categorized_product'),
    path('single-vendor-product/<int:vendor_id>/', views.VendorProduct, name='VendorProduct'),

    path('addcomment/<int:id>/', views.addcomment, name='addcomment'),

]
