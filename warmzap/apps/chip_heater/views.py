import json
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import render
from django.views import View

from chip_heater.forms import ChipForm
from core.settings import BASE_DIR
from chip_heater.whatsapp_web import WhatsappWeb, LoginQRcode
from chip_heater.models import Chip
from django.contrib import messages
from django.contrib.messages import get_messages

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request: HttpRequest):
        context = {
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
                yield f"data:image/png;base64{data.b64_qrcode}\n"
            else:
                if error:
                    yield data
                    break

                yield f'''
                    <span class="loading loading-spinner loading-lg text-slate-500"></span>
                    <span class="text-green-400">Sincronizando dados.</span>
                '''
                Chip.objects.create(
                    name=payload.get('name'),
                    number=data,
                    user=request.user,
                )
                success = True
        if success:
            messages.success(request, "Número adicionado com sucesso.")
            print([i for i in get_messages(request)])

    return StreamingHttpResponse(stream())


