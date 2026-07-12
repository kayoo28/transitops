
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Sum, Avg, Max
from django.utils import timezone

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

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

from .forms import (
    LoginForm,
    VehicleForm,
    DriverForm,
    TripForm,
    FuelRecordForm,
    MaintenanceForm,
    ExpenseForm,
)


# ==========================================================
# LOGIN
# ==========================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data.get("username")

            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password,
            )

            if user:

                login(request, user)

                return redirect("dashboard")

            messages.error(
                request,
                "Invalid Username or Password."
            )

    return render(
        request,
        "transport/login.html",
        {
            "form": form
        }
    )


# ==========================================================
# LOGOUT
# ==========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


# ==========================================================
# DASHBOARD
# ==========================================================

@login_required
def dashboard(request):

    total_vehicles = Vehicle.objects.count()

    total_drivers = Driver.objects.count()

    total_trips = Trip.objects.count()

    active_trips = Trip.objects.filter(
        status="ONGOING"
    ).count()

    total_expense = Expense.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    recent_notifications = Notification.objects.filter(
        user=request.user
    )[:5]

    alerts = DashboardAlert.objects.filter(
        is_active=True
    )[:5]

    recent_trips = Trip.objects.select_related(
    "vehicle",
    "driver",
    ).order_by("-start_date", "-start_time")[:5]

    context = {

        "total_vehicles": total_vehicles,

        "total_drivers": total_drivers,

        "total_trips": total_trips,

        "active_trips": active_trips,

        "total_expense": total_expense,
        "recent_trips": recent_trips,

        "recent_notifications": recent_notifications,

        "alerts": alerts,

    }

    return render(
        request,
        "transport/dashboard.html",
        context,
    )


# ==========================================================
# VEHICLE LIST
# ==========================================================

@login_required
def vehicle_list(request):

    vehicles = Vehicle.objects.all().order_by("vehicle_number")

    context = {

        "vehicles": vehicles,

        "available_count": vehicles.filter(
            status="AVAILABLE"
        ).count(),

        "on_trip_count": vehicles.filter(
            status="ON_TRIP"
        ).count(),

        "maintenance_count": vehicles.filter(
            status="MAINTENANCE"
        ).count(),

    }

    return render(
        request,
        "transport/fleet.html",
        context,
    )

# ==========================================================
# ADD VEHICLE
# ==========================================================

@login_required
def vehicle_create(request):

    if request.method == "POST":

        form = VehicleForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            vehicle = form.save(commit=False)

            vehicle.created_by = request.user

            vehicle.save()

            messages.success(
                request,
                "Vehicle added successfully."
            )

            return redirect("fleet")

    else:

        form = VehicleForm()

    return render(
        request,
        "transport/vehicle_form.html",
        {
            "form": form,
            "title": "Add Vehicle",
        },
    )


# ==========================================================
# UPDATE VEHICLE
# ==========================================================

@login_required
def vehicle_update(request, pk):

    vehicle = get_object_or_404(
        Vehicle,
        pk=pk,
    )

    if request.method == "POST":

        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Vehicle updated successfully."
            )

            return redirect("fleet")

    else:

        form = VehicleForm(
            instance=vehicle,
        )

    return render(
        request,
        "transport/vehicle_form.html",
        {
            "form": form,
            "title": "Edit Vehicle",
            "vehicle": vehicle,
        },
    )


# ==========================================================
# DELETE VEHICLE
# ==========================================================

@login_required
def vehicle_delete(request, pk):

    vehicle = get_object_or_404(
        Vehicle,
        pk=pk,
    )

    if request.method == "POST":

        vehicle.delete()

        messages.success(
            request,
            "Vehicle deleted successfully."
        )

        return redirect("fleet")

    return render(
        request,
        "transport/confirm_delete.html",
        {
            "object": vehicle,
            "title": "Delete Vehicle",
        },
    )

# ==========================================================
# DRIVER LIST
# ==========================================================

from django.db.models import Avg

@login_required
def driver_list(request):

    drivers = Driver.objects.all().order_by("full_name")

    context = {

        "drivers": drivers,

        "active_driver_count": drivers.filter(
            active=True
        ).count(),

        "valid_license_count": drivers.filter(
            license_status="VALID"
        ).count(),

        "average_experience": round(
            drivers.aggregate(
                Avg("experience")
            )["experience__avg"] or 0,
            1,
        ),

    }

    return render(
        request,
        "transport/drivers.html",
        context,
    )


# ==========================================================
# ADD DRIVER
# ==========================================================

@login_required
def driver_create(request):

    if request.method == "POST":

        form = DriverForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Driver added successfully."
            )

            return redirect("drivers")

    else:

        form = DriverForm()

    return render(
        request,
        "transport/driver_form.html",
        {
            "form": form,
            "title": "Add Driver",
        },
    )

# ==========================================================
# UPDATE DRIVER
# ==========================================================

@login_required
def driver_update(request, pk):

    driver = get_object_or_404(
        Driver,
        pk=pk,
    )

    if request.method == "POST":

        form = DriverForm(
            request.POST,
            request.FILES,
            instance=driver,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Driver updated successfully."
            )

            return redirect("drivers")

    else:

        form = DriverForm(
            instance=driver,
        )

    return render(
        request,
        "transport/driver_form.html",
        {
            "form": form,
            "driver": driver,
            "title": "Edit Driver",
        },
    )


# ==========================================================
# DELETE DRIVER
# ==========================================================

@login_required
def driver_delete(request, pk):

    driver = get_object_or_404(
        Driver,
        pk=pk,
    )

    if request.method == "POST":

        driver.delete()

        messages.success(
            request,
            "Driver deleted successfully."
        )

        return redirect("drivers")

    return render(
        request,
        "transport/confirm_delete.html",
        {
            "object": driver,
            "title": "Delete Driver",
        },
    )


# ==========================================================
# TRIP LIST
# ==========================================================

@login_required
def trip_list(request):

    trips = Trip.objects.select_related(
        "vehicle",
        "driver"
    ).order_by(
        "-start_date",
        "-start_time"
    )

    total_trips = trips.count()

    completed_trip_count = trips.filter(
        status="COMPLETED"
    ).count()

    ongoing_trip_count = trips.filter(
        status="ONGOING"
    ).count()

    cancelled_trip_count = trips.filter(
        status="CANCELLED"
    ).count()

    total_distance = (
        trips.aggregate(
            Sum("distance")
        )["distance__sum"] or 0
    )

    total_trip_cost = (
        trips.aggregate(
            Sum("trip_cost")
        )["trip_cost__sum"] or 0
    )

    completion_rate = (
        round(
            (completed_trip_count / total_trips) * 100,
            1,
        )
        if total_trips else 0
    )

    context = {

        "trips": trips,

        "ongoing_trip_count": ongoing_trip_count,

        "completed_trip_count": completed_trip_count,

        "cancelled_trip_count": cancelled_trip_count,

        "total_distance": total_distance,

        "total_trip_cost": total_trip_cost,

        "completion_rate": completion_rate,

    }

    return render(
        request,
        "transport/trips.html",
        context,
    )


# ==========================================================
# ADD TRIP
# ==========================================================

@login_required
def trip_create(request):

    if request.method == "POST":

        form = TripForm(request.POST)

        if form.is_valid():

            trip = form.save(commit=False)

            trip.created_by = request.user

            trip.save()

            messages.success(
                request,
                "Trip created successfully."
            )

            return redirect("trips")

    else:

        form = TripForm()

    return render(
        request,
        "transport/trip_form.html",
        {
            "form": form,
            "title": "Add Trip",
        },
    )


# ==========================================================
# UPDATE TRIP
# ==========================================================

@login_required
def trip_update(request, pk):

    trip = get_object_or_404(
        Trip,
        pk=pk,
    )

    if request.method == "POST":

        form = TripForm(
            request.POST,
            instance=trip,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Trip updated successfully."
            )

            return redirect("trips")

    else:

        form = TripForm(
            instance=trip,
        )

    return render(
        request,
        "transport/trip_form.html",
        {
            "form": form,
            "trip": trip,
            "title": "Edit Trip",
        },
    )


# ==========================================================
# DELETE TRIP
# ==========================================================

@login_required
def trip_delete(request, pk):

    trip = get_object_or_404(
        Trip,
        pk=pk,
    )

    if request.method == "POST":

        trip.delete()

        messages.success(
            request,
            "Trip deleted successfully."
        )

        return redirect("trips")

    return render(
        request,
        "transport/confirm_delete.html",
        {
            "object": trip,
            "title": "Delete Trip",
        },
    )

# ==========================================================
# FUEL LIST
# ==========================================================

@login_required
def fuel_list(request):

    records = FuelRecord.objects.select_related(
        "vehicle",
        "trip",
    ).order_by("-fuel_date")

    total_quantity = (
        records.aggregate(
            Sum("quantity")
        )["quantity__sum"] or 0
    )

    total_cost = (
        records.aggregate(
            Sum("total_cost")
        )["total_cost__sum"] or 0
    )

    vehicle_count = (
        records.values("vehicle")
        .distinct()
        .count()
    )

    average_quantity = (
        records.aggregate(
            Avg("quantity")
        )["quantity__avg"] or 0
    )

    average_cost = (
        records.aggregate(
            Avg("total_cost")
        )["total_cost__avg"] or 0
    )

    context = {

        "records": records,

        "total_quantity": round(
            total_quantity,
            2,
        ),

        "total_cost": round(
            total_cost,
            2,
        ),

        "vehicle_count": vehicle_count,

        "average_quantity": round(
            average_quantity,
            2,
        ),

        "average_cost": round(
            average_cost,
            2,
        ),

    }

    return render(
        request,
        "transport/fuel.html",
        context,
    )

@login_required
def fuel_create(request):

    if request.method == "POST":

        form = FuelRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Fuel record added successfully.")

            return redirect("fuel")

    else:

        form = FuelRecordForm()

    return render(
        request,
        "transport/fuel_form.html",
        {
            "form": form,
            "title": "Add Fuel Record",
        },
    )


@login_required
def fuel_update(request, pk):

    fuel = get_object_or_404(FuelRecord, pk=pk)

    if request.method == "POST":

        form = FuelRecordForm(
            request.POST,
            instance=fuel,
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Fuel record updated.")

            return redirect("fuel")

    else:

        form = FuelRecordForm(instance=fuel)

    return render(
        request,
        "transport/fuel_form.html",
        {
            "form": form,
            "title": "Edit Fuel Record",
        },
    )


@login_required
def fuel_delete(request, pk):

    fuel = get_object_or_404(FuelRecord, pk=pk)

    if request.method == "POST":

        fuel.delete()

        messages.success(request, "Fuel record deleted.")

        return redirect("fuel")

    return render(
        request,
        "transport/confirm_delete.html",
        {
            "object": fuel,
            "title": "Delete Fuel Record",
        },
    )


# ==========================================================
# MAINTENANCE
# ==========================================================

@login_required
def maintenance_list(request):

    maintenances = Maintenance.objects.select_related(
        "vehicle"
    ).order_by("-service_date")

    pending_count = maintenances.filter(
        status="PENDING"
    ).count()

    completed_count = maintenances.filter(
        status="COMPLETED"
    ).count()

    total_estimated_cost = (
        maintenances.aggregate(
            Sum("estimated_cost")
        )["estimated_cost__sum"] or 0
    )

    total_actual_cost = (
        maintenances.aggregate(
            Sum("actual_cost")
        )["actual_cost__sum"] or 0
    )

    total_records = maintenances.count()

    completion_rate = (
        round(
            (completed_count / total_records) * 100,
            1,
        )
        if total_records else 0
    )

    context = {

        "maintenances": maintenances,

        "pending_count": pending_count,

        "completed_count": completed_count,

        "total_estimated_cost": round(
            total_estimated_cost,
            2,
        ),

        "total_actual_cost": round(
            total_actual_cost,
            2,
        ),

        "completion_rate": completion_rate,

    }

    return render(
        request,
        "transport/maintenance.html",
        context,
    )


@login_required
def maintenance_create(request):

    if request.method == "POST":

        form = MaintenanceForm(request.POST)

        if form.is_valid():

            maintenance = form.save(commit=False)

            maintenance.created_by = request.user

            maintenance.save()

            messages.success(request, "Maintenance added.")

            return redirect("maintenance")

    else:

        form = MaintenanceForm()

    return render(
        request,
        "transport/maintenance_form.html",
        {
            "form": form,
            "title": "Add Maintenance",
        },
    )


@login_required
def maintenance_update(request, pk):

    maintenance = get_object_or_404(Maintenance, pk=pk)

    if request.method == "POST":

        form = MaintenanceForm(
            request.POST,
            instance=maintenance,
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Maintenance updated.")

            return redirect("maintenance")

    else:

        form = MaintenanceForm(instance=maintenance)

    return render(
        request,
        "transport/maintenance_form.html",
        {
            "form": form,
            "title": "Edit Maintenance",
        },
    )


@login_required
def maintenance_delete(request, pk):

    maintenance = get_object_or_404(Maintenance, pk=pk)

    if request.method == "POST":

        maintenance.delete()

        messages.success(request, "Maintenance deleted.")

        return redirect("maintenance")

    return render(
        request,
        "transport/confirm_delete.html",
        {
            "object": maintenance,
            "title": "Delete Maintenance",
        },
    )


# ==========================================================
# EXPENSE
# ==========================================================

@login_required
def expense_list(request):

    expenses = Expense.objects.select_related(
        "vehicle",
        "trip",
    ).order_by("-expense_date")

    total_amount = (
        expenses.aggregate(
            Sum("amount")
        )["amount__sum"] or 0
    )

    average_amount = (
        expenses.aggregate(
            Avg("amount")
        )["amount__avg"] or 0
    )

    highest_expense = (
        expenses.aggregate(
            Max("amount")
        )["amount__max"] or 0
    )

    category_count = (
        expenses.values("category")
        .distinct()
        .count()
    )

    context = {

        "expenses": expenses,

        "total_amount": round(
            total_amount,
            2,
        ),

        "average_amount": round(
            average_amount,
            2,
        ),

        "highest_expense": round(
            highest_expense,
            2,
        ),

        "category_count": category_count,

    }

    return render(
        request,
        "transport/expenses.html",
        context,
    )


@login_required
def expense_create(request):

    if request.method == "POST":

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.created_by = request.user

            expense.save()

            messages.success(request, "Expense added.")

            return redirect("expenses")

    else:

        form = ExpenseForm()

    return render(
        request,
        "transport/expense_form.html",
        {
            "form": form,
            "title": "Add Expense",
        },
    )


@login_required
def expense_update(request, pk):

    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense,
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Expense updated.")

            return redirect("expenses")

    else:

        form = ExpenseForm(instance=expense)

    return render(
        request,
        "transport/expense_form.html",
        {
            "form": form,
            "title": "Edit Expense",
        },
    )


@login_required
def expense_delete(request, pk):

    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":

        expense.delete()

        messages.success(request, "Expense deleted.")

        return redirect("expenses")

    return render(
        request,
        "transport/confirm_delete.html",
        {
            "object": expense,
            "title": "Delete Expense",
        },
    )


# ==========================================================
# ANALYTICS
# ==========================================================

@login_required
def analytics(request):

    vehicle_count = Vehicle.objects.count()

    driver_count = Driver.objects.count()

    trip_count = Trip.objects.count()

    revenue = (
        Trip.objects.aggregate(
            Sum("trip_cost")
        )["trip_cost__sum"] or 0
    )

    available_vehicles = Vehicle.objects.filter(
        status="AVAILABLE"
    ).count()

    on_trip_vehicles = Vehicle.objects.filter(
        status="ON_TRIP"
    ).count()

    maintenance_vehicles = Vehicle.objects.filter(
        status="MAINTENANCE"
    ).count()

    fuel_quantity = (
        FuelRecord.objects.aggregate(
            Sum("quantity")
        )["quantity__sum"] or 0
    )

    fuel_cost = (
        FuelRecord.objects.aggregate(
            Sum("total_cost")
        )["total_cost__sum"] or 0
    )

    avg_fuel_cost = (
        FuelRecord.objects.aggregate(
            Avg("total_cost")
        )["total_cost__avg"] or 0
    )

    completed_maintenance = Maintenance.objects.filter(
        status="COMPLETED"
    ).count()

    pending_maintenance = Maintenance.objects.filter(
        status="PENDING"
    ).count()

    maintenance_cost = (
        Maintenance.objects.aggregate(
            Sum("actual_cost")
        )["actual_cost__sum"] or 0
    )

    expense_total = (
        Expense.objects.aggregate(
            Sum("amount")
        )["amount__sum"] or 0
    )

    avg_expense = (
        Expense.objects.aggregate(
            Avg("amount")
        )["amount__avg"] or 0
    )

    highest_expense = (
        Expense.objects.aggregate(
            Max("amount")
        )["amount__max"] or 0
    )

    completed_trips = Trip.objects.filter(
        status="COMPLETED"
    ).count()

    completion_rate = (
        round((completed_trips / trip_count) * 100, 1)
        if trip_count else 0
    )

    fleet_utilization = (
        round((on_trip_vehicles / vehicle_count) * 100, 1)
        if vehicle_count else 0
    )

    active_drivers = Driver.objects.filter(
        active=True
    ).count()

    active_trips = Trip.objects.filter(
        status="ONGOING"
    ).count()

    maintenance_due = Maintenance.objects.filter(
        status="PENDING"
    ).count()

    total_distance = (
        Trip.objects.aggregate(
            Sum("distance")
        )["distance__sum"] or 0
    )

    average_distance = (
        Trip.objects.aggregate(
            Avg("distance")
        )["distance__avg"] or 0
    )

    licensed_drivers = Driver.objects.filter(
        license_status="VALID"
    ).count()

    avg_driver_experience = (
        Driver.objects.aggregate(
            Avg("experience")
        )["experience__avg"] or 0
    )

    driver_availability = (
        round((active_drivers / driver_count) * 100, 1)
        if driver_count else 0
    )

    recent_trips = Trip.objects.order_by(
        "-start_date",
        "-start_time",
    )[:5]

    return render(
        request,
        "transport/analytics.html",
        {
            "vehicle_count": vehicle_count,
            "driver_count": driver_count,
            "trip_count": trip_count,
            "revenue": revenue,
            "available_vehicles": available_vehicles,
            "on_trip_vehicles": on_trip_vehicles,
            "maintenance_vehicles": maintenance_vehicles,
            "fuel_quantity": round(fuel_quantity, 2),
            "fuel_cost": round(fuel_cost, 2),
            "avg_fuel_cost": round(avg_fuel_cost, 2),
            "completed_maintenance": completed_maintenance,
            "pending_maintenance": pending_maintenance,
            "maintenance_cost": round(maintenance_cost, 2),
            "expense_total": round(expense_total, 2),
            "avg_expense": round(avg_expense, 2),
            "highest_expense": round(highest_expense, 2),
            "completion_rate": completion_rate,
            "fleet_utilization": fleet_utilization,
            "active_drivers": active_drivers,
            "active_trips": active_trips,
            "maintenance_due": maintenance_due,
            "total_distance": round(total_distance, 2),
            "average_distance": round(average_distance, 2),
            "completed_trips": completed_trips,
            "licensed_drivers": licensed_drivers,
            "avg_driver_experience": round(avg_driver_experience, 1),
            "driver_availability": driver_availability,
            "recent_trips": recent_trips,
        },
    )


# ==========================================================
# REPORTS
# ==========================================================

@login_required
def reports(request):

    trip_count = Trip.objects.count()

    revenue = (
        Trip.objects.aggregate(
            Sum("trip_cost")
        )["trip_cost__sum"] or 0
    )

    expenses = (
        Expense.objects.aggregate(
            Sum("amount")
        )["amount__sum"] or 0
    )

    profit = revenue - expenses

    vehicle_count = Vehicle.objects.count()

    available_vehicles = Vehicle.objects.filter(
        status="AVAILABLE"
    ).count()

    maintenance_vehicles = Vehicle.objects.filter(
        status="MAINTENANCE"
    ).count()

    completed_trips = Trip.objects.filter(
        status="COMPLETED"
    ).count()

    ongoing_trips = Trip.objects.filter(
        status="ONGOING"
    ).count()

    cancelled_trips = Trip.objects.filter(
        status="CANCELLED"
    ).count()

    completed_services = Maintenance.objects.filter(
        status="COMPLETED"
    ).count()

    pending_services = Maintenance.objects.filter(
        status="PENDING"
    ).count()

    maintenance_cost = (
        Maintenance.objects.aggregate(
            Sum("actual_cost")
        )["actual_cost__sum"] or 0
    )

    monthly_trips = Trip.objects.filter(
        start_date__month=timezone.now().month
    ).count()

    monthly_revenue = (
        Trip.objects.filter(
            start_date__month=timezone.now().month
        ).aggregate(
            Sum("trip_cost")
        )["trip_cost__sum"] or 0
    )

    monthly_expenses = (
        Expense.objects.filter(
            expense_date__month=timezone.now().month
        ).aggregate(
            Sum("amount")
        )["amount__sum"] or 0
    )

    fleet_utilization = (
        round((ongoing_trips / vehicle_count) * 100, 1)
        if vehicle_count else 0
    )

    average_distance = (
        Trip.objects.aggregate(
            Avg("distance")
        )["distance__avg"] or 0
    )

    completion_rate = (
        round((completed_trips / trip_count) * 100, 1)
        if trip_count else 0
    )

    maintenance_completion = (
        round(
            (completed_services /
             (completed_services + pending_services)) * 100,
            1,
        )
        if (completed_services + pending_services) else 0
    )

    profit_margin = (
        round((profit / revenue) * 100, 1)
        if revenue else 0
    )

    recent_reports = []

    return render(
        request,
        "transport/reports.html",
        {

            "trip_count": trip_count,
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "profit": round(profit, 2),

            "vehicle_count": vehicle_count,
            "available_vehicles": available_vehicles,
            "maintenance_vehicles": maintenance_vehicles,

            "completed_trips": completed_trips,
            "ongoing_trips": ongoing_trips,
            "cancelled_trips": cancelled_trips,

            "completed_services": completed_services,
            "pending_services": pending_services,
            "maintenance_cost": round(maintenance_cost, 2),

            "monthly_trips": monthly_trips,
            "monthly_revenue": round(monthly_revenue, 2),
            "monthly_expenses": round(monthly_expenses, 2),

            "fleet_utilization": fleet_utilization,
            "average_distance": round(average_distance, 2),

            "completion_rate": completion_rate,
            "fuel_efficiency": "N/A",
            "maintenance_completion": maintenance_completion,
            "profit_margin": profit_margin,

            "recent_reports": recent_reports,

        },
    )

# ==========================================================
# SETTINGS
# ==========================================================

@login_required
def settings_page(request):

    return render(
        request,
        "transport/settings.html",
    )


@login_required
def settings_view(request):

    context = {

        "vehicle_count": Vehicle.objects.count(),

        "driver_count": Driver.objects.count(),

        "trip_count": Trip.objects.count(),

        "expense_count": Expense.objects.count(),

    }

    return render(
        request,
        "transport/settings.html",
        context,
    )