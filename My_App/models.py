from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=200, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.name)


class BoardingHouse(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    price = models.FloatField()
    phone = models.IntegerField(verbose_name='Contact Number', validators=[MaxValueValidator(11), MinValueValidator(1)])
    location = models.CharField(max_length=200)
    latitude = models.FloatField(verbose_name="Latitude", max_length=50, null=True, blank=True)
    longitude = models.FloatField(verbose_name="Longitude", max_length=50, null=True, blank=True)
    admin_approval = models.BooleanField(max_length=200, default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.name)


class Picture(models.Model):
    bh = models.ForeignKey(BoardingHouse, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='bh-images/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bh)
