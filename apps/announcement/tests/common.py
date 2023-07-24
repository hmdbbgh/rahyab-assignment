from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.announcement.models import Announcement


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

    def setUp(self):
        self.announcement = Announcement.objects.create(
            title='Test Announcement',
            content='This is a test announcement.',
            user=self.user,
            accepted=True
        )
        self.unaccepted_announcement = Announcement.objects.create(
            title='Test Unaccepted Announcement',
            content='This is a test unaccepted  announcement.',
            user=self.user,
            accepted=False
        )

    def tearDown(self):
        Announcement.objects.all().delete()
