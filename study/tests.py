from django.test import TestCase
from django.test import TestCase
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
    