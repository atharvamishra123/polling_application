from django import forms
from django.core.exceptions import ValidationError
from user.models import CustomUser
from . import models


class UserCreationForm(forms.ModelForm):
    name = forms.CharField(label='Enter Name')
    email = forms.EmailField(label='Enter email')
    username = forms.CharField(label='Enter Username')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = models.CustomUser
        fields = ['name', 'email', 'username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        return name

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            name=self.cleaned_data['name'],
        )
        return user
