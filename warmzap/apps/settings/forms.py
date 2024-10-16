from accounts.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'surname',
            'cpf',
            'cellphone',
            'instagram',
        ]
        labels = {
            'cellphone': 'Telefone/Whatsapp',
        }
        widgets = {
            'cellphone': forms.TextInput(
                attrs={'oninput': 'cellphoneMask(this)'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].disabled = True

        self.fields['name'].widget.attrs['placeholder'] = 'Digite seu nome'
        self.fields['name'].required = True

        self.fields['surname'].widget.attrs['placeholder'] = (
            'Digite seu sobrenome'
        )
        self.fields['surname'].required = True

        self.fields['cellphone'].widget.attrs['placeholder'] = (
            'Digite seu telefone'
        )
        self.fields['instagram'].widget.attrs['placeholder'] = (
            'Digite seu perfil do instagram'
        )
        self.fields['cpf'].widget.attrs['placeholder'] = 'Digite seu CPF'
        self.fields['cpf'].required = True

        if self.instance and self.instance.cpf:
            self.fields['cpf'].disabled = True
        if self.instance and self.instance.name:
            self.fields['name'].disabled = True
        if self.instance and self.instance.surname:
            self.fields['surname'].disabled = True
        if self.instance and self.instance.cellphone:
            self.fields['cellphone'].disabled = True
