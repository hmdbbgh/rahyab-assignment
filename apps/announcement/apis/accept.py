from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from ..selectors import get_announcement


class AnnouncementAcceptAPI(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, announcement_id):

        announcement = get_announcement(pk=announcement_id)
        if not announcement:
            return Response(
                {"message": "Announcement not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        announcement.accepted = True
        announcement.save()
        return Response(
            {'message': 'Announcement accepted successfully.'},
            status=status.HTTP_200_OK
        )
