from os import name
from django.urls import path, include
from django.views.generic.edit import CreateView
from .views import dashboard_view
from .views import firm_views
from .views import client_views
from .views import selected_period_view
from .views import tranction_view

app_name = 'ledger'
urlpatterns = [
    path('', dashboard_view.DashboardListView.as_view(), name='index'),
    path('create-firm/', firm_views.FirmCreateView.as_view(), name='create-firm'),
    path('list-firm/', firm_views.FirmListView.as_view(), name='list-firm'),
    path('update-firm/<int:pk>/', firm_views.FirmUpdateView.as_view(), name='update-firm'),
    path('create-client/', client_views.ClientCreateView.as_view(), name='create-client'),
    path('detail-client/<int:client_id>/',
         tranction_view.ClientDetailTranctionCreateListView.as_view(),
         name='detail-client'),
    path('detail-client/<int:client_id>/update-client-tranction/<int:pk>',
         tranction_view.ClientDetailTranctionUpdateListView.as_view(),
         name='detail-client-udpate-tranction'),
    path('client/<int:client_id>/delete-tranction/<int:pk>',
         tranction_view.ClientTranctionDeleteView.as_view(),
         name='delete-client-tranction'),
    path('update-client/<int:pk>/', client_views.ClientUpdateView.as_view(), name='update-client'),
    path('period-selected-test/', selected_period_view.is_date_set, name='is-period-set'),
    path('set-period/', selected_period_view.SelectPeriodCreateView.as_view(), name='create-period'),
    path('set-period/<int:pk>/', selected_period_view.SelectPeriodUpdateView.as_view(), name='set-period'),
]
