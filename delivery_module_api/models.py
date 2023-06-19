from django.db import models
from customer_order_api.models import Order
from django.utils.text import slugify
from stdimage import StdImageField


# Create your models here.


class DeliveryMan(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    # account = models.ForeignKey(Account)
    join_ate = models.DateField()
    nid_or_passport_number = models.CharField(max_length=20)
    nid_or_passport_image = StdImageField(
        upload_to='media/images/delivery_man_images/',
        blank=True,
        null=True,
        editable=True,
        variations={'thumbnail': (220, 140)}, delete_orphans=True
    )
    drivingLicences = models.CharField(max_length=150)
    images = StdImageField(
        upload_to='media/images/delivery_man_images/',
        blank=True,
        null=True,
        editable=True,
        variations={'thumbnail': (220, 140)}, delete_orphans=True
    )


class ServiceMan(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=25)
    nid_or_pass = models.CharField(max_length=150)
    license_plate_number = models.CharField(max_length=150)
    license = models.CharField(max_length=150)


class DeliveryService(models.Model):
    service_name = models.CharField(max_length=150)
    company_details = models.TextField()
    service_man = models.ForeignKey(ServiceMan, on_delete=models.CASCADE)


class OrderDelivery(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_delivery',
        on_delete=models.CASCADE
    )
    delivered_by = models.ForeignKey(
        DeliveryMan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    service_company = models.ForeignKey(
        DeliveryService,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    delivery_charge = models.DecimalField(
        decimal_places=2,
        max_digits=5
    )
    is_done = models.BooleanField(default=False)
    delivery_pickup_time = models.TimeField()
    delivery_receive_time = models.TimeField()
