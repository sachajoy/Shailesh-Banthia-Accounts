from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
class Firm(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    abs = models.CharField(max_length=40, unique=True, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, default=1)

    def get_absolute_url(self):
        return reverse('ledger:list-firm')

    def __str__(self):
        return self.abs

class Client(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    address = models.TextField(null=True)
    mobile_number = models.CharField(max_length=11, unique=True, null=False)
    _intrest_status = models.BooleanField(default=False)
    intrest_rate = models.FloatField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, default=1)

    def get_absolute_url(self):
        return reverse('ledger:index')

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.mobile_number)

    