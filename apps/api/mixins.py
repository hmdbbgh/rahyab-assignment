from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from typing import (
    Type,
    Sequence,
)
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = (
        JWTAuthentication,
    )
    permission_classes: Sequence[Type[BasePermission]] = (
        IsAuthenticated,
    )
