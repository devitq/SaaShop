from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
import parameterized

__all__ = ()


class DynamicURLTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("catalog:item_list",),
            ("catalog:new_item_list",),
            ("catalog:friday_item_list"),
            ("catalog:unverified_item_list",),
        ],
    )
    def test_catalog_item_endpoint(self, url):
        response = Client().get(
            reverse(url),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unusual_item_detail_endpoint(self):
        with self.assertRaises(NoReverseMatch):
            unusual_response1 = Client().get(
                reverse("catalog:item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response1.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response2 = Client().get(
                reverse("catalog:item_detail", args=["text"]),
            )
            self.assertEqual(
                unusual_response2.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response3 = Client().get(
                reverse("catalog:item_detail", args=[1.1]),
            )
            self.assertEqual(
                unusual_response3.status_code,
                HTTPStatus.NOT_FOUND,
            )

    def test_re_item_detail_endpoint(self):
        usual_response = Client().get(
            reverse("catalog:re_item_detail", args=[1]),
        )
        self.assertContains(usual_response, "1", status_code=HTTPStatus.OK)

    def test_unusual_re_item_detail_endpoint(self):
        with self.assertRaises(NoReverseMatch):
            unusual_response1 = Client().get(
                reverse("catalog:re_item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response1.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response2 = Client().get(
                reverse("catalog:re_item_detail", args=[0]),
            )
            self.assertEqual(
                unusual_response2.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response3 = Client().get(
                reverse("catalog:re_item_detail", args=[1.1]),
            )
            self.assertEqual(
                unusual_response3.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response4 = Client().get(
                reverse("catalog:re_item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response4.status_code,
                HTTPStatus.NOT_FOUND,
            )

    def test_convert_item_detail_endpoint(self):
        usual_response = Client().get(
            reverse("catalog:converter_item_detail", args=[1]),
        )
        self.assertContains(usual_response, "1", status_code=HTTPStatus.OK)

    def test_unusual_convert_item_detail_endpoint(self):
        with self.assertRaises(NoReverseMatch):
            unusual_response1 = Client().get(
                reverse("catalog:converter_item_detail", args=[0]),
            )
            self.assertEqual(
                unusual_response1.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response2 = Client().get(
                reverse("catalog:converter_item_detail", args=["text"]),
            )
            self.assertEqual(
                unusual_response2.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response3 = Client().get(
                reverse("catalog:converter_item_detail", args=[1.1]),
            )
            self.assertEqual(
                unusual_response3.status_code,
                HTTPStatus.NOT_FOUND,
            )

            unusual_response4 = Client().get(
                reverse("catalog:converter_item_detail", args=[-1]),
            )
            self.assertEqual(
                unusual_response4.status_code,
                HTTPStatus.NOT_FOUND,
            )
