from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [

    path('404/', views.Error404.as_view(), name='404'),
    path('about/', views.about_us, name='about'),
    path('blog/', views.Blog.as_view(), name='blog'),
    path('blog-single/', views.BlogSingle.as_view(), name='blog-single'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('', views.Index.as_view(), name='home'),
    path('order-received/', views.OrderReceived.as_view(), name='order-received'),
    path('product-category/', views.ProductCategoryView.as_view(), name='product-category'),
    path('shop/<slug:slug>/', views.Shop.as_view(), name='shop'),
    path('vendor-products/<int:vendor_id>/', views.VendorShop, name='VendorShop'),
    path('shop-fullwidth/', views.ShopFullWidth.as_view(), name='shop-fullwidth'),
    path('product/<id>/', views.single_product_view, name='single-product-fullwidth'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms-and-conditions'),
    path('privacy-policy/', views.company_policy, name='privacy-policy'),
    path('return-refund-policy/', views.return_refunt_policy, name='return-refund-policy'),
    path('track-your-order/', views.TrackYourOrder.as_view(), name='track-your-order'),
    path('wishlist/', views.Wishlist.as_view(), name='wishlist'),
    path('get-product-details/', views.get_product_details, name='get_product_details'),
    path('vendor-registration/', views.VendorApplication.as_view(), name='vendor_registration'),
    path('category/<slug:slug>/', views.ProductView.as_view(), name='category_view'),
    path('department/<slug:slug>/', views.DepartmentView.as_view(), name='department_view'),
    path('single-category-product/', views.SingleProductCategoryView.as_view(), name='single-category-product'),
    path('login_required', views.login_required, name='login_required'),
    path('customer-login/', views.customer_login, name='customer_login'),
    path('customer-signup/', views.customer_signup, name='customer_signup'),
    path('customer-logout/', views.customer_logout, name='customer_logout'),
    path('otp-verification/', views.OTP_VerificationView, name='OTP_Verification'),
    path('order-details/<int:id>/', views.OrderDetailsTemplateView.as_view(), name='order_details'),
    path('invoice/<int:id>/', views.OrderInvoiceView.as_view(), name='order_invoice'),
    path('orders/', views.MyOrdersView.as_view(), name='my_orders'),
    path('store-location/', views.StoreLocationView.as_view(), name='store_location'),
    path('profile/', views.MyAccountView.as_view(), name='customer_profile'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('search/', views.search, name='search'),
    path('create-payment/<order_id>/', views.CreatePayment.as_view(), name='create_payment'),
    path('success-payment/<order_id>/<trx>/', views.SuccessPayment.as_view(), name='success_payment'),

]

# single-product-fullwidth
