from asgiref.sync import sync_to_async
from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from chip_heater.forms import ChipForm
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
            'StageChoices': Chip.StageChoices.NOT_STARTED,
            'chips': chips,
            'chips_counts': chips_counts,
            'chip_form': ChipForm(),
        }
        return await sync_to_async(render)(
            request, self.template_name, context
        )


class MyChipsView(View):
    template_name = 'my_chips.html'

    def get(self, request: HttpRequest):
        context = {}
        return render(request, self.template_name, context)
