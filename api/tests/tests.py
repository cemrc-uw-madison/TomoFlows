from rest_framework import status
from django.test import TestCase, Client

client = Client()

class PingTest(TestCase):
    """ Test for /api/ping """
    
    def test_ping_response(self):
        response = client.get('/api/ping')
        expected = {'message': 'API is up and running!'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
        
