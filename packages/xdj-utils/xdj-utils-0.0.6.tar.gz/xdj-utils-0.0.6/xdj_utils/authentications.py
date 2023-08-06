from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication

try:
    RoleModel = apps.get_model(*(getattr(settings, 'ROLE_MODEL', ('xdj_system.Role')).split('.')))
except Exception:
    RoleModel = None


class AnonymousAuthenticated(BaseAuthentication):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if not user or user.is_anonymous:
            user = AnonymousUser()
            user.role = RoleModel.objects.filter(id__in=settings.ANONYMOUS_ROLE or [])
        return (user, None)

