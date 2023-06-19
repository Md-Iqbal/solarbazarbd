from django.db import models


class StaticFiles(models.Model):
    title = models.CharField(max_length=150, unique=True)
    image1 = models.ImageField(
        upload_to='images/static_images/',
        blank=True,
        null=True,
        editable=True,

    )
    image2 = models.ImageField(
        upload_to='images/static_images/',
        blank=True,
        null=True,
        editable=True,

    )
    image3 = models.ImageField(
        upload_to='images/static_images/',
        blank=True,
        null=True,
        editable=True,

    )
    link = models.CharField(max_length=120, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MainSlider(models.Model):
    title = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=200, null=True,blank=True)
    image = models.ImageField(
        upload_to='images/static_images/',
        blank=True,
        null=True,
        editable=True,

    )
    link = models.CharField(max_length=120, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





