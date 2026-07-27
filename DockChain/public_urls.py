"""
Restricted URLconf used for the public deploy (see settings_public.py).

Only the public-facing `webpage` app is routed — accounts/login, the
truckmanagement/Driver/Port dashboards, and Django admin are intentionally
left out so they're unreachable from the public site regardless of what
any template happens to link to.
"""
from django.urls import include, path

urlpatterns = [
    path('', include('webpage.urls')),
]
