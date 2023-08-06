"""
Utils for Django, DRF frameworks.
"""


from django.conf import settings


def get_ip(request):
    """Get client ip from header"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


def get_http_referer(request):
    """Get client referer from header"""
    http_referer = request.META.get('HTTP_REFERER')
    http_host = request.META.get('HTTP_HOST')
    return http_referer if http_referer else http_host


def allowed_ip(request):
    """Check client ip by white list"""
    user_ip = get_ip(request)

    for allow_ip in settings.ALLOWED_IP:
        if user_ip == allow_ip or user_ip.startswith(allow_ip):
            return True
    return False
