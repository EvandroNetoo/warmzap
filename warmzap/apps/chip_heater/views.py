import json

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import render
from django.views import View

from chip_heater.forms import ChipForm
from chip_heater.models import Chip
from chip_heater.whatsapp_web import LoginQRcode, WhatsappWeb


class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request: HttpRequest):
        chips = Chip.objects.filter(user=request.user)

        chips_counts = chips.aggregate(
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

        not_started_chips = chips.filter(stage=Chip.StageChoices.NOT_STARTED)
        started_chips = chips.filter(stage=Chip.StageChoices.STARTED)
        completed_chips = chips.filter(stage=Chip.StageChoices.COMPLETED)
        banned_chips = chips.filter(stage=Chip.StageChoices.BANNED)

        context = {
            'not_started_chips': not_started_chips,
            'started_chips': started_chips,
            'completed_chips': completed_chips,
            'banned_chips': banned_chips,
            'chips_counts': chips_counts,
            'chip_form': ChipForm(),
        }
        return render(request, self.template_name, context)


class MyChipsView(View):
    template_name = 'my_chips.html'

    def get(self, request: HttpRequest):
        context = {}
        return render(request, self.template_name, context)


def generate_qrcode(request: HttpRequest):
    whatsapp_web = WhatsappWeb()
    payload = json.loads(request.body)

    def stream():
        success = False
        for error, data in whatsapp_web.generate_login_qrcode():
            if isinstance(data, LoginQRcode):
                yield f'data:image/png;base64{data.b64_qrcode}\n'
            else:
                if error:
                    yield data
                    break

                yield """
                    <span class="loading loading-spinner loading-lg text-slate-500"></span>
                    <span class="text-green-400">Sincronizando dados.</span>
                """
                Chip.objects.create(
                    name=payload.get('name'),
                    number=data,
                    user=request.user,
                    directory_token=whatsapp_web.directory_token,
                )
                success = True
        if success:
            messages.success(request, 'Número adicionado com sucesso.')

    return StreamingHttpResponse(stream())
