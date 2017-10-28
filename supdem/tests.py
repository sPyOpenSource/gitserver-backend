from django.test import TestCase
from django.test import Client

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client(enforce_csrf_checks = True)

    def test_index(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is OK.
        self.assertRedirects(response, '/git/index.html', status_code=302, target_status_code=404)

    def test_api(self):
        response = self.client.get('/api/csrf_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('csrf_token' in response.json(), True)
        csrf_token = response.json()['csrf_token']

        response = self.client.post('/api/adduser', {'email': 'test@test.nl', 'password': 'test', 'csrfmiddlewaretoken': csrf_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 201)

        '''response = self.client.post('/api/token-auth', {'email': 'test@test.nl', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('token' in response.json(), True)
        token = response.json()['token']'''

        response = self.client.post('/api/additem', {'owner': 1, 'title': 'test', 'description': 'test', 'csrfmiddlewaretoken': csrf_token})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/additem', {'owner': 1, 'title': 'test', 'description': 'test', 'csrfmiddlewaretoken': csrf_token, 'expirydate': '2007-03-04T21:08:12'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/resetpassword', {'email': 'test@test.nl', 'csrfmiddlewaretoken': csrf_token})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        response = self.client.get('/api/items?expirydate=2006-03-04T21:00:00')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        '''response = self.client.get('/api/messages', HTTP_AUTHORIZATION = 'JWT ' + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        response = self.client.post('/api/messages', {'owner': '/api/users/1', 'item': '/api/items/1', 'text': 'test'}, HTTP_AUTHORIZATION = 'JWT ' + token)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/messages', HTTP_AUTHORIZATION = 'JWT ' + token)
        self.assertEqual(len(response.json()), 1)
        response = self.client.get('/api/messages?item=2', HTTP_AUTHORIZATION = 'JWT ' + token)
        self.assertEqual(len(response.json()), 0)'''

        response = self.client.get('/api/wiki')
        self.assertEqual(response.status_code, 200)
