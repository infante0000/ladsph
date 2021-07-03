from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    error_css_class = 'error'
    phone = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
