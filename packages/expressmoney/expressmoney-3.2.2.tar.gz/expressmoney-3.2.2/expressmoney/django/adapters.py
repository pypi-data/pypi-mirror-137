from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from google.cloud import secretmanager, secretmanager_v1
from rest_framework_simplejwt.tokens import RefreshToken

from expressmoney import adapters
from expressmoney.adapters import Request

User = get_user_model()
client = secretmanager.SecretManagerServiceClient()
access_secret_version = secretmanager_v1.types.service.AccessSecretVersionRequest()

class DjangoTasks(adapters.Tasks):

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


class DjangoPubSub(adapters.PubSub):

    def __init__(self, topic_id: str, user: Union[None, int, User] = None, project: str = settings.PROJECT):
        user = None if user is None else user if isinstance(user, User) else User.objects.get(pk=user)
        access_token = RefreshToken.for_user(user).access_token if user is not None else None
        super().__init__(topic_id, access_token, project)


class DjangoRequest(Request):

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
        open_id_connect_token = id_token.fetch_id_token(Request(), self._aud)
        iap_token = {'Authorization': f'Bearer {open_id_connect_token}'}
        authorization.update(iap_token)
        return authorization


    @property
    def _aud(self):
        secrets = {
            'expressmoney': 'projects/1086735462412/secrets/IAP_CLIENT_ID/versions/1',
            'expressmoney-dev': 'projects/13337168308/secrets/IAP_CLIENT_ID/versions/1',
            'loans-russia': 'projects/70455559151/secrets/IAP_CLIENT_ID/versions/1',
        }
        access_secret_version.name = secrets.get(self._project, None)
        return client.access_secret_version(request=access_secret_version).payload.data.decode("utf-8")
