"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from emacshaqiba.models import CodeTemplate

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

        
class CodeTemplateTests(TestCase):
    def test_name(self):
        codetemplate = CodeTemplate(name="shell",
                                    gist_url="http://gist.github.com/psachin/00000",
                                    code="(buffer-name)",
                                    description="test description")

        self.assertEqual(codetemplate.name, "shell")
        self.assertEqual(codetemplate.gist_url, "http://gist.github.com/psachin/00000")
        self.assertEqual(codetemplate.code, "(buffer-name)")
        self.assertEqual(codetemplate.description, "test description")
