from __future__ import unicode_literals
from django.db import models
# from user_profile.models import CustomerProfile, RestaurantOwnerProfile
from django.contrib.auth.models import User
from vendor_profile_api.models import Vendor
from customer_profile_api.models import CustomerProfile, CustomerAddress
from inventory_api.models import *


# from promo_code.models import *
# Create your models here.

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'Order is Pending'),
        ('ACCEPTED', 'Order Accepted'),
        ('SHIPPING', 'Order is on the way'),
        ('DONE', 'Order Completed'),
        ('CANCELED', 'Order Canceled'),
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='vendor_order',
        null=True,
        blank=True
    )
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='customer_order'
    )
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.CASCADE,
        related_name='promo_orders',
        null=True,
        blank=True
    )

    ordered_by = models.CharField(max_length=20,null=True,blank=True)
    # order_tracking_number = models.IntegerField()
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    order_note = models.TextField(max_length=500, null=True, blank=True)
    delivery_address = models.ForeignKey(
        CustomerAddress,
        related_name='shipping_address',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    promo_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=30,
        choices=ORDER_STATUS_CHOICES,
        default='PENDING'
    )
    payment = models.ForeignKey(
        'PaymentDetails',
        on_delete=models.CASCADE,
        related_name='order_payment',
        null=True,
        blank=True
    )
    is_payment_successful = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    accepted_date = models.DateTimeField(null=True,blank=True)
    shipping_start_date = models.DateTimeField(null=True,blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    item_count = models.IntegerField(null=True, blank=True)
    product_list = models.TextField(max_length=1000,null=True, blank=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "%s" % (self.id)

    # if order is active
    @property
    def is_active(self):

        if self.status == "PENDING":
            return True
        elif self.status == "ACCEPTED":
            return True
        elif self.status == "SHIPPING":
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        # temp_price = 0
        # for item in self.order_items.all:
        #     temp_price += item.item_total
        # self.order_total = temp_price
        # if self.promo_code.is_valid:
        #     if self.promo_code.discount_type == 'PERCENTAGE':
        #         self.order_total = self.order_total - (self.order_total*self.promo_code.discount/100)
        #     else:
        #         self.order_total = self.order_total - self.promo_code.discount
        super(Order, self).save(*args, **kwargs)
    @property
    def sub_total(self):
        return sum([obj.quantity*obj.unit_price for obj in
                    OrderItem.objects.filter(order=self.id)])

    @property
    def total_discount(self):
        discount = 0
        if self.promo_code:
            if self.promo_code.discount_type=='PERCENTAGE':
                discount = (self.promo_code.discount*self.order_total)/100
            else:
                discount = self.promo_code.discount
        if self.other_discount:
            discount = discount+self.other_discount
        return discount
    
    @property
    def total_payable(self):
        payable_amount = self.sub_total-self.total_discount+self.total_tax
        return payable_amount


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ordered_product'
    )
    sku = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    @property
    def item_total(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        self.unit_price = self.product.discounted_price
        super(OrderItem, self).save(*args, **kwargs)


class PaymentDetails(models.Model):
    id = models.AutoField(primary_key=True)
    PAYMENT_METHOD_CHOICES = (
        ('BKASH', 'BKASH'),
        ('ROCKET', 'ROCKET'),
        ('CARD', 'CARD'),
        ('CASHON', 'CASHON'),
        ('SSLCOMMERZ', 'SSLCOMMERZ'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Payment is pending'),
        ('PAID', 'Payment received'),
        ('PARTIAL', 'Partial payment received'),
        ('FAILED', 'Payment Failed'),
    )

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_id = models.CharField(max_length=70, null=True,blank=True)
    is_failed = models.BooleanField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.amount_paid is None or self.amount_paid is 0:
    #         self.amount_paid = self.order.order_total
    #     if self.payment_status == 'FAILED':
    #         self.is_failed = True
    #     super(PaymentDetails, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.id)+' '+self.payment_method+' ' +self.payment_status


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_from'
    )
    user_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_to'
    )
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
