

from django.test import TestCase
from django.test.client import Client


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def setUp(self):
        self.c = Client()

    def test_entries_access(self):
        response = self.c.get('/login/')
        self.assertEqual(response.status_code, 200)
