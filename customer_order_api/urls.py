from django.urls import path
from customer_order_api import views

urlpatterns = [
    path('', views.OrderList.as_view()),
    path('update/<int:pk>/', views.OrderDetail.as_view()),
    path('create/', views.OrderCreate.as_view()),
    path('shop-orders/', views.ShopOrderList.as_view()),
    path('active-order/', views.ActiveOrders.as_view()),
    path('previous-completed-order/', views.PreviousOrder.as_view()),
]
