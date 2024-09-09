from django import forms

from chip_heater.models import Chip


class ChipForm(forms.ModelForm):
    class Meta:
        model = Chip
        fields = ['number', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['number'].widget.attrs['placeholder'] = 'Digite o número'
        self.fields['name'].widget.attrs['placeholder'] = 'Digite o nome'

        self.fields['number'].widget.attrs['oninput'] = 'cellphoneMask(this)'
