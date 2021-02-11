from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Report, Hike

# Register your models here.

admin.site.register(Hike)

admin.site.register(Report)
