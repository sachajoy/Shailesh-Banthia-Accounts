from django.views.generic import (
    CreateView, UpdateView, ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import models

class FirmCreateView(LoginRequiredMixin, CreateView):
    model = models.Firm
    fields = ['name', 'abs']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FirmListView(LoginRequiredMixin, ListView):
    model = models.Firm
    context_object_name = 'firms'
    template_name = 'ledger/firm_list.html'


class FirmUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Firm
    fields = ['name', 'abs']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)