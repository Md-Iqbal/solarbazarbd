from django.db import models


# Create your models here.
from djrichtextfield.models import RichTextField


class AboutUs(models.Model):
    about_us_title = models.CharField(max_length=300, null=True)
    about_us_text = models.TextField(null=True)
    aboutus_image = models.ImageField(upload_to="images/static_images/", null=True)
    why_choose_product = models.TextField(null=True)
    why_choose_product_image = models.ImageField(upload_to="images/static_images/", null=True)
    vision = models.TextField(null=True)
    vision_image = models.ImageField(upload_to="images/static_images/", null=True)
    mission = models.TextField(null=True)
    mission_image = models.ImageField(upload_to="images/static_images/", null=True)

    def __str__(self):
        return self.about_us_title


class SpecialTeam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    designation = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to="images/member_images/")
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.CharField(max_length=200, null=True)
    answer = models.TextField()

    def __str__(self):
        return self.question


class CompanyPolicy(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = RichTextField()

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    leave_message = models.TextField(null=True)
    address = models.CharField(max_length=300, null=True)
    phone1 = models.CharField(max_length=100, null=True)
    phone2 = models.CharField(max_length=100, null=True)
    phone3 = models.CharField(max_length=100, null=True)
    email1 = models.CharField( max_length=150, null=True)
    email2 = models.CharField( max_length=150, null=True)
    email3 = models.CharField( max_length=150, null=True)
    opening_hours = models.CharField(max_length=200, null=True)
    careers = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.email1
