from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from api.models import User

client = Client()

class PingTest(TestCase):
    """ Test for /api/ping """
    
    def testPingResponse(self):
        response = client.get('/api/ping')
        expected = {'message': 'API is up and running!'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
        

class UserCreationTest(TestCase):
    """
    Test for user creation
    """
    def setUp(self):
        User.objects.create(email="yzhuang63@wisc.edu", first_name="yan", last_name="zhuang")

    def testRequestAccount(self):
        responseCorrect = client.post('/api/request-account', {"email": "yzhuang63@wisc.edu", "labName": "wright lab", "institutionName": "uw madison"})
        expectedCorrect = {"message": "request made successfully!"}
        user = User.objects.get(email="yzhuang63@wisc.edu")
        self.assertEqual(responseCorrect.data, expectedCorrect)
        self.assertEqual(responseCorrect.status_code, status.HTTP_200_OK)
        self.assertEqual(user.labName, "wright lab")
        self.assertEqual(user.institutionName, "uw madison")

        responseRepeat = client.post('/api/request-account', {"email": "yzhuang63@wisc.edu", "labName": "wright lab", "institutionName": "uw madison"})
        expectedRepeat = {"message": "There is already an request related to this account"}
        self.assertEqual(responseRepeat.data, expectedRepeat)
        self.assertEqual(responseRepeat.status_code, status.HTTP_400_BAD_REQUEST)

        responseUserNotExist = client.post('/api/request-account', {"email": "yzhuang6@wisc.edu", "labName": "wright lab", "institutionName": "uw madison"})
        expectedUserNotExist = {"message": "User not found with given email"}
        self.assertEqual(responseUserNotExist.data, expectedUserNotExist)
        self.assertEqual(responseUserNotExist.status_code, status.HTTP_404_NOT_FOUND)

