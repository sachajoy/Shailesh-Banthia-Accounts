
from django.contrib import admin
from django.contrib import auth
from django.urls import path, include
from django.contrib.auth import views as auth_view
from ledger.views.dashboard_view import access_denid
urlpatterns = [
    path('', include('ledger.urls', 'ledger')),
    path('authentication/', include('authentication.urls', 'authentication')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('permission-denid', access_denid, name='permission-denied'),
    # path('admin/', admin.site.urls),
]
