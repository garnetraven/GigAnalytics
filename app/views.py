from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Delivery

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def dashboard(request):
    return render(request, "dashboard.html")

def deliveries(request):
    if not request.user.is_authenticated:
        return redirect('login')

    deliveries = Delivery.objects.filter(user=request.user)

    return render(request, "deliveries.html", {"deliveries": deliveries})

def reports(request):
    return render(request, "reports.html")

def settings(request):
    return render(request, "settings.html")
