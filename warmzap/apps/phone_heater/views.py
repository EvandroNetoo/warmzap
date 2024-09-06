from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request: HttpRequest):
        context = {}
        return render(request, self.template_name, context)
