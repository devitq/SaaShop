from django.test import Client, TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback

__all__ = ()


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    def test_getting_right_context(self):
        response = Client().get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_text_label_and_help_text(self):
        text_label = self.form.fields["text"].label
        help_text = self.form.fields["text"].help_text
        self.assertEqual(text_label, "Текст")
        self.assertEqual(help_text, "Ваш отзыв")

    def test_mail_label(self):
        text_label = self.form.fields["mail"].label
        help_text = self.form.fields["mail"].help_text
        self.assertEqual(text_label, "Почта")
        self.assertEqual(help_text, "Почта, по которой мы свяжемся с вами")

    def test_create_feedback(self):
        feedbacks_count = Feedback.objects.count()
        form_data = {
            "text": "Текст фидбека",
            "mail": "example@mail.com",
        }

        response = Client().post(
            path=reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(Feedback.objects.count(), feedbacks_count + 1)
        self.assertTrue(
            Feedback.objects.filter(text="Текст фидбека").exists(),
        )
