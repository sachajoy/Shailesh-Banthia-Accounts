from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('create-user/', views.CreateUserView.as_view(), name='create-user'),
    path('list-user/', views.UserListView.as_view(), name='list-user'),
    path('update-user/<int:pk>/', views.UserUpdateView.as_view(), name='update-user'),
]