from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(BoardingHouse)
admin.site.register(Picture)
admin.site.register(Session)
admin.site.register(Message)
