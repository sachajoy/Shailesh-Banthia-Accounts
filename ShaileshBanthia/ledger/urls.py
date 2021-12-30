from os import name
from django.urls import path, include
from .views import dashboard_view
from .views import firm_views
app_name = 'ledger'
urlpatterns = [
    path('', dashboard_view.DashboardListView.as_view(), name='index'),
    path('create-firm/', firm_views.FirmCreateView.as_view(), name='create-firm')
]
