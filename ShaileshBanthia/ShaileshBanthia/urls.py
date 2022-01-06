
from django.contrib import admin
from django.contrib import auth
from django.urls import path, include
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('', include('ledger.urls', 'ledger')),
    path('authentication/', include('authentication.urls', 'authentication')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('admin/', admin.site.urls),
]
