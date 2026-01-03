from django.urls import path
from . import views

urlpatterns = [
    path("", views.expense_list, name="expense_list"),
    path("mine/", views.expense_my_list, name="expense_my_list"),
    path("new/", views.expense_create, name="expense_create"),
    path("<int:expense_id>/approve/", views.expense_approve, name="expense_approve"),
    path("<int:expense_id>/paid/", views.expense_paid, name="expense_paid"),
]
