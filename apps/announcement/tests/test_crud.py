from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from .common import BaseAPITest
from apps.announcement.models import Announcement


User = get_user_model()


class TestAnnouncementListCreateAPI(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.create_list_url = reverse('api:announcement:create-list')
        self.data = {
            'title': 'Test valid title',
            'content': 'This is the test valid content.'
        }
        self.invalid_data = {
            'title': 'Test invalid title',
            'content': 'This is the test invalid / content.'
        }

    def test_list_announcements_authenticated(self):

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.create_list_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    def test_list_announcements_unauthenticated(self):

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.create_list_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    def test_create_announcements_unauthenticated(self):
        response = self.client.post(self.create_list_url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_create_announcements_authenticated(self):

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_list_url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        actual_data = response.json()
        self.assertEqual(actual_data["username"], self.user.username)
        self.assertEqual(actual_data["title"], self.data["title"])
        self.assertEqual(actual_data["content"], self.data["content"])

    def test_create_announcements_authenticated_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_list_url, self.invalid_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class TestAnnouncementDetailAPI(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.detail_url = reverse(
            'api:announcement:detail',
            args=[self.announcement.id]
        )
        self.data = {
            "title": 'Test Announcement',
            "content": 'This is a test announcement.'
        }

    def test_retrieve_announcement_authenticated(self):

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        actual_data = response.json()
        self.assertEqual(actual_data["username"], self.user.username)
        self.assertEqual(actual_data["title"], self.data["title"])
        self.assertEqual(actual_data["content"], self.data["content"])

    def test_retrieve_announcement_unauthenticated(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        actual_data = response.json()
        self.assertEqual(actual_data["username"], self.user.username)
        self.assertEqual(actual_data["title"], self.data["title"])
        self.assertEqual(actual_data["content"], self.data["content"])

    def test_update_announcement_authenticated_owner(self):

        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Announcement',
                'content': 'This is the updated announcement.'}
        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.title, 'Updated Announcement')

    def test_update_announcement_authenticated_non_owner(self):

        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'Updated Announcement',
                'content': 'This is the updated announcement.'}
        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.announcement.refresh_from_db()
        self.assertNotEqual(self.announcement.title, 'Updated Announcement')

    def test_delete_announcement_authenticated_owner(self):

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Announcement.objects.filter(
            pk=self.announcement.id).exists())

    def test_delete_announcement_authenticated_non_owner(self):

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Announcement.objects.filter(
            pk=self.announcement.id).exists())
