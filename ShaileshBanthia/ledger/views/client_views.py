from django.views.generic import (
    CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .. import models

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = models.Client
    fields = ['name', 'mobile_number', 'intrest_status', 'intrest_rate', 'address']

    def form_valid(self, form):
        form.created_by = self.request.user
        return super().form_valid(form)