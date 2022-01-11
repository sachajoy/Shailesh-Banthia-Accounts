from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from authentication.models import User
from authentication.forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CreateUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy('logout')


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authentication/user_update_form.html'
    permission_required = 'authentication.change_user'

    def handle_no_permission(self):
        return redirect('permission-denied')


    def get_success_url(self):
        return reverse_lazy('authentication:list-user')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users_list'
