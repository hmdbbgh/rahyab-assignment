from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from ..models import Profile
from ..selectors import get_profile
from apps.api.mixins import ApiAuthMixin


User = get_user_model()


class ProfileApi(ApiAuthMixin, APIView):

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ("bio", "announcements_count")

    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(
            self.OutPutSerializer(
                query,
                context={"request": request}
            ).data,
            status=HTTP_200_OK
        )
