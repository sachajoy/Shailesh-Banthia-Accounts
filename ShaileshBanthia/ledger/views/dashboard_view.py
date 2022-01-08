from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models import Count
from .. import models
class DashboardListView(LoginRequiredMixin, ListView):
    model = models.Client
    template_name = 'ledger/dashboard.html'
    context_object_name = 'clients'

    def get_context_data(self, *, object_list=None, **kwargs):
        client = models.Client.objects.annotate(
            val=Sum('trancation__amount')
        )
        total = client.aggregate(total=Sum('val'))
        return {'clients':client, 'total':total}

@login_required
def access_denid(request):
    return render(request, 'acces_denid.html')