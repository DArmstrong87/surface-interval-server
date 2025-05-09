from django.test import TestCase
from django.contrib.auth.models import User
from surfaceintervalapi.models import Diver
from surfaceintervalapi.types import IMPERIAL_UNIT
from tests.utils import print_test_info


class DiverTestCase(TestCase):
    """
    Test creation of User and Diver
    """

    def setUp(self):
        self.username = "TestUser"
        self.first_name = "Test"
        self.last_name = "User"

        return super().setUp()

    def test_create_user_and_diver(self):
        print_test_info("Testing User and Diver Creation")
        user = User.objects.create(
            username=self.username, first_name=self.first_name, last_name=self.last_name
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)

        diver = Diver.objects.create(user=user, default_gear_set=None, units=IMPERIAL_UNIT)

        self.assertIsNotNone(diver)
        self.assertEqual(diver.user, user)
        self.assertEqual(diver.units, IMPERIAL_UNIT)
