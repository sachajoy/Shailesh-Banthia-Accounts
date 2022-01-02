from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .. import models
class DashboardListView(LoginRequiredMixin, ListView):
    model = models.Client
    template_name = 'ledger/dashboard.html'
    context_object_name = 'clients'