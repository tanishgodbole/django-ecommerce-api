from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
User = get_user_model()
class AuthenticationTests(APITestCase):
    def test_register_and_duplicate_email(self):
        payload = {"username":"ada", "email":"ada@example.com", "password":"Safe-passphrase-2026!"}
        self.assertEqual(self.client.post("/api/v1/auth/register/", payload).status_code, 201)
        self.assertEqual(self.client.post("/api/v1/auth/register/", payload).status_code, 400)
    def test_login_refresh_and_profile(self):
        User.objects.create_user(username="ada", email="ada@example.com", password="Safe-passphrase-2026!")
        token = self.client.post("/api/v1/auth/login/", {"email":"ada@example.com", "password":"Safe-passphrase-2026!"}, format="json")
        self.assertEqual(token.status_code, 200)
        self.assertEqual(self.client.post("/api/v1/auth/refresh/", {"refresh":token.data["refresh"]}, format="json").status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data["access"])
        self.assertEqual(self.client.get("/api/v1/auth/profile/").status_code, 200)
    def test_profile_requires_auth(self):
        self.assertEqual(self.client.get("/api/v1/auth/profile/").status_code, 401)
