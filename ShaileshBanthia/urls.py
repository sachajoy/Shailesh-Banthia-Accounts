
from django.urls import path, include
from ledger.views.dashboard_view import access_denid

urlpatterns = [
    path('', include('ledger.urls', 'ledger')),
    path('authentication/', include('authentication.urls', 'authentication')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('permission-denid', access_denid, name='permission-denied'),
    path('report/', include('report.urls', 'report')),
    # path('admin/', admin.site.urls),
]