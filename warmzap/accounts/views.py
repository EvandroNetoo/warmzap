from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required


@method_decorator(login_not_required, "dispatch")
class SignInView(View):
    template_name = "signin.html"

    def get(self, request: HttpRequest):
        return render(request, self.template_name)
