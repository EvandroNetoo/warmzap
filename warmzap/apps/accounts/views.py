from asgiref.sync import sync_to_async
from django.contrib.auth import alogin, logout
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django_htmx.http import HttpResponseClientRedirect

from accounts.forms import SignInForm, SignUpForm


@method_decorator(login_not_required, 'dispatch')
class SignUpView(View):
    template_name = 'signup.html'
    form_class = SignUpForm

    async def get(self, request: HttpRequest):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    async def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not await sync_to_async(form.is_valid)():
            context = {
                'form': form,
            }
            return render(request, 'components/form.html', context)

        user = await form.asave()

        await alogin(request, user)
        return HttpResponseClientRedirect(reverse('dashboard'))


@method_decorator(login_not_required, 'dispatch')
class SignInView(View):
    template_name = 'signin.html'
    form_class = SignInForm

    async def get(self, request: HttpRequest):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    async def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not await sync_to_async(form.is_valid)():
            context = {
                'form': form,
            }
            return render(request, 'components/form.html', context)

        await alogin(request, form.user)

        redirect_url = request.GET.get('next')

        return HttpResponseClientRedirect(
            redirect_url if redirect_url else reverse('dashboard')
        )


class SignOutView(View):
    redirect_url = reverse_lazy('signin')

    async def post(self, request: HttpRequest):
        await sync_to_async(logout)(request)
        return HttpResponseClientRedirect(self.redirect_url)
