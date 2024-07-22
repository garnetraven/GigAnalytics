from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Delivery

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['date', 'app_name', 'earnings', 'expenses', 'mileage', 'time_spent', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
