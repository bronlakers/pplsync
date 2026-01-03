from django.contrib import admin
from django.urls import path, include
import os

from django.conf import settings
from django.conf.urls.static import static
from core.views import dashboard, login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", dashboard, name="dashboard"),

    path("attendance/", include("attendance.urls")),
    path("petty-cash/", include("pettycash.urls")),
    path("expenses/", include("expenses.urls")),
    path("assets/", include("assets.urls")),
]

if settings.DEBUG or os.getenv('SERVE_MEDIA', '0') == '1':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
