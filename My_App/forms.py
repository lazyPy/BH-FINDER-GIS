from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django import forms


class UserForm(UserCreationForm):
    name = forms.CharField(label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'


class BoardingHouseForm(ModelForm):
    class Meta:
        model = BoardingHouse
        fields = ['name', 'description', 'price', 'phone', 'location', 'latitude', 'longitude']


class BoardingHouseFullForm(ModelForm):
    picture = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(BoardingHouseForm.Meta):
        fields = BoardingHouseForm.Meta.fields + ['picture', ]
