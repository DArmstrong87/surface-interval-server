from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from surfaceintervalapi.models import Diver, GearItem, GearSet, GearType
from surfaceintervalapi.types import IMPERIAL_UNIT
from tests.utils import print_test_info, print_assert_that, print_test_action, print_test_setup


class GearSetViewTestCase(TestCase):
    """
    Test the GearSetView API endpoints
    """

    def setUp(self):
        print_test_setup(self)
        self.client = APIClient()

        # Create test user and diver
        self.username = "TestUser"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.diver = Diver.objects.create(
            user=self.user, default_gear_set=None, units=IMPERIAL_UNIT
        )

        # Create test gear type
        self.gear_type = GearType.objects.create(name="Test Gear Type")

        # Create test gear items
        self.gear_item1 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 1", gear_type=self.gear_type
        )
        self.gear_item2 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 2", gear_type=self.gear_type
        )

        # Create test gear set
        self.gear_set = GearSet.objects.create(diver=self.diver, name="Test Gear Set", weight=14)
        self.gear_set.gear_items.set([self.gear_item1, self.gear_item2])

        # Create and set authentication token
        self.client.force_authenticate(user=self.user)

        return super().setUp()

    def test_list_gear_sets(self):
        print_test_info("Testing List Gear Sets Endpoint")

        print_test_action("Making GET request to /gear-sets")
        response = self.client.get("/gear-sets")

        print_assert_that("response status is 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print_assert_that("response contains correct number of gear sets")
        self.assertEqual(len(response.data), 1)
        print_assert_that("response contains correct gear set data")
        gear_set_data = response.data[0]
        self.assertEqual(gear_set_data["name"], "Test Gear Set")
        self.assertEqual(gear_set_data["weight"], 14)
        self.assertEqual(len(gear_set_data["gear_items"]), 2)

    def test_retrieve_gear_set(self):
        print_test_info("Testing Retrieve Gear Set Endpoint")

        print_test_action(f"Making GET request to /gear-sets/{self.gear_set.id}")
        response = self.client.get(f"/gear-sets/{self.gear_set.id}")

        print_assert_that("response status is 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print_assert_that("response contains correct gear set data")
        self.assertEqual(response.data["name"], "Test Gear Set")
        self.assertEqual(response.data["weight"], 14)
        self.assertEqual(len(response.data["gear_items"]), 2)

    def test_create_gear_set(self):
        print_test_info("Testing Create Gear Set Endpoint")

        print_test_action("Creating new gear items")
        gear_item3 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 3", gear_type=self.gear_type
        )
        gear_item4 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 4", gear_type=self.gear_type
        )

        print_test_action("Making POST request to /gear-sets")
        new_gear_set_data = {
            "name": "New Gear Set",
            "weight": 15,
            "gearItemIds": [gear_item3.id, gear_item4.id],
        }
        response = self.client.post("/gear-sets", new_gear_set_data, format="json")

        print_assert_that("response status is 201")
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Error response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print_assert_that("response contains correct gear set data")
        self.assertEqual(response.data["name"], "New Gear Set")
        self.assertEqual(response.data["weight"], 15.0)
        self.assertEqual(len(response.data["gear_items"]), 2)

    def test_update_gear_set(self):
        print_test_info("Testing Update Gear Set Endpoint")

        print_test_action("Creating new gear item")
        gear_item3 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 3", gear_type=self.gear_type
        )

        print_test_action(f"Making PUT request to /gear-sets/{self.gear_set.id}")
        update_data = {
            "name": "Updated Gear Set",
            "weight": 20.0,
            "gearItemIds": [self.gear_item1.id, gear_item3.id],
        }
        response = self.client.put(f"/gear-sets/{self.gear_set.id}", update_data, format="json")

        print_assert_that("response status is 204")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print_assert_that("gear set is updated in database")
        updated_gear_set = GearSet.objects.get(pk=self.gear_set.id)
        self.assertEqual(updated_gear_set.name, "Updated Gear Set")
        self.assertEqual(updated_gear_set.weight, 20.0)
        self.assertEqual(updated_gear_set.gear_items.count(), 2)
        self.assertIn(gear_item3, updated_gear_set.gear_items.all())

    def test_delete_gear_set(self):
        print_test_info("Testing Delete Gear Set Endpoint")

        print_test_action(f"Making DELETE request to /gear-sets/{self.gear_set.id}")
        response = self.client.delete(f"/gear-sets/{self.gear_set.id}")

        print_assert_that("response status is 204")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print_assert_that("gear set is deleted from database")
        with self.assertRaises(GearSet.DoesNotExist):
            GearSet.objects.get(pk=self.gear_set.id)
        print_assert_that("gear items still exist")
        self.assertTrue(GearItem.objects.filter(pk=self.gear_item1.id).exists())
        self.assertTrue(GearItem.objects.filter(pk=self.gear_item2.id).exists())

    def test_unauthorized_access(self):
        print_test_info("Testing Unauthorized Access")

        print_test_action("Creating new user without authentication")
        new_user = User.objects.create_user(username="NewUser", password="newpass123")
        _ = Diver.objects.create(user=new_user, default_gear_set=None, units=IMPERIAL_UNIT)

        print_test_action("Making GET request to /gear-sets without authentication")
        self.client.force_authenticate(user=None)
        response = self.client.get("/gear-sets")

        print_assert_that("response status is 401")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_user_access(self):
        print_test_info("Testing Wrong User Access")

        print_test_action("Creating new user")
        new_user = User.objects.create_user(username="NewUser", password="newpass123")
        _ = Diver.objects.create(user=new_user, default_gear_set=None, units=IMPERIAL_UNIT)

        print_test_action("Authenticating as new user")
        self.client.force_authenticate(user=new_user)

        print_test_action(f"Making GET request to /gear-sets/{self.gear_set.id}")
        response = self.client.get(f"/gear-sets/{self.gear_set.id}")

        print_assert_that("response status is 404")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print_assert_that("response contains error message")
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "GearSet matching query does not exist.")
