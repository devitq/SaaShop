from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from homepage.forms import EchoForm

__all__ = ()


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = EchoForm()

    def test_getting_right_context(self):
        response = Client().get(reverse("homepage:echo"))
        self.assertIn("form", response.context)

    def test_text_label_and_help_text(self):
        text_label = self.form.fields["text"].label
        help_text = self.form.fields["text"].help_text
        self.assertEqual(text_label, "Текст")
        self.assertEqual(help_text, "Введите какой-нибудь текст")

    def test_submit_echo(self):
        Client().post(
            path=reverse("homepage:echo_submit"),
            data={"text": "Текст"},
        )

    def test_method_for_echo(self):
        response_get = Client().get(reverse("homepage:echo"))
        self.assertEqual(
            response_get.status_code,
            HTTPStatus.OK,
        )
        response_post = Client().post(
            path=reverse("homepage:echo"),
            data={"text": "Текст"},
        )
        self.assertEqual(
            response_post.status_code,
            HTTPStatus.METHOD_NOT_ALLOWED,
        )

    def test_method_for_echo_submit(self):
        response_get = Client().get(reverse("homepage:echo_submit"))
        self.assertEqual(
            response_get.status_code,
            HTTPStatus.METHOD_NOT_ALLOWED,
        )
        response_post = Client().post(
            path=reverse("homepage:echo_submit"),
            data={"text": "Текст"},
        )
        self.assertEqual(
            response_post.status_code,
            HTTPStatus.OK,
        )

    def test_validation_neg(self):
        invalid_form = EchoForm(
            {"text": ""},
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertFormError(
            invalid_form,
            "text",
            "Обязательное поле.",
        )

    def test_validation_pos(self):
        invalid_form = EchoForm(
            {"text": "fhdis"},
        )
        self.assertTrue(invalid_form.is_valid())
        self.assertFormError(
            invalid_form,
            "text",
            [],
        )
