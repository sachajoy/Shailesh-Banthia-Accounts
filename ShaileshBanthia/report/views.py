import datetime

from django.db.models import Sum
from django.shortcuts import render
from ledger.models import Trancation, Client, SelectedPeriod
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def intrest_statement(request, client_id):
    user_id = request.user.id
    period = SelectedPeriod.objects.get(pk=user_id)
    trancations = Trancation.objects.filter(client_id=client_id,
                                            booking_date__gte=period.start_date,
                                            booking_date__lte=period.end_date)
    firm_id = request.session.get("firm_id", 0)
    if firm_id != "0":
        trancations.filter(firm_id=firm_id)
        opening_balance = Trancation.objects.filter(client_id=client_id,
                                                    booking_date__lt=period.start_date,
                                                    firm_id=firm_id).aggregate(balance=Sum('amount'))
    else:
        opening_balance = Trancation.objects.filter(client_id=client_id,
                                                    booking_date__lt=period.start_date).aggregate(
            balance=Sum('amount'))
    opening_balance = opening_balance['balance'] if opening_balance['balance'] else 0
    client = Client.objects.get(pk=client_id)
    intrest_rate = client.intrest_rate
    balance = opening_balance
    intrest_days = client.intrest_day
    total_intrest = 0
    count = trancations.count()
    for trancation in trancations:
        trancation.balance = balance + trancation.amount
        balance += trancation.amount
        trancation.end_date = trancation.booking_date
    opening_intrest = {
        'balance': opening_balance,
        'start_date':period.start_date,
        'end_date':period.end_date,
        'intrest':0,
        'amount':opening_balance
    }
    closing_intrest = {
        'balance': opening_balance,
        'start_date': period.start_date,
        'end_date': period.end_date,
        'intrest': 0,
        'amount': opening_balance,
        'days': 0
    }
    for i in range(0, count):
        if i == 0:
            opening_intrest['end_date'] = trancations[i].booking_date
            opening_intrest['days'] = abs((opening_intrest['start_date'] - opening_intrest['end_date']).days)
            opening_intrest['intrest'] = round((opening_intrest['balance'] * opening_intrest['days'] * intrest_rate) / 36500)
            trancations[i].end_date = trancations[i + 1].booking_date
            total_intrest += opening_intrest['intrest']
        elif i == count-1:
            trancations[i].end_date = period.end_date
        else:
            trancations[i].end_date = trancations[i+1].booking_date
        trancations[i].days = abs((trancations[i].booking_date - trancations[i].end_date).days)
        trancations[i].intrest = round((trancations[i].days * trancations[i].balance * intrest_rate) / 36500)
        total_intrest += trancations[i].intrest


    return render(request, 'report/intrest_statement.html', {
        'trancations': trancations,
        'client': client,
        'tran_last': trancations.last(),
        'opening_intest': opening_intrest,
        'total_intrest': total_intrest
    })
