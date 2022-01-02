from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.fields import SlugField
from django.shortcuts import reverse
class Firm(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    abs = models.CharField(max_length=40, unique=True, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def get_absolute_url(self):
        return reverse('ledger:list-firm')

    def __str__(self):
        return self.abs

class Client(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    address = models.TextField(null=True)
    mobile_number = models.CharField(max_length=11, null=False)
    intrest_status = models.BooleanField(default=False)
    intrest_rate = models.FloatField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def get_absolute_url(self):
        return reverse('ledger:detail-client')

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.mobile_number)


class SelectedPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return "{} to {}".format(self.start_date, self.end_date)

    def get_absolute_url(self):
        return reverse('ledger:is-period-set')

    # def clean(self, *args, **kwargs):
    #     # add custom validation here
    #     if self.start_date > self.end_date:
    #         raise ValueError("Start date is greater than end date.")
    #     return super().clean(*args, **kwargs)

    