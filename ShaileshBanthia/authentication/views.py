from django.views.generic import CreateView, ListView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import User
from authentication.forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm

class CreateUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy('login')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authentication/user_update_form.html'

    def get_success_url(self):
        return reverse_lazy('authentication:list-user')

class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users_list'
