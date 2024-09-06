from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django_htmx.http import HttpResponseClientRedirect

from accounts.forms import SignInForm, SignUpForm


@method_decorator(login_not_required, 'dispatch')
class SignUpView(View):
    template_name = 'signup.html'
    form_class = SignUpForm

    def get(self, request: HttpRequest):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'components/form.html', context)

        user = form.save()
        login(request, user)
        return HttpResponseClientRedirect(reverse('dashboard'))


@method_decorator(login_not_required, 'dispatch')
class SignInView(View):
    template_name = 'signin.html'
    form_class = SignInForm

    def get(self, request: HttpRequest):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'components/form.html', context)

        login(request, form.user)

        redirect_url = request.GET.get('next')

        return HttpResponseClientRedirect(
            redirect_url if redirect_url else reverse('dashboard')
        )
