from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from ..models import Announcement
from ..permissions import IsAnnouncementOwner
from ..validations import validate_no_special_characters
from ..services import (
    create_announcement,
    update_announcement,
    delete_announcement,
    increment_announcement_views_count,
)
from ..selectors import (
    get_announcement,
    get_announcements,
)


class AnnouncementListCreateAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        elif self.request.method == 'POST':
            return (
                IsAuthenticated(),
            )
        return []

    class InputAnnouncementSerializer(serializers.Serializer):

        content = serializers.CharField(
            validators=[validate_no_special_characters]
        )
        title = serializers.CharField(
            validators=[validate_no_special_characters],
            max_length=200
        )

    class OutPutAnnouncementSerializer(serializers.ModelSerializer):

        username = serializers.ReadOnlyField(source="user.username")

        class Meta:
            model = Announcement
            fields = ("title", "content", "username")

    @extend_schema(
        responses=OutPutAnnouncementSerializer
    )
    def get(self, request):

        announcements = get_announcements()
        return Response(
            self.OutPutAnnouncementSerializer(
                announcements,
                context={"request": request},
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=InputAnnouncementSerializer,
        responses=OutPutAnnouncementSerializer
    )
    def post(self, request):
        serializer = self.InputAnnouncementSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        try:
            user = create_announcement(
                user=request.user,
                title=serializer.validated_data.get("title"),
                content=serializer.validated_data.get("content"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            self.OutPutAnnouncementSerializer(
                user,
                context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED
        )


class AnnouncementDetailAPI(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        elif self.request.method in ('PUT', 'DELETE'):
            return (
                [IsAnnouncementOwner()]
            )
        return []

    class InputAnnouncementDetailSerializer(serializers.Serializer):

        content = serializers.CharField(
            validators=[validate_no_special_characters]
        )
        title = serializers.CharField(
            validators=[validate_no_special_characters],
            max_length=200
        )

    class OutPutAnnouncementDetailSerializer(serializers.ModelSerializer):

        username = serializers.ReadOnlyField(source="user.username")

        class Meta:
            model = Announcement
            fields = (
                "title",
                "content",
                "username",
                "created_at",
                "modified_at"
            )

    def get_object(self, announcement_id):
        announcement = get_announcement(pk=announcement_id)
        self.check_object_permissions(
            self.request,
            announcement
        )
        return announcement

    @extend_schema(
        responses=OutPutAnnouncementDetailSerializer
    )
    def get(self, request, announcement_id):
        announcement = self.get_object(announcement_id)
        if not announcement:
            return Response(
                {"message": "Announcement not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        increment_announcement_views_count(pk=announcement_id)
        serializer = self.OutPutAnnouncementDetailSerializer(announcement)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=InputAnnouncementDetailSerializer,
        responses=OutPutAnnouncementDetailSerializer
    )
    def put(self, request, announcement_id):
        announcement = self.get_object(announcement_id)
        if not announcement:
            return Response(
                {"message": "Announcement not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.InputAnnouncementDetailSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        try:
            user = update_announcement(
                announcement=announcement,
                title=serializer.validated_data.get("title"),
                content=serializer.validated_data.get("content"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            self.OutPutAnnouncementDetailSerializer(
                user,
                context={"request": request}
            ).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, announcement_id):
        announcement = self.get_object(announcement_id)
        if not announcement:
            return Response(
                {"message": "Announcement not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if delete_announcement(announcement=announcement):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
