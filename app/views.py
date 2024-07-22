from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, DeliveryForm
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
                login(request, user)
                return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def deliveries(request):
    deliveries = Delivery.objects.filter(user=request.user)

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.user = request.user
            delivery.save()
            return redirect('deliveries')
    else:
        form = DeliveryForm()

    sort = request.GET.get('sort', 'date')
    if sort:
        deliveries = deliveries.order_by(sort)

    return render(request, 'deliveries.html', {
        'deliveries': deliveries,
        'form': form,
    })

def reports(request):
    return render(request, "reports.html")

def settings(request):
    return render(request, "settings.html")
