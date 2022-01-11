from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
)
from django.contrib.auth.models import Permission
from authentication.models import User
from django.forms import CheckboxSelectMultiple, ModelMultipleChoiceField


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'name', 'email', 'mob_no'
        )


class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CustomUserChangeForm(UserChangeForm):
    user_permissions = MyModelMultipleChoiceField(Permission.objects.exclude(
        content_type__app_label__in=['auth', 'admin', 'sessions', 'users', 'contenttypes']
    ).exclude(content_type__model__in=['selectedperiod', 'selectedfirm', 'user']), widget=CheckboxSelectMultiple)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('name', 'username', 'email', 'mob_no',
                  'is_active', 'is_superuser', 'user_permissions')

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'class': 'form-control',
            }
        )
        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control',
            }
        )
        self.fields['mob_no'].widget.attrs.update(
            {
                'class': 'form-control',
            }
        )

        self.fields['is_active'].widget.attrs.update(
            {
                'class': 'form-check-input',
            }
        )
        self.fields['is_superuser'].widget.attrs.update(
            {
                'class': 'form-check-input',
            }
        )
