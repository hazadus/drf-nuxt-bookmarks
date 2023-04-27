import json

from rest_framework.test import APITestCase

from bookmarks.models import Bookmark
from users.models import CustomUser


class DownloadsAPITest(APITestCase):
    """
    Test `bookmarks` app DRF API.
    """

    username = "testuser"
    password = "password"
    new_bookmark = None
    new_user = None
    auth_token = None

    @classmethod
    def setUpTestData(cls):
        cls.new_user = CustomUser.objects.create_user(
            cls.username,
            password=cls.password,
        )
        cls.new_bookmark = Bookmark.objects.create(
            title="YouTube Video",
            url="https://youtu.be/mqn0D4xat58",
            description="Test video",
            user=cls.new_user,
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

    def test_download_fails_with_zero_disk_quota(self):
        """
        Ensure that `download_start_from_web`:
        - is located at defined URL;
        - returns error if user has no disk quota.
        """
        url = "/api/v1/downloads/start/"
        response = self.client.post(
            url,
            {
                "bookmark_id": self.new_bookmark.pk,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        errors_data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "'{username}' has not enough disk quota to download files!".format(
                username=self.username,
            ),
            errors_data["bookmark_id"][0],
        )
