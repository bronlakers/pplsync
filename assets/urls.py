from django.urls import path
from . import views

urlpatterns = [
    path("", views.asset_list, name="asset_list"),
    path("new/", views.asset_create, name="asset_create"),
    path("<int:asset_id>/", views.asset_detail, name="asset_detail"),
    path("<int:asset_id>/assign/", views.asset_assign, name="asset_assign"),
    path("<int:asset_id>/return/", views.asset_return, name="asset_return"),
]
