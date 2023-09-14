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
        self.request.session['client_id'] = -1
        print('Client ID: ')
        print(self.request.session['client_id'])
        user = self.request.user
        try:
            firm_id = self.request.session['firm_id']
        except KeyError as e:
            firm_id = '0'
        period = models.SelectedPeriod.objects.get(user_id=user.id)
        client = models.Client.objects.all()
        # if firm_id != '0':
        #     client = client.filter(trancation__firm_id = firm_id)
        for c in client:
            if firm_id != '0':
                c.val = models.Trancation.objects.filter(
                    client__id=c.id, booking_date__lte=period.end_date, firm_id=firm_id
                ).aggregate(total=Sum('amount'))['total']
            else:
                c.val = models.Trancation.objects.filter(
                    client__id=c.id, booking_date__lte=period.end_date
                ).aggregate(total=Sum('amount'))['total']
            # print(c.trancation__amount['total'])
        if firm_id != '0':
            total = models.Client.objects.filter(trancation__booking_date__lte=period.end_date, 
                trancation__firm_id=firm_id).annotate(
                val=Sum('trancation__amount')
            ).aggregate(total=Sum('val'))
        else:
            total = models.Client.objects.filter(trancation__booking_date__lte=period.end_date).annotate(
                val=Sum('trancation__amount')
            ).aggregate(total=Sum('val'))

        firm_details = models.Trancation.objects.filter(
                    booking_date__lte=period.end_date
                )
        # print(firm_details)
        firm_detail = firm_details.values('firm__name').annotate(sum=Sum('amount'))

        # print(firm_detail)

        # for firm in firm_detail:
            # print(firm.values)
            # print(firm)

        return {'clients':client, 'total':total, 'firm_details': firm_detail}

@login_required
def access_denid(request):
    return render(request, 'acces_denid.html')