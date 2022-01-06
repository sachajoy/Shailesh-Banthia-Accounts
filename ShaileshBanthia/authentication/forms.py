from django.contrib.auth.forms import UserCreationForm
from authentication.models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'name', 'email', 'mob_no'
        )