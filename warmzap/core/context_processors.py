from django.http import HttpRequest


def sidebar(request: HttpRequest):
    dashboard_urls = {'dashboard'}
    my_chips_urls = {'my_chips'}

    actual_url_name = request.resolver_match.url_name

    if actual_url_name in dashboard_urls:
        active_url = 'dashboard'
    if actual_url_name in my_chips_urls:
        active_url = 'my_chips'

    return {
        'sidebar_collapsed': request.COOKIES.get('sidebarCollapsed'),
        'active_url': active_url,
    }
