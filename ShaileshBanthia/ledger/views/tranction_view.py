from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    UpdateView,
    CreateView,
    DeleteView,
    ListView
)
from django.http import JsonResponse
from .. import forms
from django.urls import reverse_lazy
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


class ClientTranctionDeleteView(LoginRequiredMixin, PermissionRequiredMixin,  DeleteView):
    model = models.Trancation
    context_object_name = 'trancation'
    permission_required = "ledger.delete_trancation"

    def handle_no_permission(self):
        return redirect('permission-denied')

    def get_success_url(self):
        return reverse_lazy('ledger:detail-client', kwargs={
            'client_id': self.kwargs['client_id']
        })

class TrancationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Trancation
    permission_required = 'ledger.view_ledger'
    template_name = 'ledger/all_trancation.html'


    def handle_no_permission(self):
        return redirect('permission-denied')

    def get_queryset(self):
        period = models.SelectedPeriod.objects.get(pk=self.request.user.id)
        queryset =models.Trancation.objects.filter(booking_date__gte=period.start_date, booking_date__lte=period.end_date)
        return queryset


@login_required
def verfiy_entry(request, client_id):
    if request.method == 'POST':
        trancation_id = request.POST.get('trancation_id')
        print("Trancation ID:" + trancation_id)
        trancation = models.Trancation.objects.get(pk=trancation_id)
        trancation.verifed = not trancation.verifed
        trancation.save()
        return JsonResponse({'result': trancation.verifed})
    return JsonResponse({'result':'Did not get id'})

