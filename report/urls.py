from django.urls import path

from . import views
app_name = 'report'
urlpatterns = [
    path('intrest-statement/<int:client_id>/', views.intrest_statement, name='intrest-statement'),
    path('selected-trancation-statement/<int:client_id>/', views.selected_trancations, name='selected-entry-statement'),
    path('day-report/', views.day_trancations, name='day-report'),
]
