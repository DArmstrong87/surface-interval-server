from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from surfaceintervalapi.models import Diver
from surfaceintervalapi.types import IMPERIAL_UNIT
from tests.utils import print_test_info, print_assert_that, print_test_action, print_test_setup


class SiBaseTestCase(TestCase):
    def setUp(self):
        print_test_setup(self)
        self.client = APIClient()

        print_test_action("Creating test user for SI Base Test Case")
        self.user = User.objects.create_user(username="TestUser", password="123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        print_test_action("Creating test diver for SI Base Test Case")
        self.diver = Diver.objects.create(
            user=self.user, default_gear_set=None, units=IMPERIAL_UNIT
        )

    def test_setup(self):
        print_test_info("Testing SI Base Test Case Setup")
        print_assert_that("Test user was created")
        self.assertTrue(User.objects.filter(username="TestUser").exists())
        print_assert_that("Test diver was created")
        self.assertTrue(Diver.objects.filter(user=self.user).exists())

    def tearDown(self):
        self.user.delete()
        self.token.delete()
        self.diver.delete()
        super().tearDown()
