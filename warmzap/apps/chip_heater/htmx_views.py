from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django_htmx.http import HttpResponseClientRefresh

from chip_heater.forms import ChipForm


def generate_wpp_qrcode(request: HttpRequest):
    if request.method == 'POST':
        form = ChipForm(request.POST)

        if not form.is_valid():
            context = {'form': form}
            html = render_to_string('components/form.html', context)
            return HttpResponse(html)

        chip = form.save(commit=False)
        chip.user = request.user
        chip.save()

        messages.success(request, 'Chip adicionado com sucesso.')

        return HttpResponseClientRefresh()
