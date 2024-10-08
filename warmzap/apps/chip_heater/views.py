import json
import os
import shutil
from secrets import token_hex

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.core.files import File
from django.db.models import Count, Q
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import render
from django.views import View

from chip_heater.forms import ChipForm
from chip_heater.models import Chip
from chip_heater.tasks import send_message_and_schedule_next
from chip_heater.whatsapp_web import LoginQRCode, WhatsAppWeb


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


def generate_qrcode(request: HttpRequest):
    directory_token = token_hex(16)
    profile_dir_path = settings.BASE_DIR / f'wpp_sessions/{directory_token}'

    whatsapp_web = WhatsAppWeb(profile_dir_path)
    payload = json.loads(request.body)

    def stream():
        success = False
        generator = whatsapp_web.generate_login_qrcode(
            directory_token, profile_dir_path
        )
        for error, data in generator:
            if isinstance(data, LoginQRCode):
                yield f'data:image/png;base64{data.b64_qrcode}\n'
            else:
                if error:
                    yield data
                    break

                yield """
                    <span class="loading loading-spinner loading-lg text-slate-500"></span>
                    <span class="text-green-400">Sincronizando dados.</span>
                """
                chip_instance = Chip(
                    name=payload.get('name'),
                    number=next(generator),
                    user=request.user,
                )
                zip_file = shutil.make_archive(
                    whatsapp_web.profile_dir_path,
                    'zip',
                    whatsapp_web.profile_dir_path,
                )
                with open(zip_file, 'rb') as f:
                    chip_instance.browser_profile = File(
                        f, name=os.path.basename(zip_file)
                    )
                    chip_instance.save()
                os.remove(zip_file)
                shutil.rmtree(whatsapp_web.profile_dir_path)
                success = True
        if success:
            messages.success(request, 'Número adicionado com sucesso.')

    return StreamingHttpResponse(stream())
