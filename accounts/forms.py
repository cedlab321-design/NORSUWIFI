from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'id_number', 'phone', 'department']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border rounded'}),
            'department': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border rounded'}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Password'
    }))