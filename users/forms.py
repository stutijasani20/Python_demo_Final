from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from . models import *

class RegisterForm(UserCreationForm):
    USER_ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('recruiter', 'Recruiter'),
    ]
    role = forms.ChoiceField(choices=USER_ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')