from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class RoomAsset(models.Model):
    asset_name = models.CharField(max_length=20, default='Not Specified')
    asset_type = models.CharField(max_length=20, default='Not Specified')
    url = models.URLField(null=True, blank=True)


class Room(models.Model):
    name = models.CharField(max_length=20, default="None submitted")
    floor = models.IntegerField()
    has_tv = models.BooleanField()
    assets = models.ForeignKey(RoomAsset, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    time = models.DateTimeField(default=now)
    duration = models.IntegerField(default=1)
    scheduler = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
