from django.shortcuts import render

def login(request):
    return render(request,"transport/login.html")

def dashboard(request):
    return render(request,"transport/dashboard.html")