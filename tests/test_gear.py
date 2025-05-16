from django.test import TestCase
from django.contrib.auth.models import User
from surfaceintervalapi.models import Diver, GearItem, GearSet, GearType, CustomGearType
from surfaceintervalapi.types import IMPERIAL_UNIT
from tests.utils import print_test_info, print_assert_that, print_test_action, print_test_setup


class GearTestCase(TestCase):
    """
    Test creation and management of GearItems and GearSets
    """

    def setUp(self):
        print_test_setup(self)
        self.username = "TestUser"
        self.first_name = "Test"
        self.last_name = "User"

        # Create test user and diver
        self.user = User.objects.create(
            username=self.username, first_name=self.first_name, last_name=self.last_name
        )
        self.diver = Diver.objects.create(
            user=self.user, default_gear_set=None, units=IMPERIAL_UNIT
        )

        # Create test gear type
        self.gear_type = GearType.objects.create(name="Test Gear Type")

        return super().setUp()

    def test_create_gear_item_with_gear_type(self):
        print_test_info("Testing GearItem Creation with GearType")

        print_test_action("Creating GearItem with GearType")
        gear_item = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item", gear_type=self.gear_type
        )

        print_assert_that("GearItem is created")
        self.assertIsNotNone(gear_item)
        print_assert_that("GearItem properties match")
        self.assertEqual(gear_item.name, "Test Gear Item")
        self.assertEqual(gear_item.gear_type, self.gear_type)
        self.assertEqual(gear_item.diver, self.diver)
        self.assertIsNone(gear_item.custom_gear_type)

    def test_create_gear_item_with_custom_gear_type(self):
        print_test_info("Testing GearItem Creation with CustomGearType")

        print_test_action("Creating CustomGearType")
        custom_gear_type = CustomGearType.objects.create(
            diver=self.diver, name="Test Custom Gear Type"
        )

        print_test_action("Creating GearItem with CustomGearType")
        gear_item = GearItem.objects.create(
            diver=self.diver, name="Test Custom Gear Item", custom_gear_type=custom_gear_type
        )

        print_assert_that("GearItem is created")
        self.assertIsNotNone(gear_item)
        print_assert_that("GearItem properties match")
        self.assertEqual(gear_item.name, "Test Custom Gear Item")
        self.assertEqual(gear_item.custom_gear_type, custom_gear_type)
        self.assertEqual(gear_item.diver, self.diver)
        self.assertIsNone(gear_item.gear_type)

    def test_create_gear_set(self):
        print_test_info("Testing GearSet Creation")

        print_test_action("Creating GearItems")
        gear_item1 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 1", gear_type=self.gear_type
        )
        gear_item2 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 2", gear_type=self.gear_type
        )

        print_test_action("Creating GearSet")
        gear_set = GearSet.objects.create(diver=self.diver, name="Test Gear Set", weight=10.5)
        gear_set.gear_items.set([gear_item1, gear_item2])

        print_assert_that("GearSet is created")
        self.assertIsNotNone(gear_set)
        print_assert_that("GearSet properties match")
        self.assertEqual(gear_set.name, "Test Gear Set")
        self.assertEqual(gear_set.weight, 10.5)
        self.assertEqual(gear_set.diver, self.diver)
        print_assert_that("GearSet contains correct gear items")
        self.assertEqual(gear_set.gear_items.count(), 2)
        self.assertIn(gear_item1, gear_set.gear_items.all())
        self.assertIn(gear_item2, gear_set.gear_items.all())

    def test_update_gear_set(self):
        print_test_info("Testing GearSet Update")

        print_test_action("Creating initial GearSet")
        gear_item1 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 1", gear_type=self.gear_type
        )
        gear_set = GearSet.objects.create(diver=self.diver, name="Initial Gear Set", weight=10.5)
        gear_set.gear_items.set([gear_item1])

        print_test_action("Creating new GearItem")
        gear_item2 = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item 2", gear_type=self.gear_type
        )

        print_test_action("Updating GearSet")
        gear_set.name = "Updated Gear Set"
        gear_set.weight = 15.0
        gear_set.gear_items.set([gear_item1, gear_item2])
        gear_set.save()

        print_assert_that("GearSet is updated")
        updated_gear_set = GearSet.objects.get(pk=gear_set.pk)
        self.assertEqual(updated_gear_set.name, "Updated Gear Set")
        self.assertEqual(updated_gear_set.weight, 15.0)
        self.assertEqual(updated_gear_set.gear_items.count(), 2)
        self.assertIn(gear_item1, updated_gear_set.gear_items.all())
        self.assertIn(gear_item2, updated_gear_set.gear_items.all())

    def test_delete_gear_set(self):
        print_test_info("Testing GearSet Deletion")

        print_test_action("Creating GearSet")
        gear_item = GearItem.objects.create(
            diver=self.diver, name="Test Gear Item", gear_type=self.gear_type
        )
        gear_set = GearSet.objects.create(diver=self.diver, name="Test Gear Set", weight=10.5)
        gear_set.gear_items.set([gear_item])

        print_test_action("Deleting GearSet")
        gear_set_id = gear_set.id
        gear_set.delete()

        print_assert_that("GearSet is deleted")
        with self.assertRaises(GearSet.DoesNotExist):
            GearSet.objects.get(pk=gear_set_id)
        print_assert_that("GearItem still exists")
        self.assertTrue(GearItem.objects.filter(pk=gear_item.id).exists())
