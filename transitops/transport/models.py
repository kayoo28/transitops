from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


# ==========================================================
# VEHICLE MODEL
# ==========================================================

class Vehicle(models.Model):

    STATUS_CHOICES = (
        ("AVAILABLE", "Available"),
        ("ON_TRIP", "On Trip"),
        ("MAINTENANCE", "Maintenance"),
        ("INACTIVE", "Inactive"),
    )

    FUEL_CHOICES = (
        ("PETROL", "Petrol"),
        ("DIESEL", "Diesel"),
        ("CNG", "CNG"),
        ("EV", "Electric"),
    )

    vehicle_number = models.CharField(
        max_length=20,
        unique=True,
    )

    vehicle_name = models.CharField(
        max_length=100,
    )

    vehicle_type = models.CharField(
        max_length=50,
    )

    brand = models.CharField(
        max_length=50,
    )

    model = models.CharField(
        max_length=50,
    )

    manufacturing_year = models.PositiveIntegerField()

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
    )

    seating_capacity = models.PositiveIntegerField(
        default=2
    )

    mileage = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Kilometers per litre"
    )

    odometer = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    insurance_expiry = models.DateField()

    pollution_expiry = models.DateField()

    registration_expiry = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )

    image = models.ImageField(
        upload_to="vehicles/",
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehicles_created"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["vehicle_number"]

        verbose_name = "Vehicle"

        verbose_name_plural = "Vehicles"

    def __str__(self):

        return self.vehicle_number


# ==========================================================
# DRIVER MODEL
# ==========================================================

class Driver(models.Model):

    LICENSE_STATUS = (
        ("VALID", "Valid"),
        ("EXPIRED", "Expired"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_profile"
    )

    driver_id = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(
        max_length=120
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    license_expiry = models.DateField()

    license_status = models.CharField(
        max_length=20,
        choices=LICENSE_STATUS,
        default="VALID"
    )

    experience = models.PositiveIntegerField(
        default=0
    )

    joining_date = models.DateField()

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    emergency_contact = models.CharField(
        max_length=15
    )

    active = models.BooleanField(
        default=True
    )

    image = models.ImageField(
        upload_to="drivers/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["full_name"]

        verbose_name = "Driver"

        verbose_name_plural = "Drivers"

    def __str__(self):

        return self.full_name
    

# ==========================================================
# TRIP MODEL
# ==========================================================

class Trip(models.Model):

    STATUS_CHOICES = (
        ("SCHEDULED", "Scheduled"),
        ("ONGOING", "Ongoing"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    trip_id = models.CharField(
        max_length=20,
        unique=True,
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="trips",
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="trips",
    )

    source = models.CharField(
        max_length=150,
    )

    destination = models.CharField(
        max_length=150,
    )

    start_date = models.DateField()

    start_time = models.TimeField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    end_time = models.TimeField(
        null=True,
        blank=True,
    )

    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Distance in KM",
    )

    estimated_duration = models.DurationField()

    actual_duration = models.DurationField(
        null=True,
        blank=True,
    )

    cargo_details = models.TextField(
        blank=True,
    )

    customer_name = models.CharField(
        max_length=120,
        blank=True,
    )

    customer_phone = models.CharField(
        max_length=15,
        blank=True,
    )

    trip_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SCHEDULED",
    )

    remarks = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trips_created",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-start_date",
            "-start_time",
        ]

        verbose_name = "Trip"

        verbose_name_plural = "Trips"

    def __str__(self):

        return self.trip_id


# ==========================================================
# FUEL RECORD MODEL
# ==========================================================

class FuelRecord(models.Model):

    PAYMENT_CHOICES = (
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("UPI", "UPI"),
        ("COMPANY", "Company Account"),
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="fuel_records",
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fuel_records",
    )

    fuel_date = models.DateField(
        default=timezone.now,
    )

    fuel_station = models.CharField(
        max_length=150,
        blank=True,
    )

    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    price_per_litre = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    odometer_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="UPI",
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-fuel_date",
            "-created_at",
        ]

        verbose_name = "Fuel Record"

        verbose_name_plural = "Fuel Records"

    def __str__(self):

        return f"{self.vehicle.vehicle_number} - {self.fuel_date}"
    

# ==========================================================
# MAINTENANCE MODEL
# ==========================================================

class Maintenance(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    )

    PRIORITY_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="maintenance_records",
    )

    title = models.CharField(
        max_length=150,
    )

    description = models.TextField()

    service_center = models.CharField(
        max_length=150,
        blank=True,
    )

    mechanic_name = models.CharField(
        max_length=120,
        blank=True,
    )

    service_date = models.DateField()

    next_service_date = models.DateField(
        null=True,
        blank=True,
    )

    estimated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    actual_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    remarks = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_created",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-service_date",
        ]

        verbose_name = "Maintenance"

        verbose_name_plural = "Maintenance Records"

    def __str__(self):

        return f"{self.vehicle.vehicle_number} - {self.title}"


# ==========================================================
# EXPENSE MODEL
# ==========================================================

class Expense(models.Model):

    CATEGORY_CHOICES = (
        ("FUEL", "Fuel"),
        ("MAINTENANCE", "Maintenance"),
        ("SALARY", "Salary"),
        ("TOLL", "Toll"),
        ("INSURANCE", "Insurance"),
        ("OTHER", "Other"),
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="expenses",
        null=True,
        blank=True,
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )

    expense_date = models.DateField(
        default=timezone.now,
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
    )

    title = models.CharField(
        max_length=150,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    description = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses_created",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-expense_date",
            "-created_at",
        ]

        verbose_name = "Expense"

        verbose_name_plural = "Expenses"

    def __str__(self):

        return f"{self.category} - ₹{self.amount}"
    

# ==========================================================
# NOTIFICATION MODEL
# ==========================================================

class Notification(models.Model):

    notification_type = (
        ("INFO", "Information"),
        ("WARNING", "Warning"),
        ("SUCCESS", "Success"),
        ("ERROR", "Error"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=150,
    )

    message = models.TextField()

    notification_category = models.CharField(
        max_length=20,
        choices=notification_type,
        default="INFO",
    )

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        verbose_name = "Notification"

        verbose_name_plural = "Notifications"

    def __str__(self):

        return self.title


# ==========================================================
# DASHBOARD ALERT MODEL
# ==========================================================

class DashboardAlert(models.Model):

    ALERT_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=ALERT_CHOICES,
        default="LOW",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        verbose_name = "Dashboard Alert"

        verbose_name_plural = "Dashboard Alerts"

    def __str__(self):

        return self.title