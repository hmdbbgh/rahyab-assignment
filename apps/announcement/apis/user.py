from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from ..models import Announcement
from ..selectors import get_user_announcements


class UserAnnouncementsAPI(APIView):

    permission_classes = [IsAuthenticated]

    class OutPutUserAnnouncementSerializer(serializers.ModelSerializer):

        class Meta:
            model = Announcement
            fields = ("title", "content", "accepted")

    @extend_schema(
        responses=OutPutUserAnnouncementSerializer
    )
    def get(self, request):

        return Response(
            self.OutPutUserAnnouncementSerializer(
                get_user_announcements(user=request.user),
                context={"request": request},
                many=True
            ).data,
            status=status.HTTP_200_OK
        )
