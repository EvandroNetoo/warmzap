from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from chip_heater.forms import ChipForm


class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request: HttpRequest):
        context = {
            'chip_form': ChipForm(),
        }
        return render(request, self.template_name, context)
