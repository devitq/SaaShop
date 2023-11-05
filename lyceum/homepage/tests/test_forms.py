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
        form_data = {
            "text": "Текст",
        }

        Client().post(
            path=reverse("homepage:echo_submit"),
            data=form_data,
        )
