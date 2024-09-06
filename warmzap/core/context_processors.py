from django.http import HttpRequest


def sidebar(request: HttpRequest):
    return {'sidebar_collapsed': request.COOKIES.get('sidebarCollapsed')}
