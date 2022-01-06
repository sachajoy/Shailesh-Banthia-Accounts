from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.core.serializers import serialize
from .. import models


@login_required
def is_date_set(request):
    selected_peroid_record = models.SelectedPeriod.objects.filter(
        user_id=request.user.id)
    print(selected_peroid_record)
    if len(selected_peroid_record) != 1:
        return redirect('ledger:create-period')
    start_date = selected_peroid_record[0].start_date
    end_date = selected_peroid_record[0].end_date
    end_date = selected_peroid_record[0].end_date
    request.session["start_date"] = start_date.strftime('%b %d, %Y')
    request.session["end_date"] = end_date.strftime('%b %d, %Y')
    request.session["firm_id"] = 0
    request.session["firm_name"] = "All Company"
    request.session.set_expiry(0)
    return redirect('ledger:index')


class SelectPeriodUpdateView(LoginRequiredMixin, UpdateView):
    model = models.SelectedPeriod
    fields = ['start_date', 'end_date']
    template_name = 'ledger/set_period.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, user=self.kwargs['pk'])

class SelectPeriodCreateView(LoginRequiredMixin, CreateView):
    model = models.SelectedPeriod
    fields = ['start_date', 'end_date']
    template_name = 'ledger/set_period.html'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)