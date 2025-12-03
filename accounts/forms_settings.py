from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class SettingsForm(forms.Form):
    first_name = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={'class':'block w-full px-3 py-2 border rounded'}))
    last_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class':'block w-full px-3 py-2 border rounded'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'block w-full px-3 py-2 border rounded'}))
    id_number = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'block w-full px-3 py-2 border rounded'}))
    receive_newsletters = forms.BooleanField(required=False, initial=True)
    public_profile = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['id_number'].initial = getattr(user.userprofile, 'id_number', '') if hasattr(user, 'userprofile') else ''
            profile = getattr(user, 'userprofile', None)
            if profile:
                # fallback defaults
                self.fields['receive_newsletters'].initial = getattr(profile, 'subscribe_newsletter', True) if hasattr(profile, 'subscribe_newsletter') else True
                self.fields['public_profile'].initial = getattr(profile, 'is_public', True) if hasattr(profile, 'is_public') else True

    def save(self):
        if not self.user:
            return None
        data = self.cleaned_data
        u = self.user
        u.first_name = data.get('first_name', '')
        u.last_name = data.get('last_name', '')
        u.email = data.get('email', '')
        u.save()
        profile = getattr(u, 'userprofile', None)
        if profile:
            profile.id_number = data.get('id_number', '')
            if hasattr(profile, 'subscribe_newsletter'):
                profile.subscribe_newsletter = data.get('receive_newsletters', True)
            if hasattr(profile, 'is_public'):
                profile.is_public = data.get('public_profile', True)
            profile.save()
        return u
