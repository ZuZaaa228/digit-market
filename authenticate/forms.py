from django import forms
from django.contrib.auth import authenticate

from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _('Почта')
        self.fields['username'].label = _('Ник')
        self.fields['password'].label = _('Пароль')
        self.fields['confirm_password'].label = _('Подтвердить пароль')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _('Почта')
        self.fields['password'].label = _('Пароль')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
            if not user.is_active:
                raise forms.ValidationError("User is not active")
        return self.cleaned_data


from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _('Почта')
        self.fields['username'].label = _('Ник')


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = _('Старый пароль')
        self.fields['new_password1'].label = _('Новый пароль')
        self.fields['new_password2'].label = _('Подтверди пароль')
