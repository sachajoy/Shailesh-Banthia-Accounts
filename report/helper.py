from ledger import models
from django.db.models import Sum
from datetime import datetime

def client_trancation_details_selected_firm(client_id, user_id, firm_id, from_date, to_date):
    context = {}
    period = models.SelectedPeriod.objects.get(user_id=user_id)
    firms = models.Firm.objects.all()



    tranctions = models.Trancation.objects.filter(
        booking_date__gte=from_date,
        booking_date__lte=to_date
    )

    tranctions_agg = models.Trancation.objects.all()

    if client_id != "-1":
        client = models.Client.objects.get(pk=client_id)
        tranctions = tranctions.filter(client=client)
        tranctions_agg = tranctions.filter(client=client)
    
    if firm_id != "-1":
        firm = models.Firm.objects.get(pk=firm_id)
        tranctions = tranctions.filter(firm=firm)
        tranctions_agg = tranctions.filter(firm=firm)

    
    # from_date = datetime.strptime(from_date, "YYYY-mm-dd")

    opening_balance = tranctions_agg.filter(
        booking_date__lt=from_date
    ).aggregate(balance=Sum('amount'))

    print(opening_balance)

    closing_balance = tranctions_agg.filter(
        booking_date__lte=to_date
    ).aggregate(balance=Sum('amount'))

    payment = tranctions_agg.filter(
       booking_date__gte=from_date,
        booking_date__lte=to_date, amount__gt=0,
    ).aggregate(payment=Sum('amount'))

    recipt = tranctions_agg.filter(
        booking_date__gte=from_date,
        booking_date__lte=to_date, amount__lt=0, 
    ).aggregate(recipt=Sum('amount'))

    payment['payment'] = payment['payment'] if payment['payment'] else 0
    recipt['recipt'] = recipt['recipt'] if recipt['recipt'] else 0
    opening_balance['balance'] = opening_balance['balance'] if opening_balance['balance'] else 0
    closing_balance['balance'] = closing_balance['balance'] if closing_balance['balance'] else 0
    total_payment_due = payment['payment'] 
    total = payment['payment'] + recipt['recipt']
    # context['client'] = client
    context['tranctions'] = tranctions
    context['opening_balance'] = opening_balance['balance']
    context['closing_balance'] = closing_balance['balance']
    context['total_payment_due'] = total_payment_due
    context['recipt'] = recipt['recipt']
    context['total'] = total
    print(context)
    return context


