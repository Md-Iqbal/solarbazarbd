from datetime import date

# from customer.models import CustomerProfile
# from delivery_module_api.models import *
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from stdimage import StdImageField

from vendor_profile_api.models import Vendor, Supplier
#for searche engine
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from .custom_model_managers import *

User = settings.AUTH_USER_MODEL


# product category
class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    alternative_name = models.CharField(max_length=200, null=True, blank=True)
    descriptions = models.TextField(null=True, blank=True)
    icon = models.ImageField(
        # upload_to='media/images/category_images/' + str(name) + '/',
        upload_to='images/category_images/',
        blank=True,
        null=True,
        editable=True,
    )
    image = StdImageField(
        upload_to='images/category_images/',
        blank=True,
        null=True,
        editable=True,
        variations={'thumbnail': (120, 100)}, delete_orphans=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# product sub-category
class ProductSubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        ProductCategory,
        related_name='product_subcategory_category',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=150)
    alternative_name = models.CharField(max_length=150, null=True)
    descriptions = models.TextField(null=True)
    icon = StdImageField(
        upload_to='media/images/category_images/',
        blank=True,
        null=True,
        editable=True,
    )
    image = StdImageField(
        upload_to='media/images/category_images/',
        blank=True,
        null=True,
        editable=True,
        variations={'thumbnail': (120, 100)}, delete_orphans=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductSubCategory, self).save(*args, **kwargs)


class ProductWarranty(models.Model):
    id = models.AutoField(primary_key=True)

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='warranty_vendor')
    WARRANTY_CHOICES = (
        ('Replacement', 'Replacement'),
        ('Service', 'Service'),
        ('Other', 'Other'),
    )
    INTERVAL_CHOICES = (
        ('Day', 'Day'),
        ('Month', 'Month'),
        ('Year', 'Year'),
    )
    type = models.CharField(max_length=20, choices=WARRANTY_CHOICES)
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)
    limit = models.IntegerField(null=True, blank=True)
    conditions = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.type + self.interval + str(self.id))
        super(ProductWarranty, self).save(*args, **kwargs)

    def __str__(self):
        return self.type + '--' + self.interval + '--' + str(self.limit)


# product Information
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='product_vendor')
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    discounted_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )
    stock_quantity = models.IntegerField()
    sub_category = models.ForeignKey(
        ProductSubCategory,
        on_delete=models.CASCADE,
        related_name='product_sub_category',
        null=True
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='product_category',
        blank=True,
        null=True
    )
    alternative_names = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    description = models.TextField()
    warranty_id = models.ForeignKey(
        ProductWarranty,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True
    )
    warranty_limit = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=None,
        null=True,
        blank=True)
    additional_info = models.TextField(null=True)
    minimum_order_quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    maximum_order_quantity = models.IntegerField(validators=[MinValueValidator(1)], default=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    # for functioning search engine
    search_vector = SearchVectorField(null=True)

    objects = ProductManager()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, self.code)
        self.discounted_price = self.price

        self.search_vector = (
            SearchVector('name', weight='A')
            + SearchVector('alternative_names', weight='B')
            + SearchVector('category__name', weight='B')
        )

        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

    @property
    def is_available(self):
        if self.is_active & self.stock_quantity > 0:
            return True
        else:
            return False


# product Images
class ProductImages(models.Model):
    id = models.AutoField(primary_key=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images'
    )
    image = StdImageField(
        upload_to='images/product_images/',
        blank=True,
        null=True,
        editable=True,
        variations={'thumbnail': (220, 140)}, delete_orphans=True
    )


# product Purchased
class ProductPurchased(models.Model):
    id = models.AutoField(primary_key=True)

    batch_code = models.CharField(max_length=10, unique=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_purchased',
        null=True
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='product_purchased_vendor'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='product_purchased_supplier'
    )
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    purchase_date = models.DateField()
    additional_field = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.batch_code + self.product.code, self.supplier.supplier_name)
        self.selling_price = self.product.price
        super(ProductPurchased, self).save(*args, **kwargs)

    def __str__(self):
        return self.batch_code


# Product Review
class ProductReview(models.Model):
    id = models.AutoField(primary_key=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(User, on_delete=models.SET('Unknown'))
    review = models.CharField(max_length=150)
    is_active = models.CharField(max_length=150)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product.name + str(self.created))
        super(ProductReview, self).save(*args, **kwargs)


# discount
class Discount(models.Model):
    id = models.AutoField(primary_key=True)

    DISCOUNT_TYPE_CHOICES = (
        ('PERCENTAGE', 'Percentage'),
        ('AMOUNT', 'Fixed Amount'),
    )
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='product_discount'
    )
    conditions = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount_type = models.CharField(choices=DISCOUNT_TYPE_CHOICES, max_length=10)
    discount = models.IntegerField(
        validators=[MinValueValidator(0)]
    )

    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if self.discount_type == 'PERCENTAGE':
            Product.objects.filter(pk=self.product_id).update(discounted_price=self.discount)
            # p.discounted_price = p.price - self.discount
            # print(p.discounted_price)
            # p.save()
        #     self.product.discounted_price = self.product.price - (self.product.price*self.discount/100)
        # else:
        #     self.product.discounted_price = self.product.price - self.discount

        self.slug = slugify(self.product.name + str(self.created))
        super(Discount, self).save(*args, **kwargs)

    @property
    def is_valid(self):
        today = date.today()
        if self.is_active and today >= self.valid_from and today <= self.valid_to:
            return True
        return False


class PromoCode(models.Model):
    id = models.AutoField(primary_key=True)

    DISCOUNT_TYPE_CHOICES = (
        ('PERCENTAGE', 'Percentage'),
        ('AMOUNT', 'Fixed Amount'),
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='vendor_promo_codes'
    )
    code = models.CharField(
        max_length=50,
        unique=True
    )
    valid_from = models.DateField()
    valid_to = models.DateField()

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    limit = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.code = self.code.replace(' ', '')
        self.slug = slugify(self.code)
        super(PromoCode, self).save(*args, **kwargs)

    # checking for promo code validity
    @property
    def is_valid(self):
        today = date.today()
        if self.is_active and today >= self.valid_from and today <= self.valid_to:
            return True
        return False

    def __str__(self):
        return self.code
