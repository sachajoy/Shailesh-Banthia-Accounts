from .. import  models
from django.db.models import Sum
def client_trancation_details_selected_firm(client_id, user_id, firm_id):
    context = {}
    client = models.Client.objects.get(pk=client_id)
    period = models.SelectedPeriod.objects.get(user_id=user_id)
    tranctions = models.Trancation.objects.filter(
        client=client, booking_date__gte=period.start_date,
        booking_date__lte=period.end_date, firm_id=firm_id
    ).order_by('-booking_date')
    opening_balance = models.Trancation.objects.filter(
        client=client, booking_date__lt=period.start_date, firm_id=firm_id
    ).aggregate(balance=Sum('amount'))

    closing_balance = models.Trancation.objects.filter(
        client=client, booking_date__lte=period.end_date, firm_id=firm_id
    ).aggregate(balance=Sum('amount'))

    payment = models.Trancation.objects.filter(
        client=client, booking_date__gte=period.start_date,
        booking_date__lte=period.end_date, amount__gt=0, firm_id=firm_id
    ).aggregate(payment=Sum('amount'))

    recipt = models.Trancation.objects.filter(
        client=client, booking_date__gte=period.start_date,
        booking_date__lte=period.end_date, amount__lt=0, firm_id=firm_id
    ).aggregate(recipt=Sum('amount'))

    payment['payment'] = payment['payment'] if payment['payment'] else 0
    recipt['recipt'] = recipt['recipt'] if recipt['recipt'] else 0
    opening_balance['balance'] = opening_balance['balance'] if opening_balance['balance'] else 0
    closing_balance['balance'] = closing_balance['balance'] if closing_balance['balance'] else 0
    total_payment_due = payment['payment'] + opening_balance['balance']
    total = payment['payment'] + opening_balance['balance'] + recipt['recipt']
    context['client'] = client
    context['tranctions'] = tranctions
    context['opening_balance'] = opening_balance['balance']
    context['closing_balance'] = closing_balance['balance']
    context['total_payment_due'] = total_payment_due
    context['total'] = total
    return context

def client_trancation_detial_all_company(client_id, user_id):
    context = {}
    client = models.Client.objects.get(pk=client_id)
    period = models.SelectedPeriod.objects.get(user_id=user_id)
    tranctions = models.Trancation.objects.filter(
        client=client, booking_date__gte=period.start_date,
        booking_date__lte=period.end_date
    )
    opening_balance = models.Trancation.objects.filter(
        client=client, booking_date__lt=period.start_date
    ).aggregate(balance=Sum('amount'))
    closing_balance = models.Trancation.objects.filter(
        client=client, booking_date__lte=period.end_date
    ).aggregate(balance=Sum('amount'))
    payment = models.Trancation.objects.filter(
        client=client, booking_date__gte=period.start_date,
        booking_date__lte=period.end_date, amount__gt=0
    ).aggregate(payment=Sum('amount'))
    recipt = models.Trancation.objects.filter(
        client=client, booking_date__gte=period.start_date,
        booking_date__lte=period.end_date, amount__lt=0,
    ).aggregate(recipt=Sum('amount'))


    payment['payment'] = payment['payment'] if payment['payment'] else 0
    recipt['recipt'] = recipt['recipt'] if recipt['recipt'] else 0
    opening_balance['balance'] = opening_balance['balance'] if opening_balance['balance'] else 0
    closing_balance['balance'] = closing_balance['balance'] if closing_balance['balance'] else 0
    total_payment_due = payment['payment'] + opening_balance['balance']
    total = payment['payment'] + opening_balance['balance'] + recipt['recipt']
    context['client'] = client
    context['tranctions'] = tranctions
    context['opening_balance'] = opening_balance['balance']
    context['closing_balance'] = closing_balance['balance']
    context['total_payment_due'] = total_payment_due
    context['total'] = total
    return context