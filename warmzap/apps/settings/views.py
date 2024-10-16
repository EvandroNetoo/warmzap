from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django_htmx.http import HttpResponseClientRedirect

from settings.forms import UserForm


class ProfileSettingsView(View):
    template_name = 'profile_settings.html'
    form_class = UserForm

    def get(self, request: HttpRequest):
        context = {
            'form': self.form_class(instance=request.user),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST, instance=request.user)

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'components/form.html', context)

        form.save()
        return HttpResponseClientRedirect(reverse('profile_settings'))
