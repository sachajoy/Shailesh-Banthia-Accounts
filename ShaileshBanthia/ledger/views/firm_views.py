from django.views.generic import (
    CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import models

class FirmCreateView(LoginRequiredMixin, CreateView):
    model = models.Firm
    fields = ['name', 'abs']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)