from django.http import HttpRequest
from django.shortcuts import aget_object_or_404, render
from django.views import View
from django_htmx.http import HttpResponseClientRefresh

from chip_heater.forms import StartHeatingForm
from chip_heater.models import Chip
from chip_heater.tasks import send_message_and_schedule_next


class StartHeatingView(View):
    form_class = StartHeatingForm

    async def post(self, request: HttpRequest, chip_pk: str):
        chip = await aget_object_or_404(Chip, pk=chip_pk, user=request.user)
        form = self.form_class(request.POST, instance=chip)

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'components/form.html', context)

        started_chips = request.user.chips.filter(
            stage=Chip.StageChoices.STARTED
        )
        if await started_chips.acount() >= request.user.started_chips_limit:
            form.add_error(
                None,
                f'Melhore o seu plano para aquecer mais de {request.user.started_chips_limit} números simultaneamente',
            )
            context = {'form': form}
            return render(request, 'components/form.html', context)

        form.instance.stage = Chip.StageChoices.STARTED
        form.instance.heated_days = 0

        await form.instance.asave()

        send_message_and_schedule_next.delay(form.instance.pk)

        return HttpResponseClientRefresh()
