from django import forms
from django.core.exceptions import ValidationError
from askqa.models import *


class AskForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    text = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    tags = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class RegisterForm(forms.Form):
    login = forms.CharField(
        max_length=30,
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=50,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=30,
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        max_length=30,
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=30,
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProfileEditForm(forms.Form):
    login = forms.CharField(
        required=False,
        max_length=40,
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        max_length=40,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    avatar = forms.ImageField(
        required=False,
        label='UserAvatar',
        widget=forms.FileInput(attrs={'class': 'form-control ask-higher'})
    )


class AnswerForm(forms.Form):
    text = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={'class': 'ask-textarea'})
        )
