from django import forms

from chip_heater.models import Chip


class ChipForm(forms.ModelForm):
    class Meta:
        model = Chip
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Digite o nome'
