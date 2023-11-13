from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings, TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm, PersonalDataForm
from feedback.models import Feedback, PersonalData

__all__ = ()


class UploadTests(TestCase):
    @override_settings(MEDIA_ROOT="tests/")
    def test_file_upload(self):
        files = [
            SimpleUploadedFile(f"test_file{i}.txt", b"file_content")
            for i in range(10)
        ]
        response = self.client.post(
            reverse("feedback:feedback"),
            data={
                "files": files,
                Feedback.text.field.name: "Текст фидбека",
                PersonalData.name.field.name: "Имя",
                PersonalData.mail.field.name: "fjid@hf.fsd",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("feedback:feedback"))
        for f in files:
            f.close()


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.feedback_form = FeedbackForm()
        cls.personal_data_form = PersonalDataForm()

    def test_validation_neg_01(self):
        invalid_form = FeedbackForm(
            {
                Feedback.text.field.name: "",
            },
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertTrue(invalid_form.has_error(Feedback.text.field.name))
        invalid_form = PersonalDataForm(
            {
                PersonalData.name.field.name: "",
                PersonalData.mail.field.name: "",
            },
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertTrue(invalid_form.has_error(PersonalData.mail.field.name))
        self.assertFalse(invalid_form.has_error(PersonalData.name.field.name))

    def test_validation_neg_02(self):
        invalid_form = PersonalDataForm(
            {
                PersonalData.name.field.name: "dfsf",
                PersonalData.mail.field.name: "fsdf.fdsf",
            },
        )
        self.assertFalse(invalid_form.is_valid())
        self.assertFalse(invalid_form.has_error(PersonalData.name.field.name))
        self.assertTrue(invalid_form.has_error(PersonalData.mail.field.name))

    def test_validation_pos(self):
        invalid_form = FeedbackForm(
            {
                Feedback.text.field.name: "fdfd",
            },
        )
        self.assertTrue(invalid_form.is_valid())
        self.assertFalse(invalid_form.has_error(Feedback.text.field.name))
        invalid_form = PersonalDataForm(
            {
                PersonalData.name.field.name: "fdfd",
                PersonalData.mail.field.name: "ex@mail.com",
            },
        )
        self.assertTrue(invalid_form.is_valid())
        self.assertFalse(invalid_form.has_error(PersonalData.name.field.name))
        self.assertFalse(invalid_form.has_error(PersonalData.mail.field.name))

    def test_getting_right_context(self):
        response = Client().get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_text_label_and_help_text(self):
        text_label = self.feedback_form.fields[Feedback.text.field.name].label
        help_text = self.feedback_form.fields[
            Feedback.text.field.name
        ].help_text
        self.assertEqual(text_label, "Текст")
        self.assertEqual(help_text, "Ваш отзыв")

    def test_mail_label_and_help_text(self):
        text_label = self.personal_data_form.fields[
            PersonalData.mail.field.name
        ].label
        help_text = self.personal_data_form.fields[
            PersonalData.mail.field.name
        ].help_text
        self.assertEqual(text_label, "Почта")
        self.assertEqual(help_text, "Почта, по которой мы свяжемся с вами")

    def test_name_label_and_help_text(self):
        text_label = self.personal_data_form.fields[
            PersonalData.name.field.name
        ].label
        help_text = self.personal_data_form.fields[
            PersonalData.name.field.name
        ].help_text
        self.assertEqual(text_label, "Имя")
        self.assertEqual(help_text, "Ваше имя")

    def test_create_feedback(self):
        feedbacks_count = Feedback.objects.count()
        response = Client().post(
            path=reverse("feedback:feedback"),
            data={
                Feedback.text.field.name: "Текст фидбека",
                PersonalData.name.field.name: "Имя",
                PersonalData.mail.field.name: "fjid@hf.fsd",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(Feedback.objects.count(), feedbacks_count + 1)
        self.assertTrue(
            Feedback.objects.filter(text="Текст фидбека").exists(),
        )
