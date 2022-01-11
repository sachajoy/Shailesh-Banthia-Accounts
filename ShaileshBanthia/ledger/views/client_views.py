from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView
)

from .. import models


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Client
    fields = ['name', 'mobile_number', 'intrest_status', 'intrest_rate', 'address']
    permission_required = 'ledger.add_client'

    def handle_no_permission(self):
        return redirect('permission-denied')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ledger:detail-client', kwargs={
            'client_id': self.object.id,
        })


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Client
    fields = ['name', 'mobile_number', 'intrest_status', 'intrest_rate', 'address']
    permission_required = 'ledger.change_client'


    def handle_no_permission(self):
        return redirect('permission-denied')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ledger:detail-client', kwargs={
            'pk': self.get_object().id,
        })

    def get_redirect_field_name(self):
        return reverse('permission-denied')
