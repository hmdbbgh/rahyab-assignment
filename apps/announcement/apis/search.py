from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ..models import Announcement
from ..selectors import (
    get_announcements,
    search_announcements
)


class AnnouncementSearchAPI(APIView):

    class OutPutAnnouncementSearchSerializer(serializers.ModelSerializer):

        username = serializers.ReadOnlyField(source="user.username")

        class Meta:
            model = Announcement
            fields = ("title", "content", "username")

    @extend_schema(
        responses=OutPutAnnouncementSearchSerializer
    )
    def get(self, request):

        search_query = request.query_params.get('q', '')
        if search_query:
            announcements = search_announcements(
                search_text=search_query
            )
        else:
            announcements = get_announcements()

        return Response(
            self.OutPutAnnouncementSearchSerializer(
                announcements,
                context={"request": request},
                many=True
            ).data,
            status=status.HTTP_200_OK
        )
