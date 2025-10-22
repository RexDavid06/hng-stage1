from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.
class AnalyzerTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_and_get_string(self):
        payload = {"value": "racecar"}
        res = self.client.post("api/strings", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.json()
        self.assrtEqual(data["value"], "racecar")
        self.assertTrue(data["properties"] ["is_palindrome"])

        #get
        res2 = self.client.get(f"/api/strings/racecar")
        self.assretEqual(res2.status_code, status.HTTP_200_OK)
