from rest_framework import status
from surfaceintervalapi.models import GearItem, GearType, CustomGearType
from tests.si_base_test_case import SiBaseTestCase
from tests.utils import print_test_info, print_assert_that, print_test_action


class TestGearItemView(SiBaseTestCase):
    def setUp(self):
        super().setUp()

        print_test_action("Creating test gear type")
        self.gear_type = GearType.objects.create(name="Test Gear Type")

        print_test_action("Creating test custom gear type")
        self.custom_gear_type = CustomGearType.objects.create(
            diver=self.diver, name="Test Custom Gear Type"
        )

        print_test_action("Creating test gear item")
        self.gear_item = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item", gear_type=self.gear_type
        )

    def test_list_gear_items(self):
        print_test_info("Testing list gear items endpoint")
        response = self.client.get("/gear-items")

        print_assert_that("Response status code is 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print_assert_that("Response contains the created gear item")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Gear Item")

    def test_retrieve_gear_item(self):
        print_test_info("Testing retrieve gear item endpoint")
        response = self.client.get(f"/gear-items/{self.gear_item.id}")

        print_assert_that("Response status code is 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print_assert_that("Response contains correct gear item data")
        self.assertEqual(response.data["name"], "Test Gear Item")

    def test_create_gear_item_with_gear_type(self):
        print_test_info("Testing create gear item with gear type")
        data = {
            "name": "New Gear Item",
            "gearTypeId": self.gear_type.id,
            "customGearTypeId": None,
            "newCustomGearType": None,
        }
        response = self.client.post("/gear-items", data, format="json")

        print_assert_that("Response status code is 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print_assert_that("Gear item was created with correct data")
        self.assertEqual(response.data["name"], "New Gear Item")
        self.assertEqual(GearItem.objects.count(), 2)

    def test_create_gear_item_with_custom_gear_type(self):
        print_test_info("Testing create gear item with custom gear type")
        data = {
            "name": "New Custom Gear Item",
            "gearTypeId": None,
            "customGearTypeId": self.custom_gear_type.id,
            "newCustomGearType": None,
        }
        response = self.client.post("/gear-items", data, format="json")

        print_assert_that("Response status code is 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print_assert_that("Gear item was created with correct data")
        self.assertEqual(response.data["name"], "New Custom Gear Item")
        self.assertEqual(GearItem.objects.count(), 2)

    def test_create_gear_item_with_new_custom_gear_type(self):
        print_test_info("Testing create gear item with new custom gear type")
        data = {
            "name": "New Custom Type Gear Item",
            "gearTypeId": None,
            "customGearTypeId": None,
            "newCustomGearType": "Brand New Custom Type",
        }
        response = self.client.post("/gear-items", data, format="json")

        print_assert_that("Response status code is 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print_assert_that("Gear item was created with correct data")
        self.assertEqual(response.data["name"], "New Custom Type Gear Item")
        self.assertEqual(GearItem.objects.count(), 2)
        self.assertEqual(CustomGearType.objects.count(), 2)

    def test_update_gear_item(self):
        print_test_info("Testing update gear item endpoint")
        data = {
            "name": "Updated Gear Item",
            "gearTypeId": self.gear_type.id,
            "customGearTypeId": None,
            "newCustomGearType": "",
        }
        response = self.client.put(f"/gear-items/{self.gear_item.id}", data, format="json")

        print_assert_that("Response status code is 204")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print_assert_that("Gear item was updated")
        updated_item = GearItem.objects.get(pk=self.gear_item.id)
        self.assertEqual(updated_item.name, "Updated Gear Item")

    def test_delete_gear_item(self):
        print_test_info("Testing delete gear item endpoint")
        response = self.client.delete(f"/gear-items/{self.gear_item.id}")

        print_assert_that("Response status code is 204")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print_assert_that("Gear item was deleted")
        self.assertEqual(GearItem.objects.count(), 0)

    def tearDown(self):
        self.gear_item.delete()
        self.gear_type.delete()
        self.custom_gear_type.delete()
        super().tearDown()
