from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..selectors import get_announcement_views_count


class AnnouncementViewsCountAPI(APIView):

    def get(self, request, announcement_id):

        views_count = get_announcement_views_count(pk=announcement_id)

        if views_count is None:
            return Response(
                {"message": "Announcement not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"views_count": views_count},
            status=status.HTTP_200_OK
        )
