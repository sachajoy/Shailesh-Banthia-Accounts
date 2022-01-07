from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.views.generic import (
    UpdateView,
    CreateView,
    DeleteView
)
from .. import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .. import models
from .helper_functions import (
    client_trancation_details_selected_firm,
    client_trancation_detial_all_company
)

class ClientDetailTranctionCreateListView(LoginRequiredMixin, CreateView):
    model = models.Trancation
    form_class = forms.TrancationForm
    template_name = 'ledger/client_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.kwargs.get('client_id')
        user_id = self.request.user.pk
        firm_id = self.request.session['firm_id']
        if firm_id != "0":
            context.update(client_trancation_details_selected_firm(
                client_id=client_id, user_id=user_id, firm_id=firm_id
            ))
            print(context)
            return context
        context.update(client_trancation_detial_all_company(client_id, user_id))
        return context


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientDetailTranctionCreateListView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = models.Client.objects.get(pk=self.kwargs['client_id'])
        self.object.created_by = self.request.user
        return super(ClientDetailTranctionCreateListView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ledger:detail-client', kwargs={
            'client_id': self.kwargs['client_id']
        })


class ClientDetailTranctionUpdateListView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ['ledger.change_trancation']
    redirect_field_name = reverse_lazy('permission-denied')
    model = models.Trancation
    form_class = forms.TrancationForm
    template_name = 'ledger/client_details.html'

    def handle_no_permission(self):
        return redirect('permission-denied')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.kwargs.get('client_id')
        user_id = self.request.user.pk
        firm_id = self.request.session['firm_id']
        if firm_id != "0":
            context.update(client_trancation_details_selected_firm(
                client_id=client_id, user_id=user_id, firm_id=firm_id
            ))
            print(context)
            return context
        context.update(client_trancation_detial_all_company(client_id, user_id))
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

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientDetailTranctionUpdateListView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        return kwargs


class ClientTranctionDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Trancation
    context_object_name = 'trancation'

    def get_success_url(self):
        return reverse_lazy('ledger:detail-client', kwargs={
            'client_id': self.kwargs['client_id']
        })
