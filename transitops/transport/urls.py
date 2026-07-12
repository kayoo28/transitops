from django.urls import path

from . import views

urlpatterns = [

    # ==========================================
    # Authentication
    # ==========================================

    path(
        "",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    # ==========================================
    # Dashboard
    # ==========================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # ==========================================
    # Fleet Management
    # ==========================================

    path(
        "fleet/",
        views.vehicle_list,
        name="fleet",
    ),

    path(
        "fleet/add/",
        views.vehicle_create,
        name="vehicle_add",
    ),

    path(
        "fleet/<int:pk>/edit/",
        views.vehicle_update,
        name="vehicle_edit",
    ),

    path(
        "fleet/<int:pk>/delete/",
        views.vehicle_delete,
        name="vehicle_delete",
    ),

    # ==========================================
    # Driver Management
    # ==========================================

    path(
        "drivers/",
        views.driver_list,
        name="drivers",
    ),

    path(
        "drivers/add/",
        views.driver_create,
        name="driver_add",
    ),

    path(
        "drivers/<int:pk>/edit/",
        views.driver_update,
        name="driver_edit",
    ),

    path(
        "drivers/<int:pk>/delete/",
        views.driver_delete,
        name="driver_delete",
    ),

    # ==========================================
    # Trip Management
    # ==========================================

    path(
        "trips/",
        views.trip_list,
        name="trips",
    ),

    path(
        "trips/add/",
        views.trip_create,
        name="trip_add",
    ),

    path(
        "trips/<int:pk>/edit/",
        views.trip_update,
        name="trip_edit",
    ),

    path(
        "trips/<int:pk>/delete/",
        views.trip_delete,
        name="trip_delete",
    ),

    # ==========================================
    # Fuel Management
    # ==========================================

    path(
        "fuel/",
        views.fuel_list,
        name="fuel",
    ),

    path(
        "fuel/add/",
        views.fuel_create,
        name="fuel_add",
    ),

    path(
        "fuel/<int:pk>/edit/",
        views.fuel_update,
        name="fuel_edit",
    ),

    path(
        "fuel/<int:pk>/delete/",
        views.fuel_delete,
        name="fuel_delete",
    ),

    # ==========================================
    # Maintenance
    # ==========================================

    path(
        "maintenance/",
        views.maintenance_list,
        name="maintenance",
    ),

    path(
        "maintenance/add/",
        views.maintenance_create,
        name="maintenance_add",
    ),

    path(
        "maintenance/<int:pk>/edit/",
        views.maintenance_update,
        name="maintenance_edit",
    ),

    path(
        "maintenance/<int:pk>/delete/",
        views.maintenance_delete,
        name="maintenance_delete",
    ),

    # ==========================================
    # Expense Management
    # ==========================================

    path(
        "expenses/",
        views.expense_list,
        name="expenses",
    ),

    path(
        "expenses/add/",
        views.expense_create,
        name="expense_add",
    ),

    path(
        "expenses/<int:pk>/edit/",
        views.expense_update,
        name="expense_edit",
    ),

    path(
        "expenses/<int:pk>/delete/",
        views.expense_delete,
        name="expense_delete",
    ),

    # ==========================================
    # Analytics
    # ==========================================

    path(
        "analytics/",
        views.analytics,
        name="analytics",
    ),

    # ==========================================
    # Reports
    # ==========================================

    path(
        "reports/",
        views.reports,
        name="reports",
    ),

    # ==========================================
    # Settings
    # ==========================================

    path(
        "settings/",
        views.settings_page,
        name="settings",
    ),

path(
    "settings/",
    views.settings_view,
    name="settings",
),
]