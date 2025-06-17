from django.test import TestCase
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from surfaceintervalapi.models import Diver
from surfaceintervalapi.types import IMPERIAL_UNIT
from tests.utils import print_test_action, print_test_setup


class SiBaseTestCase(TestCase):
    def setUp(self):
        cache.clear()

        print_test_setup(self)
        self.client = APIClient()

        print_test_action("Creating test user for SI Base Test Case")
        self.user = User.objects.create_user(
            username="TestUser", email="test@example.com", password="123"
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")

        print_test_action("Creating test diver for SI Base Test Case")
        self.diver = Diver.objects.create(
            user=self.user, default_gear_set=None, units=IMPERIAL_UNIT
        )

    def test_setup(self):
        self.assertTrue(User.objects.filter(username="TestUser").exists())
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        self.assertTrue(Diver.objects.filter(user=self.user).exists())
        self.assertTrue(self.diver.user == self.user)
        self.assertTrue(self.diver.units == IMPERIAL_UNIT)
        self.assertTrue(self.diver.default_gear_set is None)

    def tearDown(self):
        self.user.delete()
        self.diver.delete()
        super().tearDown()
