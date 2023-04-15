import json

from rest_framework.test import APITestCase

from users.models import CustomUser


class UsersAPITest(APITestCase):
    """
    Test `users` app DRF API.
    """

    username = "testuser"
    password = "password"
    first_name = "Ivan"
    last_name = "Ivanov"
    new_user = None
    auth_token = None

    @classmethod
    def setUpTestData(cls):
        cls.new_user = CustomUser.objects.create_user(
            cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

    def setUp(self):
        """
        Login to get auth token for further tests.
        """
        url = "/api/v1/token/login/"
        response = self.client.post(
            url,
            {"username": self.username, "password": self.password},
        )
        self.auth_token = json.loads(response.content).get("auth_token")

    def test_logged_in_user_detail_api(self):
        """
        Ensure that `LoggedInUserDetailView`:
        - is located at defined URL;
        - returns all necessary data.
        """
        url = "/api/v1/user/details/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        user_details = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_details["username"], self.username)
        self.assertEqual(user_details["first_name"], self.first_name)
        self.assertEqual(user_details["last_name"], self.last_name)

    def test_user_update_api(self):
        """
        Ensure that `UserUpdateView`:
        - is located at defined URL;
        - partially updates user data using "PATCH" method;
        - returns all necessary data.
        """
        new_first_name = "Petr"
        new_last_name = "Petrov"
        new_email = "petr@petrov.ru"
        url = f"/api/v1/user/{self.new_user.pk}/"
        response = self.client.patch(
            url,
            {
                "first_name": new_first_name,
                "last_name": new_last_name,
                "email": new_email,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        user_details = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_details["first_name"], new_first_name)
        self.assertEqual(user_details["last_name"], new_last_name)
        self.assertEqual(user_details["email"], new_email)
