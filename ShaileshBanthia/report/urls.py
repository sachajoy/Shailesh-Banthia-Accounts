from django.urls import path

from . import views
app_name = 'report'
urlpatterns = [
    path('intrest-statement/<int:client_id>/', views.intrest_statement, name='intrest-statement'),
]
