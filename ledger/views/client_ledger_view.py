from django.views import generic
from .. import models
from django.contrib.auth import mixins
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
