from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, DeliveryForm
from .models import Delivery
from datetime import timedelta

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

@login_required
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

def get_week_range(date):
    """Return start and end dates of the week containing the given date."""
    start_of_week = date - timedelta(days=date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return start_of_week, end_of_week

@login_required
def reports(request):
    # Get current week or week from query parameters
    today = timezone.now().date()
    week_start_date_str = request.GET.get('week_start_date', str(today - timedelta(days=today.weekday())))

    try:
        week_start_date = parse_date(week_start_date_str)
        if week_start_date is None:
            raise ValueError("Invalid date format")
    except (ValueError, TypeError):
        week_start_date = today - timedelta(days=today.weekday())

    week_end_date = week_start_date + timedelta(days=6)

    # Retrieve data from the database
    deliveries = Delivery.objects.filter(date__range=[week_start_date, week_end_date]).values()
    df = pd.DataFrame(list(deliveries))

    # Debugging: Print DataFrame contents
    print("DataFrame contents:")
    print(df)

    # Check if the DataFrame is not empty and contains the required column
    if not df.empty and 'date' in df.columns:
        # Perform data analysis using pandas and numpy
        earnings_mean = np.mean(df['earnings'])
        expenses_sum = np.sum(df['expenses'])
        mileage_mean = np.mean(df['mileage'])

        # Create a pivot table for total earnings and expenses per date
        grouped_df = df.groupby('date').agg({'earnings': 'sum', 'expenses': 'sum'}).reset_index()
        
        # Plotting
        fig, ax = plt.subplots(figsize=(12, 8))

        # Define the bar width and positions
        bar_width = 0.35
        r1 = np.arange(len(grouped_df['date']))
        r2 = [x + bar_width for x in r1]

        # Create bars for earnings and expenses
        earnings_bars = ax.bar(r1, grouped_df['earnings'], color='skyblue', width=bar_width, edgecolor='grey', label='Earnings')
        expenses_bars = ax.bar(r2, grouped_df['expenses'], color='salmon', width=bar_width, edgecolor='grey', label='Expenses')

        # Add labels and title
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Total Amount', fontweight='bold')
        ax.set_title('Total Earnings and Expenses per Date', fontweight='bold')
        ax.set_xticks([r + bar_width / 2 for r in range(len(grouped_df['date']))])
        ax.set_xticklabels(grouped_df['date'].astype(str), rotation=45)

        # Add legend
        ax.legend()

        # Annotate bars with numerical values
        def annotate_bars(bars):
            for bar in bars:
                yval = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0, yval,
                    f'{yval:.2f}',
                    va='bottom', ha='center',
                    fontsize=10, color='black'
                )

        annotate_bars(earnings_bars)
        annotate_bars(expenses_bars)

        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

    else:
        # If the DataFrame is empty or 'date' column is missing
        earnings_mean = 0
        expenses_sum = 0
        mileage_mean = 0
        image_base64 = None

    # Determine the next and previous weeks
    next_week_start = week_start_date + timedelta(weeks=1)
    prev_week_start = week_start_date - timedelta(weeks=1)

    context = {
        'earnings_mean': earnings_mean,
        'expenses_sum': expenses_sum,
        'mileage_mean': mileage_mean,
        'image_base64': image_base64,
        'week_start_date': week_start_date,
        'week_end_date': week_end_date,
        'next_week_start': next_week_start,
        'prev_week_start': prev_week_start,
    }
    return render(request, 'reports.html', context)

@login_required
def settings(request):
    return render(request, "settings.html")
