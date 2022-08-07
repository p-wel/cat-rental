from django.test import TestCase


class URLTests(TestCase):
    """
    Basic URL tests.
    Checks some URLs if they return status code 200
    """

    def test_index(self):
        response = self.client.get()
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get()
        self.assertEqual(response.status_code, 200)

    def test_species(self):
        response = self.client.get()
        self.assertEqual(response.status_code, 200)

    def test_explore(self):
        response = self.client.get()
        self.assertEqual(response.status_code, 200)

    def test_cats_list_1(self):
        response = self.client.get()
        self.assertEqual(response.status_code, 200)