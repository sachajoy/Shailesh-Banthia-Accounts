from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import (
    UpdateView,
    CreateView,
    DeleteView
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from .. import models


class ClientDetailTranctionCreateListView(LoginRequiredMixin, CreateView):
    model = models.Trancation
    fields = [
        'sector', 'amount',
        'remarks', 'date',
        'booking_date', 'passenger_list',
        'firm'
    ]
    template_name = 'ledger/client_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = models.Client.objects.get(pk=self.kwargs.get('client_id'))
        print(client.id)
        period = models.SelectedPeriod.objects.get(user=self.request.user)
        tranctions = models.Trancation.objects.filter(
            client=client, booking_date__gte=period.start_date,
            booking_date__lte=period.end_date
        )
        opening_balance = models.Trancation.objects.filter(
            client=client, booking_date__lt=period.start_date
        ).aggregate(balance=Sum('amount'))
        closing_balance = models.Trancation.objects.filter(
            client=client, booking_date__lte=period.end_date
        ).aggregate(balance=Sum('amount'))
        payment = models.Trancation.objects.filter(
            client=client, booking_date__gte=period.start_date,
            booking_date__lte=period.end_date, amount__gt=0
        ).aggregate(payment=Sum('amount'))
        recipt = models.Trancation.objects.filter(
            client=client, booking_date__gte=period.start_date,
            booking_date__lte=period.end_date, amount__lt=0
        ).aggregate(recipt=Sum('amount'))
        payment['payment'] = payment['payment'] if payment['payment'] else 0
        recipt['recipt'] = recipt['recipt'] if recipt['recipt'] else 0
        opening_balance['balance'] = opening_balance['balance'] if opening_balance['balance'] else 0
        closing_balance['balance'] = closing_balance['balance'] if closing_balance['balance'] else 0
        total_payment_due = payment['payment'] + opening_balance['balance']
        total = payment['payment'] + opening_balance['balance'] + recipt['recipt']
        context['client'] = client
        context['tranctions'] = tranctions
        context['opening_balance'] = opening_balance['balance']
        context['closing_balance'] = closing_balance['balance']
        context['total_payment_due'] = total_payment_due
        context['total'] = total
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = models.Client.objects.get(pk=self.kwargs['client_id'])
        self.object.created_by = self.request.user
        return super(ClientDetailTranctionCreateListView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ledger:detail-client', kwargs={
            'client_id': self.kwargs['client_id']
        })

class ClientDetailTranctionUpdateListView(LoginRequiredMixin, UpdateView):
    model = models.Trancation
    fields = [
        'sector', 'amount',
        'remarks', 'date',
        'booking_date', 'passenger_list',
        'firm'
    ]
    template_name = 'ledger/client_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = models.Client.objects.get(pk=self.kwargs.get('client_id'))
        print(client.id)
        period = models.SelectedPeriod.objects.get(user=self.request.user)
        tranctions = models.Trancation.objects.filter(
            client=client, booking_date__gte=period.start_date,
            booking_date__lte=period.end_date
        )
        opening_balance = models.Trancation.objects.filter(
            client=client, booking_date__lt=period.start_date
        ).aggregate(balance=Sum('amount'))
        closing_balance = models.Trancation.objects.filter(
            client=client, booking_date__lte=period.end_date
        ).aggregate(balance=Sum('amount'))
        payment = models.Trancation.objects.filter(
            client=client, booking_date__gte=period.start_date,
            booking_date__lte=period.end_date, amount__gt=0
        ).aggregate(payment=Sum('amount'))
        recipt = models.Trancation.objects.filter(
            client=client, booking_date__gte=period.start_date,
            booking_date__lte=period.end_date, amount__lt=0
        ).aggregate(recipt=Sum('amount'))
        payment['payment'] = payment['payment'] if payment['payment'] else 0
        recipt['recipt'] = recipt['recipt'] if recipt['recipt'] else 0
        opening_balance['balance'] = opening_balance['balance'] if opening_balance['balance'] else 0
        closing_balance['balance'] = closing_balance['balance'] if closing_balance['balance'] else 0
        total_payment_due = payment['payment'] + opening_balance['balance']
        total = payment['payment'] + opening_balance['balance'] + recipt['recipt']
        context['client'] = client
        context['tranctions'] = tranctions
        context['opening_balance'] = opening_balance['balance']
        context['closing_balance'] = closing_balance['balance']
        context['total_payment_due'] = total_payment_due
        context['total'] = total
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = models.Client.objects.get(pk=self.kwargs['client_id'])
        self.object.created_by = self.request.user
        return super(ClientDetailTranctionUpdateListView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ledger:detail-client', kwargs={
            'client_id': self.kwargs['client_id']
        })

class ClientTranctionDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Trancation
    context_object_name = 'trancation'
    def get_success_url(self):
        return reverse_lazy('ledger:detail-client', kwargs={
            'client_id': self.kwargs['client_id']
        })