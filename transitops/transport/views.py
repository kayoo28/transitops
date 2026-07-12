from django.shortcuts import render


def login_view(request):
    return render(request, "transport/login.html")


def dashboard(request):
    return render(request, "transport/dashboard.html")


def vehicles(request):
    return render(request, "transport/vehicles.html")


def drivers(request):
    return render(request, "transport/drivers.html")


def trips(request):
    return render(request, "transport/trips.html")


def maintenance(request):
    return render(request, "transport/maintenance.html")


def fuel(request):
    return render(request, "transport/fuel.html")


def reports(request):
    return render(request, "transport/reports.html")


def settings_page(request):
    return render(request, "transport/settings.html")