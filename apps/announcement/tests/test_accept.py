from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from .common import BaseAPITest

User = get_user_model()


class TestAnnouncementAcceptAPI(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.accept_url = reverse(
            'api:announcement:accept',
            args=[self.announcement.id]
        )
        self.accept_url_fake = reverse(
            'api:announcement:accept',
            args=[10000]
        )

    def test_accpet_announcement_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.accept_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_accpet_announcement_admin_not_found(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.accept_url_fake)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_accpet_announcement_not_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.accept_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_accpet_announcement_unauthenticated(self):
        response = self.client.post(self.accept_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
