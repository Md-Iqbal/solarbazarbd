from django.db import models
from django.conf import settings
from stdimage import StdImageField

User = settings.AUTH_USER_MODEL
# Create your models here.


class BusinessAgentProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_user', blank=True, null=True)
    business_center_id = models.CharField(max_length=50, null=True)
    reference_code = models.CharField(max_length=50, null=True)
    full_name = models.CharField(max_length=50, null=True)
    father_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)
    confirm_password = models.CharField(max_length=20, null=True)
    profile_image = models.ImageField(
        upload_to='images/agent_images/',
        blank=True,
        null=True,
        editable=True,
    )

    nid_front = models.ImageField(
        upload_to='images/agent_images/',
        blank=True,
        null=True,
        editable=True,
    )
    nid_back = models.ImageField(
        upload_to='images/agent_images/',
        blank=True,
        null=True,
        editable=True,
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Disabled', 'Disabled'),
        ('Pending', 'Pending'),
        ('Declined', 'Declined'),
        ('Blocked', 'Blocked')
    )

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')

    account_number = models.CharField(max_length=150)
    account_name = models.CharField(max_length=150)
    bank_name = models.CharField(max_length=150)
    account_holder_name = models.CharField(max_length=150, null=True, blank=True)
    branch_name = models.CharField(max_length=150)
    branch_address = models.CharField(max_length=150, null=True, blank=True)
    type_of_account = models.CharField(max_length=50, null=True, blank=True)
    routing_no = models.CharField(max_length=50, null=True, blank=True)
    cheque_img = models.ImageField(
        upload_to='media/images/vendor_images/cheque/',
        blank=True,
        null=True,
        editable=True,
    )

    def __str__(self):
        return self.full_name


