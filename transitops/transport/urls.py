from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("vehicles/", views.vehicles, name="vehicles"),
    path("drivers/", views.drivers, name="drivers"),
    path("trips/", views.trips, name="trips"),
    path("maintenance/", views.maintenance, name="maintenance"),
    path("fuel/", views.fuel, name="fuel"),
    path("reports/", views.reports, name="reports"),
    path("settings/", views.settings_page, name="settings"),
]