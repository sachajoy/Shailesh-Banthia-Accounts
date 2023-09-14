from django.views import generic
from .. import models
from django.contrib.auth import mixins
from django.db.models import Sum
from django.shortcuts import redirect
from .helper_functions import (
    client_trancation_detial_all_company,
    client_trancation_details_selected_firm
)


class ClientLedgerListView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    generic.ListView,
):
    model = models.Trancation
    # context_object_name = 'trancations'
    permission_required = "ledger.view_ledger"

    def handle_no_permission(self):
        return redirect("permission-denied")

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.kwargs.get('client_id')
        self.request.session['client_id'] = client_id
        user_id = self.request.user.pk
        firm_id = self.request.session['firm_id']
        if firm_id != "0":
            context.update(client_trancation_details_selected_firm(
                client_id=client_id, user_id=user_id, firm_id=firm_id
            ))
        else:
            context.update(client_trancation_detial_all_company(client_id, user_id))
        trancations = context['tranctions']
        balance = context['opening_balance']
        for tran in trancations:
            tran.balance = balance + tran.amount
            balance = tran.balance
        context['tranctions'] = trancations
        return context


class ClientLedgerPrintListView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    generic.ListView,
):
    model = models.Trancation
    template_name = 'ledger/print_client_ledger.html'
    permission_required = 'ledger.view_ledger'

    def handle_no_permission(self):
        return redirect('permission-denied')

    def get_context_data(self, *, object_list=None, **kwargs):
        client_id = self.kwargs.get('client_id')
        self.request.session['client_id'] = client_id
        trancation_id = self.kwargs.get('trancation_id')
        firm_id = self.request.session['firm_id']
        trancation = models.Trancation.objects.get(pk=trancation_id)
        user = self.request.user
        period = models.SelectedPeriod.objects.get(user_id=user.id)
        trancations = models.Trancation.objects.filter(
            client_id=client_id, booking_date__gte=trancation.booking_date,
            booking_date__lte=period.end_date
        )
        opening_balance = models.Trancation.objects.filter(
            client_id=client_id, booking_date__lt=trancation.booking_date
        ).aggregate(opening_balance=Sum('amount'))

        if firm_id != "0":
            trancations = trancations.filter(firm_id=firm_id)
            opening_balance = models.Trancation.objects.filter(
                client_id=client_id, booking_date__lt=trancation.booking_date,
                firm_id=firm_id
            ).aggregate(opening_balance=Sum('amount'))
        total_positive = trancations.filter(amount__gte=0).aggregate(total=Sum('amount'))
        total_negative = trancations.filter(amount__lte=0).aggregate(total=Sum('amount'))
        context = {
            'opening_balance': opening_balance['opening_balance'] if opening_balance['opening_balance'] else 0,
            'total_due': total_positive['total'] if total_positive['total'] else 0,
            'total_rec': total_negative['total'] if total_negative['total'] else 0,
            'tranctions': trancations,
        }

        firm_details = models.Trancation.objects.filter(
        client__id=client_id, booking_date__gte=period.start_date,
        booking_date__lte=period.end_date).values('firm__name').annotate(sum=Sum('amount'))

        context['period'] = period
        if context['opening_balance'] > 0:
            context['total_due'] += context['opening_balance']
        else:
            context['total_rec'] += context['opening_balance']
        context['total'] = context['total_due'] + context['total_rec']
        context['logo'] = self.kwargs.get('logo')
        context['name'] = self.kwargs.get('name')
        context['period'] = self.kwargs.get('period')
        context['booking'] = self.kwargs.get('booking')
        context['firm'] = self.kwargs.get('firm')
        context['firm_show'] = self.kwargs.get('firm_show')
        context['firm_details'] = firm_details
        
        return context
