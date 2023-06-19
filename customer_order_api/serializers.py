from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from customer_profile_api.serializers import CustomerAddressSerializer
from .models import *


class OrderItemSerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(
        source='product.code',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('id', 'order',)


class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'order',
        )


class OrderSerializer(WritableNestedModelSerializer):
    customer_id = serializers.CharField(
        source="customer.user.id",
        read_only=True
    )
    customer_username = serializers.CharField(
        source="customer.user.username",
        read_only=True
    )
    customer_email = serializers.CharField(
        source="customer.user.email",
        read_only=True
    )
    # customer_avatar = serializers.CharField(
    #     source="customer.avatar",
    #     read_only=True
    # )
    customer_phone = serializers.CharField(
        source="customer.phone",
        read_only=True
    )
    vendor_name = serializers.CharField(
        source="vendor.company_name",
        read_only=True
    )
    vendor_user_id = serializers.CharField(
        source="vendor.user.id",
        read_only=True
    )
    vendor_image = serializers.ImageField(
        source="vendor.vendor_images",
        read_only=True
    )

    order_items = OrderItemSerializer(many=True)
    # payment = PaymentDetailsSerializer(required=False)
    delivery_address = CustomerAddressSerializer(read_only=True, required=False)
    promo_discount = serializers.CharField(
        source="promo_code.discount",
        read_only=True
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'id',
            'customer',
            'order_total',
            'is_payment_successful',
            'status',
            'status',
            'created',
            'updated'
        )

    # def create(self, validated_data):
    #     order = Order.objects.create(**validated_data)
    #     payment_data = validated_data.pop('PaymentDetails_data')
    #     payment_instance = PaymentDetails.objects.create(
    #         order=order,
    #         **payment_data
    #     )


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        payment = PaymentDetailsSerializer(required=False)
        fields = (
            'status',
            'payment',
        )
        read_only_fields = (
            'id',
            'vendor'
        )
