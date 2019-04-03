from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Insert a valid email address.')   # Alt. required=False, help_text='Optional.'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )