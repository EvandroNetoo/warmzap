from django import forms

from chip_heater.models import Chip


class ChipForm(forms.ModelForm):
    class Meta:
        model = Chip
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Digite o nome'


class StartHeatingForm(forms.ModelForm):
    class Meta:
        model = Chip
        fields = ['days_to_heat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['days_to_heat'].widget.attrs['placeholder'] = (
            'Digite a quantidade de dias'
        )
        self.fields['days_to_heat'].required = True
