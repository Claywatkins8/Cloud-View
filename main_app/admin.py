from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Report, Hike, userPhoto, hikePhoto, reportPhoto

# Register your models here.

admin.site.register(Hike)

admin.site.register(Report)

admin.site.register(userPhoto)
admin.site.register(hikePhoto)
admin.site.register(reportPhoto)
