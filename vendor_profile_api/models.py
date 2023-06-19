from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from stdimage import StdImageField
# from customer.models import CustomerProfile
# from delivery_module_api.models import *
from django.conf import settings
# from inventory_api.models import Supplier
# from inventory_api.models import Vendor, Supplier
User = settings.AUTH_USER_MODEL


class Vendor(models.Model):
    BUSINESS_TYPE_CHOICES = (
        ('Private Limited Company', 'Private Limited Company'),
        ('Public Limited Company', 'Public Limited Company'),
        ('Proprietorship Company', 'Proprietorship Company'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Disabled', 'Disabled'),
        ('Blocked', 'Blocked'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vendor_user',
        null=True,
        blank=True
    )
    vendor_business_id = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20,  null=True, blank=True)
    type_of_business = models.CharField(max_length=150, null=True, blank=True, choices=BUSINESS_TYPE_CHOICES,)
    status = models.CharField(max_length=150, default='Pending', choices=STATUS_CHOICES,)
    company_owner_name = models.CharField(max_length=150, null=True, blank=True)
    year_of_establishment = models.CharField(max_length=5,null=True,blank=True)
    vat_id = models.IntegerField(null=True, blank=True)
    account_status = models.CharField(max_length=5, default="N")
    nid_front_image = models.ImageField(
        upload_to='media/images/vendor_images/NID/',
        blank=True,
        null=True,
        editable=True,
    )
    nid_back_image = models.ImageField(
        upload_to='media/images/vendor_images/NID/',
        blank=True,
        null=True,
        editable=True,)
    legal_document_img = models.ImageField(
        upload_to='media/images/vendor_images/legal_doc/',
        blank=True,
        null=True,
        editable=True,
    )
    legal_document_file = models.FileField(
        upload_to='media/images/vendor_images/legal_doc/',
        blank=True,
        null=True,
        editable=True,
    )
    # suplier_rating = models.IntegerField()

    account_number = models.CharField(max_length=150)
    account_name = models.CharField(max_length=150)
    bank_name = models.CharField(max_length=150)
    account_holder_name = models.CharField(max_length=150,null=True, blank=True)
    branch_name = models.CharField(max_length=150)
    branch_address = models.CharField(max_length=150,null=True, blank=True)
    type_of_account = models.CharField(max_length=50,null=True, blank=True)
    routing_no = models.CharField(max_length=50, null=True, blank=True)
    cheque_img = models.ImageField(
        upload_to='media/images/vendor_images/cheque/',
        blank=True,
        null=True,
        editable=True,
    )
    likes = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    banner_image = StdImageField(
        upload_to='media/images/vendor_images/',
        blank=True,
        null=True,
        editable=True,
    )
    optional_banner_image = StdImageField(
        upload_to='media/images/vendor_images/',
        blank=True,
        null=True,
        editable=True,
    )
    profile_image = StdImageField(
        upload_to='media/images/vendor_images/',
        blank=True,
        null=True,
        editable=True,
        variations={'thumbnail': (220, 140)}, delete_orphans=True
    )

    def __str__(self):
        return self.company_name



# class VendorBankAccount(models.Model):
#     vendor = models.ForeignKey(
#         Vendor,
#         on_delete=models.CASCADE,
#         related_name='vendor_account'
#     )
#     account_number = models.CharField(max_length=150)
#     account_name = models.CharField(max_length=150)
#     bank_name = models.CharField(max_length=150)
#     account_holder_name = models.CharField(max_length=150)
#     branch_name = models.CharField(max_length=150)
#     branch_address = models.CharField(max_length=150)
#     type_of_account = models.CharField(max_length=50)
#     routing_no = models.CharField(max_length=50,null=True, blank=True)
#     cheque_img = models.ImageField(
#         upload_to='media/images/vendor_images/cheque/',
#         blank=True,
#         null=True,
#         editable=True,
#     )
#     created = models.DateField(auto_now_add=True)
#     updated = models.DateField(auto_now=True)
#
#     def __str__(self):
#         return self.vendor.company_name


# class Supplier(models.Model):
#     id = models.AutoField(primary_key=True)
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='supplier_vendor',null=True, blank=True)
#     supplier_name = models.CharField(max_length=50)
#     supplier_email = models.EmailField(max_length=50, null=True)
#     supplier_phone = models.CharField(max_length=15, null=True)
#     supplier_address = models.CharField(max_length=120, null=True)
#     slug = models.SlugField(null=True, blank=True, unique=True)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.supplier_name)
#         super(Supplier, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return self.supplier_name
