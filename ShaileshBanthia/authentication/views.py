from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import User
from authentication.forms import CustomUserCreationForm
from django.urls import reverse_lazy

class CreateUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy('login')
