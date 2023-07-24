from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Announcement


User = get_user_model()


class BaseAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_user(
            username='hamedadmin',
            password='hmdbbgh1011',
            is_staff=True
        )
        cls.user = User.objects.create_user(
            username='hamed',
            password='hmdbbgh1011'
        )
        cls.second_user = User.objects.create_user(
            username='hamed2',
            password='hmdbbgh1011'
        )

    def setUp(self):
        self.announcement = Announcement.objects.create(
            title='Test Announcement',
            content='This is a test announcement.',
            user=self.user,
            accepted=True
        )

        self.unaccepted_announcement = Announcement.objects.create(
            title='Test Announcement',
            content='This is a test announcement.',
            user=self.user,
            accepted=True
        )

    def tearDown(self):
        Announcement.objects.all().delete()


class AnnouncementListViewTest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.list_url = reverse('announcement-list')

    def test_list_announcements_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming only 1 announcement in the database
        self.assertEqual(len(response.data), 1)

    def test_list_announcements_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AnnouncementDetailViewTest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.detail_url = reverse(
            'announcement-detail', args=[self.announcement.id])

    def test_retrieve_announcement_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_announcement_unauthenticated(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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


class AcceptAnnouncementViewTest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.accept_url = reverse(
            'accept-announcement', args=[self.announcement.id])

    def test_accept_announcement_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(self.accept_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.status, 'accepted')

    def test_accept_announcement_as_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.accept_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.announcement.refresh_from_db()
        self.assertNotEqual(self.announcement.status, 'accepted')

    def test_accept_nonexistent_announcement(self):
        self.client.force_authenticate(user=self.admin_user)
        # Assuming 9999 does not exist in the database
        invalid_url = reverse('accept-announcement', args=[9999])
        response = self.client.put(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request(self):
        response = self.client.put(self.accept_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.announcement.refresh_from_db()
        self.assertNotEqual(self.announcement.status, 'accepted')
