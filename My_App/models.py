from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=200, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




class BoardingHouse(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    price = models.FloatField()
    phone = models.IntegerField(verbose_name='Contact Number')
    location = models.CharField(max_length=200)
    latitude = models.FloatField(verbose_name="Latitude", max_length=50, null=True, blank=True)
    longitude = models.FloatField(verbose_name="Longitude", max_length=50, null=True, blank=True)
    admin_approval = models.BooleanField(max_length=200, default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']




class Picture(models.Model):
    bh = models.ForeignKey(BoardingHouse, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='bh-images/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bh
