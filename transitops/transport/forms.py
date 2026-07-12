from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    Vehicle,
    Driver,
    Trip,
    FuelRecord,
    Maintenance,
    Expense,
)


# ==========================================================
# LOGIN FORM
# ==========================================================

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Username",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
                "autocomplete": "current-password",
            }
        )
    )


# ==========================================================
# VEHICLE FORM
# ==========================================================

class VehicleForm(forms.ModelForm):

    class Meta:

        model = Vehicle

        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )

        widgets = {

            "vehicle_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "vehicle_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "vehicle_type": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "brand": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "model": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "manufacturing_year": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "fuel_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "seating_capacity": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "mileage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "odometer": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "insurance_expiry": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "pollution_expiry": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "registration_expiry": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

# ==========================================================
# DRIVER FORM
# ==========================================================

class DriverForm(forms.ModelForm):

    class Meta:

        model = Driver

        exclude = (
            "created_at",
            "updated_at",
        )

        widgets = {

            "user": forms.Select(
                attrs={"class": "form-select"}
            ),

            "driver_id": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "full_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "city": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "state": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "pincode": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "license_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "license_expiry": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "license_status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "experience": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "joining_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "emergency_contact": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }


# ==========================================================
# TRIP FORM
# ==========================================================

class TripForm(forms.ModelForm):

    class Meta:

        model = Trip

        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )

        widgets = {

            "trip_id": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "vehicle": forms.Select(
                attrs={"class": "form-select"}
            ),

            "driver": forms.Select(
                attrs={"class": "form-select"}
            ),

            "source": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "destination": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "distance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "estimated_duration": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "HH:MM:SS",
                }
            ),

            "actual_duration": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "HH:MM:SS",
                }
            ),

            "cargo_details": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "customer_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "customer_phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "trip_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

# ==========================================================
# FUEL RECORD FORM
# ==========================================================

class FuelRecordForm(forms.ModelForm):

    class Meta:

        model = FuelRecord

        exclude = (
            "created_at",
        )

        widgets = {

            "vehicle": forms.Select(
                attrs={"class": "form-select"}
            ),

            "trip": forms.Select(
                attrs={"class": "form-select"}
            ),

            "fuel_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "fuel_station": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "price_per_litre": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "total_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "odometer_reading": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "payment_mode": forms.Select(
                attrs={"class": "form-select"}
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }


# ==========================================================
# MAINTENANCE FORM
# ==========================================================

class MaintenanceForm(forms.ModelForm):

    class Meta:

        model = Maintenance

        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )

        widgets = {

            "vehicle": forms.Select(
                attrs={"class": "form-select"}
            ),

            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "service_center": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "mechanic_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "service_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "next_service_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "estimated_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "actual_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "priority": forms.Select(
                attrs={"class": "form-select"}
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

# ==========================================================
# EXPENSE FORM
# ==========================================================

class ExpenseForm(forms.ModelForm):

    class Meta:

        model = Expense

        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )

        widgets = {

            "vehicle": forms.Select(
                attrs={"class": "form-select"}
            ),

            "trip": forms.Select(
                attrs={"class": "form-select"}
            ),

            "expense_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "category": forms.Select(
                attrs={"class": "form-select"}
            ),

            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        if amount <= 0:
            raise forms.ValidationError(
                "Amount must be greater than zero."
            )

        return amount


# ==========================================================
# COMMON FORM VALIDATION
# ==========================================================

class BaseBootstrapForm(forms.ModelForm):

    """
    Base form for future forms.
    Automatically applies Bootstrap classes.
    """

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.CheckboxInput):

                field.widget.attrs.setdefault(
                    "class",
                    "form-check-input"
                )

            elif isinstance(field.widget, forms.Select):

                field.widget.attrs.setdefault(
                    "class",
                    "form-select"
                )

            elif isinstance(field.widget, forms.ClearableFileInput):

                field.widget.attrs.setdefault(
                    "class",
                    "form-control"
                )

            else:

                field.widget.attrs.setdefault(
                    "class",
                    "form-control"
                )