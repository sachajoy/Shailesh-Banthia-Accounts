from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .. import models

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = models.Client
    fields = ['name', 'mobile_number', 'intrest_status', 'intrest_rate', 'address']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ledger:detail-client', kwargs= {
            'pk':self.object.id,
        })

class ClientDetialView(LoginRequiredMixin, DetailView):
    model = models.Client
    template_name = 'ledger/client_details.html'
    context_object_name = 'client'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Client
    fields = ['name', 'mobile_number', 'intrest_status', 'intrest_rate', 'address']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ledger:detail-client', kwargs= {
            'pk':self.get_object().id,
        })