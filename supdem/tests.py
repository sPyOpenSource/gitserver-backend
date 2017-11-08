from django.test import TestCase
from django.test import Client

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is OK.
        self.assertRedirects(response, '/git/index.html', status_code=302, target_status_code=404)

    def test_api(self):
        response = self.client.get('/api/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        response = self.client.post('/api/items', {'title': 'test', 'description': 'test'})
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/messages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        response = self.client.post('/api/messages', {'item': '/api/items/1', 'text': 'test'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/messages')
        self.assertEqual(len(response.json()), 1)
        response = self.client.get('/api/messages/2')
        self.assertEqual(response.json()['detail'], 'Not found.')
