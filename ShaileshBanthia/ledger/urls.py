from os import name
from django.urls import path, include
from .views import dashboard_view
from .views import firm_views
from .views import client_views
app_name = 'ledger'
urlpatterns = [
    path('', dashboard_view.DashboardListView.as_view(), name='index'),
    path('create-firm/', firm_views.FirmCreateView.as_view(), name='create-firm'),
    path('list-firm/', firm_views.FirmListView.as_view(), name='list-firm'),
    path('update-firm/<int:pk>/', firm_views.FirmUpdateView.as_view(), name='update-firm'),
    path('create-client/', client_views.ClientCreateView.as_view(), name='create-client'),
    path('detail-client/<int:pk>/', client_views.ClientDetialView.as_view(), name='detail-client'),
    path('update-client/<int:pk>/', client_views.ClientUpdateView.as_view(), name='update-client'),
]
