from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class UserResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class CustomPasswordChangeForm(PasswordChangeForm):
    pass  # You can customize this later if needed

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'input-field',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email address',
            'class': 'input-field',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'input-field',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
            'class': 'input-field',
        })
