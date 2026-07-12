from django.contrib import admin

from .models import (
    Vehicle,
    Driver,
    Trip,
    FuelRecord,
    Maintenance,
    Expense,
    Notification,
    DashboardAlert,
)


# ==========================================================
# VEHICLE ADMIN
# ==========================================================

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "vehicle_number",
        "vehicle_name",
        "vehicle_type",
        "brand",
        "fuel_type",
        "status",
        "insurance_expiry",
    )

    list_filter = (
        "status",
        "vehicle_type",
        "fuel_type",
        "brand",
    )

    search_fields = (
        "vehicle_number",
        "vehicle_name",
        "brand",
        "model",
    )

    ordering = (
        "vehicle_number",
    )

    list_per_page = 20


# ==========================================================
# DRIVER ADMIN
# ==========================================================

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):

    list_display = (
        "driver_id",
        "full_name",
        "phone",
        "license_number",
        "license_status",
        "active",
    )

    list_filter = (
        "license_status",
        "active",
    )

    search_fields = (
        "driver_id",
        "full_name",
        "phone",
    )

    ordering = (
        "full_name",
    )

    list_per_page = 20


# ==========================================================
# TRIP ADMIN
# ==========================================================

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "trip_id",
        "vehicle",
        "driver",
        "source",
        "destination",
        "status",
        "start_date",
    )

    list_filter = (
        "status",
        "start_date",
    )

    search_fields = (
        "trip_id",
        "source",
        "destination",
    )

    autocomplete_fields = (
        "vehicle",
        "driver",
    )

    ordering = (
        "-start_date",
    )

    list_per_page = 20


# ==========================================================
# FUEL RECORD ADMIN
# ==========================================================

@admin.register(FuelRecord)
class FuelRecordAdmin(admin.ModelAdmin):

    list_display = (
        "vehicle",
        "trip",
        "fuel_date",
        "quantity",
        "price_per_litre",
        "total_cost",
    )

    list_filter = (
        "fuel_date",
        "payment_mode",
    )

    search_fields = (
        "vehicle__vehicle_number",
        "fuel_station",
    )

    ordering = (
        "-fuel_date",
    )

    list_per_page = 20


# ==========================================================
# MAINTENANCE ADMIN
# ==========================================================

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):

    list_display = (
        "vehicle",
        "title",
        "priority",
        "status",
        "service_date",
        "next_service_date",
    )

    list_filter = (
        "priority",
        "status",
    )

    search_fields = (
        "vehicle__vehicle_number",
        "title",
        "mechanic_name",
    )

    ordering = (
        "-service_date",
    )

    list_per_page = 20


# ==========================================================
# EXPENSE ADMIN
# ==========================================================

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "amount",
        "expense_date",
        "vehicle",
    )

    list_filter = (
        "category",
        "expense_date",
    )

    search_fields = (
        "title",
        "vehicle__vehicle_number",
    )

    ordering = (
        "-expense_date",
    )

    list_per_page = 20


# ==========================================================
# NOTIFICATION ADMIN
# ==========================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "notification_category",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_category",
        "is_read",
    )

    search_fields = (
        "title",
        "message",
        "user__username",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20


# ==========================================================
# DASHBOARD ALERT ADMIN
# ==========================================================

@admin.register(DashboardAlert)
class DashboardAlertAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "priority",
        "is_active",
        "created_at",
    )

    list_filter = (
        "priority",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20