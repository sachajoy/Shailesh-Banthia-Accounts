from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import models

class DashboardListView(LoginRequiredMixin, ListView):
    model = models.Firm
    template_name = 'ledger/dashboard.html'
    context_object_name = 'firms'