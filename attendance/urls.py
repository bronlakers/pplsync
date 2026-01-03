from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload, name="attendance_upload"),
    path("month/", views.month_view, name="attendance_month_view"),
    path("mine/", views.my_history, name="attendance_my_history"),
]
