import json
from pathlib import Path

from django.test import TestCase

from drf_stripe.stripe_api.products import stripe_api_update_products_prices


class BaseTest(TestCase):
    def setUp(self) -> None:
        event = self._load_test_data("v1/stripe_product_list.json")
        stripe_api_update_products_prices(test_data=event)
        event = self._load_test_data("v1/stripe_price_list.json")
        stripe_api_update_products_prices(test_data=event)

    def tearDown(self) -> None:
        pass

    @staticmethod
    def _load_test_data(file_name):
        p = Path("tests/mock_responses") / file_name
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    @staticmethod
    def _print(v):
        print("$$$$$$$ DEBUG $$$$$")
        print(v)
        assert False
