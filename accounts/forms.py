from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'image',)

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = ('email', 'image',)

class CustomPasswordChangeForm(PasswordChangeForm):
    pass