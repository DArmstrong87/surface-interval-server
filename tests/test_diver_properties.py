from django.test import TestCase
from surfaceintervalapi.models import Diver
from tests.utils import print_test_info, print_assert_that, print_test_action, print_test_setup


class DiverPropertiesTestCase(TestCase):
    """
    Test creation of User and Diver
    """

    fixtures = [
        "tests/fixtures/users.json",
        "tests/fixtures/divers.json",
        "tests/fixtures/dives.json",
        "tests/fixtures/specialties.json",
        "tests/fixtures/dive_specialties.json",
    ]

    def setUp(self):
        print_test_setup(self)
        return super().setUp()

    def test_diver_dynamic_properties(self):
        print_test_info("Testing Diver dynamic properties")

        print_test_action("Getting first Diver from fixtures.")
        diver = Diver.objects.filter().first()

        print_assert_that("Diver exists")
        self.assertIsNotNone(diver)

        print_assert_that("Diver dynamic properties match")

        self.assertEqual(diver.total_dives, 15)

        most_recent_dive = diver.most_recent_dive.strftime("%Y-%m-%d")
        self.assertEqual(most_recent_dive, "2018-11-10")

        self.assertEqual(diver.deepest_dive, 130)
        self.assertEqual(diver.longest_dive, 64)
        self.assertEqual(diver.shortest_dive, 15)
        self.assertEqual(diver.most_logged_specialty.get("specialty_name"), "Boat")
        self.assertEqual(diver.most_logged_specialty.get("count"), 3)

        self.assertEqual(diver.air_consumption["most_efficient"]["cu_ft_min"], 0.79)
        self.assertEqual(diver.air_consumption["most_efficient"]["ltrs_min"], 22.37)
        self.assertEqual(diver.air_consumption["least_efficient"]["cu_ft_min"], 0.79)
        self.assertEqual(diver.air_consumption["least_efficient"]["ltrs_min"], 22.37)
        self.assertEqual(diver.air_consumption["average"]["cu_ft_min"], 0.85)
        self.assertEqual(diver.air_consumption["average"]["ltrs_min"], 24.07)

    def test_null_values_in_dynamic_properties(self):
        print_test_info("Testing Diver dynamic properties with null values")

        diver = Diver.objects.get(pk=2)

        print_assert_that("Diver exists")
        self.assertIsNotNone(diver)

        print_assert_that("Null values are being handled appropriately with dynamic properties")
        self.assertEqual(diver.total_dives, 0)
        self.assertIsNone(diver.longest_dive)
        self.assertIsNone(diver.shortest_dive)
        self.assertIsNone(diver.most_logged_specialty)
        self.assertIsNone(diver.air_consumption)
        self.assertIsNone(diver.air_consumption)
