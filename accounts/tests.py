from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("account_signup")
        self.login_url = reverse("account_login")

    def test_user_signup(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "testpassword123",
                "password2": "testpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        user = get_user_model().objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_user_login(self):
        # First, create a user
        user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )

        # Now, attempt to log in
        response = self.client.post(
            self.login_url,
            {"login": "testuser", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)
