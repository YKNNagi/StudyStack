from django.test import TestCase
from .models import Study
from django.contrib.auth import get_user_model
from .forms import StudyForm

# Create your tests here.

class StudyFormTest(TestCase):

    def test_valid_content(self):
        form = StudyForm(
            data={
                "content": "Pythonを勉強する"
            }
        )

        self.assertTrue(form.is_valid())


    def test_short_content(self):
            form = StudyForm(
                data={
                    "content": " a "
                }
            )
    
            self.assertFalse(form.is_valid())
            self.assertIn("content", form.errors)

    def test_whitespace_only_content(self):
            form = StudyForm(
                data={
                    "content": "   "
                }
            )
    
            self.assertFalse(form.is_valid())
            self.assertIn("content", form.errors)

class StudyModelTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

    def test_create_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        self.assertEqual(Study.objects.count(), 1)
        self.assertEqual(study.content, "Pythonを勉強する")
        self.assertEqual(study.user, self.user)

    def test_update_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        study.content = "Djangoを勉強する"
        study.save()

        study.refresh_from_db()

        self.assertEqual(study.content, "Djangoを勉強する")

    def test_delete_study(self):
         study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

         self.assertEqual(Study.objects.count(), 1)

         study.delete()

         self.assertEqual(Study.objects.count(), 0)

    def test_read_study(self):
         Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

         study = Study.objects.get(
            user=self.user
        )

         self.assertEqual(study.content, "Pythonを勉強する")

        