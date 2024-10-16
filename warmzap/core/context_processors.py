from django.http import HttpRequest


def sidebar(request: HttpRequest):
    dashboard_urls = {'dashboard'}
    my_chips_urls = {'my_chips'}
    settings_urls = {'profile_settings'}

    actual_url_name = request.resolver_match.url_name

    active_url = ''
    if actual_url_name in dashboard_urls:
        active_url = 'dashboard'
    if actual_url_name in my_chips_urls:
        active_url = 'my_chips'
    if actual_url_name in settings_urls:
        active_url = 'settings'

    return {
        'sidebar_collapsed': request.COOKIES.get('sidebarCollapsed'),
        'active_url': active_url,
    }
