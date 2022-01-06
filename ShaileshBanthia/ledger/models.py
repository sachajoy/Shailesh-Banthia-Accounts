from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        return reverse('ledger:detail-client', kwargs={
            'pk': self.kwargs['pk']
        })

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

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(_("End Date cannot be less than Start Date"))


class Trancation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sector = models.CharField(null=False, max_length=100)
    amount = models.IntegerField(null=False)
    remarks = models.TextField(null=True, blank=True)
    date = models.TextField()
    booking_date = models.DateField()
    passenger_list = models.TextField(null=True)
    verifed = models.BooleanField(default=False)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE, default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    class Meta:
        ordering = ['booking_date']

    def __str__(self):
        return "{} - {}".format(self.client, self.date)

    def get_absolute_url(self):
        return reverse('ledger:detail-client', kwargs={
            'client_id': self.client_id
        })

