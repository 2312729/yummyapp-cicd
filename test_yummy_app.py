import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Basic order-total tests."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 2}), 100000)

    def test_calculate_total_for_multiple_items(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": 1, "bun": 1}), 95000
        )

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)


class TestMediumLevel(unittest.TestCase):
    def test_apply_valid_promo_code(self):
        self.assertEqual(YummyApp().apply_promo_code(100000, "GIAM10"), 90000)

    def test_apply_new_os_promo_code(self):
        self.assertEqual(
            YummyApp(os_version=15).apply_promo_code(100000, "NEW_OS_ONLY"),
            80000,
        )

    def test_reject_promo_code_when_offline(self):
        with self.assertRaises(ConnectionError):
            YummyApp(network_status="offline").apply_promo_code(
                100000, "GIAM10"
            )

    def test_reject_promo_code_on_old_os(self):
        with self.assertRaises(ValueError):
            YummyApp(os_version=14).apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    def test_get_nearby_restaurants(self):
        restaurants = YummyApp().get_nearby_restaurants()
        self.assertEqual(len(restaurants), 2)

    @patch("gps_service.get_current_location")
    def test_get_nearby_restaurants_when_signal_is_lost(self, get_location):
        get_location.side_effect = gps_service.GPSSignalLostError
        self.assertEqual(
            YummyApp().get_nearby_restaurants(),
            "Khong the xac dinh vi tri.",
        )


if __name__ == "__main__":
    unittest.main()
