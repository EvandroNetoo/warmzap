from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from chip_heater.forms import ChipForm, StartHeatingForm
from chip_heater.models import Chip


class DashboardView(View):
    template_name = 'dashboard.html'

    async def get(self, request: HttpRequest):
        chips = Chip.objects.filter(user=request.user)

        chips_counts = await chips.aaggregate(
            not_started_count=Count(
                'id', filter=Q(stage=Chip.StageChoices.NOT_STARTED)
            ),
            started_count=Count(
                'id', filter=Q(stage=Chip.StageChoices.STARTED)
            ),
            completed_count=Count(
                'id', filter=Q(stage=Chip.StageChoices.COMPLETED)
            ),
            banned_count=Count('id', filter=Q(stage=Chip.StageChoices.BANNED)),
        )

        context = {
            'StageChoices': Chip.StageChoices,
            'chips': [chip async for chip in chips],
            'chips_counts': chips_counts,
            'chip_form': ChipForm(),
        }
        return render(request, self.template_name, context)


class MyChipsView(View):
    template_name = 'my_chips.html'

    async def get(self, request: HttpRequest):
        chips = Chip.objects.filter(user=request.user)

        context = {
            'StageChoices': Chip.StageChoices,
            'chips': [chip async for chip in chips],
            'chip_form': ChipForm(),
            'start_heating_form': StartHeatingForm(),
        }
        return render(request, self.template_name, context)
