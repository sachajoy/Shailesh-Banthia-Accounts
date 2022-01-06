from django.forms import ModelForm
from . import models
from django.core.exceptions import ValidationError


class TrancationForm(ModelForm):
    class Meta:
        model = models.Trancation
        fields = [
            'amount', 'sector', 'date', 'remarks',
            'firm', 'booking_date', 'passenger_list',
        ]

    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    def clean_booking_date(self):
        print("clean_booking_date invoked")
        date = self.cleaned_data['booking_date']
        period = models.SelectedPeriod.objects.get(
            user_id=self.user_id
        )
        print(type(date))
        print(type(period.end_date))
        if date > period.end_date:
            print("caught end booking date")
            raise ValidationError("Date is Not between the set peroid")
        if date < period.start_date:
            print("caught start booking date")
            raise ValidationError("Date is Not between the set peroid")

        return date
