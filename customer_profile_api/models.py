from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Create your models here.
from stdimage import StdImageField


class CustomerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customer_profile', null=True, blank=True)
    name = models.CharField(max_length=150, null=True,blank=True)
    phone = models.CharField(max_length=50, null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    image = StdImageField(
        upload_to='images/customer_images/',
        blank=True,
        null=True,
        editable=True,
        delete_orphans=True,
    )
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    short_address = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.phone


class CustomerAddress(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='customer_address')
    zip_code = models.CharField(max_length=50)
    area = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=50, null=True)
    house_number = models.CharField(max_length=50, null=True)
    flat_number = models.CharField(max_length=50, null=True)
    floor_number = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.customer.user.username
