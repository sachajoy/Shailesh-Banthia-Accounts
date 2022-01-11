from django.views.generic import (
    CreateView, UpdateView, ListView,
    FormView
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .. import models


class FirmCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Firm
    fields = ['name', 'abs']
    permission_required = "ledger.add_firm"

    def handle_no_permission(self):
        return redirect('permission-denied')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


class FirmListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Firm
    context_object_name = 'firms'
    template_name = 'ledger/firm_list.html'
    permission_required = "ledger.view_firm"

    def handle_no_permission(self):
        return redirect('permission-denied')


class FirmUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Firm
    fields = ['name', 'abs']
    permission_required = "ledger.view_firm"

    def handle_no_permission(self):
        return redirect('permission-denied')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


@login_required
def select_firm(request):
    if request.method == 'POST':
        firm_id = request.POST.get('firm')
        if firm_id == 0 or firm_id == "0":
            request.session['firm_id'] = firm_id
            request.session['firm_name'] = "All Company"
            return redirect('ledger:index')
        firm_name = models.Firm.objects.get(pk=firm_id).name
        request.session['firm_id'] = firm_id
        request.session['firm_name'] = firm_name
        return redirect('ledger:index')
    firms = models.Firm.objects.all()
    return render(request, 'ledger/select_firm.html', {
        'firms': firms
    })
