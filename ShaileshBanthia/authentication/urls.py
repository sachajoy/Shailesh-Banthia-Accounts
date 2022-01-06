from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('create-user/', views.CreateUserView.as_view(), name='create-user')
]