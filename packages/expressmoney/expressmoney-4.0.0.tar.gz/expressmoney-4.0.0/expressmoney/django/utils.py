"""
Utils for Django, DRF frameworks.
"""
from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from expressmoney import utils


User = get_user_model()


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


class DjangoTasks(utils.Tasks):

    def __init__(self,
                 service: str = 'default',
                 path: str = '/',
                 user: Union[None, int, User] = None,
                 project: str = settings.PROJECT,
                 queue: str = 'attempts-1',
                 location: str = 'europe-west1',
                 in_seconds: int = None):
        user = None if user is None else user if isinstance(user, User) else User.objects.get(pk=user)
        access_token = RefreshToken.for_user(user).access_token if user is not None else None
        super().__init__(service, path, access_token, project, queue, location, in_seconds)


class DjangoPubSub(utils.PubSub):

    def __init__(self, topic_id: str, user: Union[None, int, User] = None, project: str = settings.PROJECT):
        user = None if user is None else user if isinstance(user, User) else User.objects.get(pk=user)
        access_token = RefreshToken.for_user(user).access_token if user is not None else None
        super().__init__(topic_id, access_token, project)


class DjangoRequest(utils.Request):

    def __init__(self,
                 service: str = None,
                 path: str = '/',
                 user: Union[None, int, User] = None,
                 project: str = 'expressmoney',
                 timeout: tuple = (30, 30),
                 ):
        user = None if user is None else user if isinstance(user, User) else User.objects.get(pk=user)
        access_token = RefreshToken.for_user(user).access_token if user is not None else None
        super().__init__(service, path, access_token, project, timeout)

    def _get_authorization(self) -> dict:
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token
        authorization = super()._get_authorization()
        open_id_connect_token = id_token.fetch_id_token(Request(), settings.IAP_CLIENT_ID)
        iap_token = {'Authorization': f'Bearer {open_id_connect_token}'}
        authorization.update(iap_token)
        return authorization
