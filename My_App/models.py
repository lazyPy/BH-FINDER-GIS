from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.name)


class BoardingHouse(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    avail_room = models.IntegerField()
    phone = models.CharField(verbose_name='Contact Number', max_length=200)
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

    def __str__(self):
        return str(self.bh)


class Session(models.Model):
    session_id = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.session_id)


class Message(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    bh = models.ForeignKey(BoardingHouse, on_delete=models.CASCADE)
    body = models.TextField()
    session = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
