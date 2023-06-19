from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'created', 'is_payment_successful')
    list_filter = ('is_payment_successful',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    def order(self, obj):
        return obj.order.id

    def product(self, obj):
        return obj.product.code

    list_display = ('order', 'product', 'quantity')


@admin.register(PaymentDetails)
class PaymentDetailsAdmin(admin.ModelAdmin):
    def order_no(self, obj):
        return obj.order_no.id

    list_display = ( 'transaction_id', 'is_failed')
    list_filter = ('is_failed',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    def user_from(self, obj):
        return obj.user_from.username

    def user_to(self, obj):
        return obj.user_to.username

    list_display = (
        'user_from',
        'user_to',
        'title',
        'created'
    )
