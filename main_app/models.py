from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


# class Profile (models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()


class Hike (models.Model):
    name = models.CharField(max_length=200)
    coord = models.CharField(max_length=200)
    length = models.CharField(max_length=200)
    gain = models.CharField(max_length=200)
    highPoint = models.CharField(max_length=200)
    PugetSound = 'PS'
    NorthCascades = 'NC'
    CenteralWA = 'CW'
    SouthCascades = 'SC'
    EasternWA = 'EW'
    region_choices = [
        (PugetSound, 'Puget Sound'),
        (NorthCascades, 'North Cascades'),
        (CenteralWA, 'Centeral Washington'),
        (SouthCascades, 'South Cascades'),
        (EasternWA, 'Eastern Washington'),
    ]
    hike_region = models.CharField(
        max_length=2,
        choices=region_choices,
        default=PugetSound)
    image = models.FileField(upload_to='static/css/resources')
    description = models.CharField(max_length=5000, default=None)
    directions = models.CharField(max_length=5000)

    def __str__(self):
        return f"{self.name}"


class Report (models.Model):
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1500)
    hikeType = models.CharField(max_length=50)
    conditions = models.CharField(max_length=50)
    road = models.CharField(max_length=50)
    bugs = models.CharField(max_length=50)
    snow = models.CharField(max_length=50)
    image = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user}"


class Photo(models.Model):
    url = models.CharField(max_length=200)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"User Report photo: {self.profile_id} @{self.url}"
