
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Sum

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

    return render(
        request,
        "transport/fleet.html",
        {
            "vehicles": vehicles,
        },
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

@login_required
def driver_list(request):

    drivers = Driver.objects.all().order_by("full_name")

    return render(
        request,
        "transport/drivers.html",
        {
            "drivers": drivers,
        },
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
        "driver",
    ).order_by("-start_date", "-start_time")

    return render(
        request,
        "transport/trips.html",
        {
            "trips": trips,
        },
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

    fuels = FuelRecord.objects.select_related(
        "vehicle",
        "trip",
    ).order_by("-fuel_date")

    return render(
        request,
        "transport/fuel.html",
        {
            "fuels": fuels,
        },
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

    maintenance = Maintenance.objects.all().order_by("-service_date")

    return render(
        request,
        "transport/maintenance.html",
        {
            "maintenance": maintenance,
        },
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

    expenses = Expense.objects.all().order_by("-expense_date")

    return render(
        request,
        "transport/expenses.html",
        {
            "expenses": expenses,
        },
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

    context = {
        "vehicle_count": Vehicle.objects.count(),
        "driver_count": Driver.objects.count(),
        "trip_count": Trip.objects.count(),
        "expense_total": Expense.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0,
    }

    return render(
        request,
        "transport/analytics.html",
        context,
    )


# ==========================================================
# REPORTS
# ==========================================================

@login_required
def reports(request):

    return render(
        request,
        "transport/reports.html",
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

