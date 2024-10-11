from typing import Any

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordMixin

from accounts.models import User


class SignUpForm(forms.ModelForm, SetPasswordMixin):
    class Meta:
        model = User
        fields = [
            'email',
            'instagram',
            'cellphone',
        ]
        labels = {
            'cellphone': 'Telefone/Whatsapp',
        }
        widgets = {
            'cellphone': forms.TextInput(
                attrs={'oninput': 'cellphoneMask(this)'}
            )
        }

    password1, password2 = SetPasswordMixin.create_password_fields()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = '' if not email else email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Usuário com este e-mail já existe.')
        return email

    def clean_instagram(self):
        instagram = self.cleaned_data.get('instagram')
        instagram = '' if not instagram else instagram.lower()

        if User.objects.filter(instagram=instagram).exists():
            raise forms.ValidationError(
                'Usuário com este instagram já existe.'
            )

        return instagram

    def clean(self) -> dict[str, Any]:
        self.validate_passwords()
        return super().clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Digite seu e-mail',
            'instagram': 'Digite seu usuário',
            'cellphone': '(11) 99999-9999',
            'password1': 'Digite sua senha',
            'password2': 'Confirme sus senha',
        }
        for field_name, field in self.fields.items():
            field.required = True
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name),
            })

    async def asave(self, commit: bool = True) -> Any:
        user = super().save(False)
        user.set_password(self.cleaned_data['password1'])
        await user.asave(commit)
        return user


class SignInForm(forms.Form):
    email = forms.CharField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Digite seu e-mail',
            'password': 'Digite sua senha',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name)
            })

    def clean(self) -> dict[str, Any]:
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if (user := authenticate(username=email, password=password)) is None:
            raise forms.ValidationError('Credenciais incorretas.')
        self.user = user
        return super().clean()
