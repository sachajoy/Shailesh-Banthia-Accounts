import datetime

from django.db.models import Sum
from django.shortcuts import render
from ledger.models import Trancation, Client, SelectedPeriod, Firm
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from .helper import client_trancation_details_selected_firm

from datetime import datetime
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

class SelectTrancationForm(forms.Form):
    selected = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )

@login_required
def selected_trancations(request, client_id):
    print("selected entry")
    user_id = request.user.id
    period = SelectedPeriod.objects.get(pk=user_id)
    trancations = Trancation.objects.filter(client_id=client_id,
                                            booking_date__gte=period.start_date,
                                            booking_date__lte=period.end_date)
    firm_id = request.session.get("firm_id", 0)
    if firm_id != "0":
        trancations.filter(firm_id=firm_id)
    client = Client.objects.get(pk=client_id)
    if request.method == "POST":
        print("post")
        data =request.POST.getlist('selected')
        data = list(map(int, data))
        print(type(data))
        print(data)
        trancations = Trancation.objects.filter(id__in=data)
        total_due = 0
        total = 0
        total_rec = 0
        for tran in trancations:
            if tran.amount > 0:
                total_due += tran.amount
            total += tran.amount
        total_rec = total - total_due
        return render(request, "ledger/print_client_ledger.html", {
            "tranctions": trancations,
            "total_due": total_due,
            "total": total,
            "total_rec": total_rec
        })
    # print(trancations)
    return render(request, "report/select_trancation.html", {
        "tranctions": trancations,
        "client": client
    })

@login_required
def day_trancations(request):
    print("day report")
    user_id = request.user.id
    period = SelectedPeriod.objects.get(pk=user_id)
    error_in_date = 1
    trancations = Trancation.objects.filter(
        booking_date__gte=period.start_date,
                                            booking_date__lte=period.end_date)
    firm_id = request.session.get("firm_id", 0)
    clients = Client.objects.all()
    firms = Firm.objects.all()
    if firm_id != "0":
        trancations.filter(firm_id=firm_id)
    # client = Client.objects.get(pk=client_id)
    if request.method == "POST":
        # print("post")
        # data =request.POST.getlist('selected')
        date_from = request.POST.get('from')
        date_to = request.POST.get('to')
        client_requested = request.POST.get('client')
        firm_requested = request.POST.get('firm')
        
        error_in_date = 1
        if datetime.strptime(date_from, "%Y-%m-%d") > datetime.strptime(date_to, "%Y-%m-%d"):
            error_in_date = 0
            # print("error in date")
        # print(date_from)
        # print(date_to)
        trancations = Trancation.objects.filter(booking_date__gte=date_from,
                                            booking_date__lte=date_to)
        if client_requested != "-1":
            client = Client.objects.get(pk=client_requested)
            trancations = trancations.filter(client=client)
            
        if firm_requested != "-1":
            firm = Firm.objects.get(pk=firm_requested)
            trancations = trancations.filter(firm=firm)
       
        context = client_trancation_details_selected_firm(client_requested, request.user.id, firm_requested, date_from, date_to)
        # print(trancations)
        return render(request, "report/day_report.html", {
            "tranctions": trancations,
            "error_in_date": error_in_date,
            "client_id": int(client_requested),
            "firm_id": int(firm_requested),
            "clients": clients,
            "from_date": date_from,
            "to_date": date_to,
            "firms" : firms,
            "context": context
        })
    # print(trancations)
    return render(request, "report/day_report.html", {
        "error_in_date": error_in_date,
        "client_id": "-1",
        "clients": clients,
        "firms" : firms
    })

