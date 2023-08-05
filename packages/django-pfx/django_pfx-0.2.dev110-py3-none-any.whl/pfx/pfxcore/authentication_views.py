import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse

import jwt
from django_request_mapping import request_mapping

from pfx.pfxcore.exceptions import AuthenticationError
from pfx.pfxcore.views import BaseRestView, BodyMixin, rest_api

logger = logging.getLogger(__name__)


@request_mapping("/auth")
class AuthenticationView(BodyMixin, BaseRestView):

    @rest_api("/login", method="post")
    def login(self, request, *args, **kwargs):
        data = self.deserialize_body(self.request)
        user = authenticate(request, username=data['username'],
                            password=data['password'])
        if user is not None:
            return JsonResponse({
                'token': self._prepare_token(user)
            })
        raise AuthenticationError()

    @rest_api("/change-password", method="post")
    def change_password(self, request, *args, **kwargs):
        if self.request.user and self.request.user.is_authenticated:
            data = self.deserialize_body(self.request)
            user = authenticate(request,
                                username=self.request.user.get_username(),
                                password=data['old_password'])
            if user is not None:
                user.set_password(data['new_password'])
                user.save()
                return JsonResponse({
                    'message': 'password updated successfully'
                })
        raise AuthenticationError()

    def _prepare_token(self, user):
        payload = {
            'pfx_user_pk': user.pk,
        }
        if settings.PFX_TOKEN_VALIDITY:
            exp = datetime.utcnow() + timedelta(**settings.PFX_TOKEN_VALIDITY)
            payload.update(exp=exp)
        payload.update(self.get_extra_payload(user))
        return jwt.encode(
            payload, settings.PFX_SECRET_KEY, algorithm="HS256")

    def get_extra_payload(self, user):
        return {}
