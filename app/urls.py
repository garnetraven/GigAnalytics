from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/deliveries/", views.deliveries, name="deliveries"),
    path("dashboard/reports/", views.reports, name="reports"),
    path("dashboard/settings/", views.settings, name="settings"),
]
