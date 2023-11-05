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

    def test_validation_neg_01(self):
        invalid_form = FeedbackForm(
            {Feedback.text.field.name: "", Feedback.mail.field.name: ""},
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertFormError(
            invalid_form,
            Feedback.text.field.name,
            "Обязательное поле.",
        )
        self.assertFormError(
            invalid_form,
            Feedback.mail.field.name,
            "Обязательное поле.",
        )

    def test_validation_neg_02(self):
        invalid_form = FeedbackForm(
            {
                Feedback.text.field.name: "fsdfs",
                Feedback.mail.field.name: "fsdf.fsd",
            },
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertFormError(
            invalid_form,
            Feedback.mail.field.name,
            "Введите правильный адрес электронной почты.",
        )

    def test_validation_pos(self):
        invalid_form = FeedbackForm(
            {
                Feedback.text.field.name: "fdfd",
                Feedback.mail.field.name: "fsdf@gifd.fds",
            },
        )
        self.assertTrue(invalid_form.is_valid())
        self.assertFormError(
            invalid_form,
            Feedback.text.field.name,
            [],
        )
        self.assertFormError(
            invalid_form,
            Feedback.mail.field.name,
            [],
        )

    def test_getting_right_context(self):
        response = Client().get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_text_label_and_help_text(self):
        text_label = self.form.fields[Feedback.text.field.name].label
        help_text = self.form.fields[Feedback.text.field.name].help_text
        self.assertEqual(text_label, "Текст")
        self.assertEqual(help_text, "Ваш отзыв")

    def test_mail_label(self):
        text_label = self.form.fields[Feedback.mail.field.name].label
        help_text = self.form.fields[Feedback.mail.field.name].help_text
        self.assertEqual(text_label, "Почта")
        self.assertEqual(help_text, "Почта, по которой мы свяжемся с вами")

    def test_create_feedback(self):
        feedbacks_count = Feedback.objects.count()
        response = Client().post(
            path=reverse("feedback:feedback"),
            data={
                Feedback.text.field.name: "Текст фидбека",
                Feedback.mail.field.name: "example@mail.com",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(Feedback.objects.count(), feedbacks_count + 1)
        self.assertTrue(
            Feedback.objects.filter(text="Текст фидбека").exists(),
        )
