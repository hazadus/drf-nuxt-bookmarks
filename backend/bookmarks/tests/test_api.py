import json

from rest_framework.test import APITestCase

from bookmarks.models import Bookmark, Folder, Tag
from bookmarks.serializers import FolderSerializer
from users.models import CustomUser

NUMBER_OF_TAGS = 10
NUMBER_OF_FOLDERS = 10
NUMBER_OF_BOOKMARKS_IN_FOLDER = 20


class BookmarksAPITest(APITestCase):
    """
    Test `bookmarks` app DRF API.
    """

    username = "testuser"
    password = "password"
    telegram_id = "133637887"
    first_name = "Ivan"
    last_name = "Ivanov"
    new_user = None
    auth_token = None

    @classmethod
    def setUpTestData(cls):  # noqa: max-complexity: 4
        cls.new_user = CustomUser.objects.create_user(
            cls.username,
            password=cls.password,
            telegram_id=cls.telegram_id,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )
        new_bookmark = Bookmark.objects.create(
            title="Bookmarks App",
            url="https://bookmarks.hazadus.ru",
            description="Site bookmarking app",
            user=cls.new_user,
        )
        for i in range(0, NUMBER_OF_TAGS):
            tag = Tag.objects.create(title=f"Tag #{i}")
            new_bookmark.tags.add(tag)

        # Create folders with bookmarks within
        for i in range(0, NUMBER_OF_FOLDERS):
            folder = Folder.objects.create(
                title=f"Folder #{i}",
                user=cls.new_user,
            )
            for j in range(0, NUMBER_OF_BOOKMARKS_IN_FOLDER):
                Bookmark.objects.create(
                    title=f"Bookmark {j} in folder {i}",
                    user=cls.new_user,
                    url="https://bookmarks.hazadus.ru",
                    folder=folder,
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

    def test_tag_list_api(self):
        """
        Ensure that `TagListView`:
        - is located at defined URL;
        - tag list is annotated with "bookmarks_qty" field;
        - returns all tags applied to authenticated user's bookmarks.
        """
        url = "/api/v1/tags/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        tag_list = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(tag_list), NUMBER_OF_TAGS)

        for i in range(0, NUMBER_OF_TAGS):
            self.assertEqual(tag_list[i]["bookmarks_qty"], 1)

    def test_folder_list_api(self):
        """
        Ensure that `FolderListView`:
        - is located at defined URL;
        - folder list is annotated with "bookmarks_qty" field;
        - returns all authenticated user's folders.
        """
        url = "/api/v1/folders/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        folder_list = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(folder_list), NUMBER_OF_FOLDERS)

        for i in range(0, NUMBER_OF_FOLDERS):
            self.assertEqual(
                folder_list[i]["bookmarks_qty"], NUMBER_OF_BOOKMARKS_IN_FOLDER
            )

    def test_folder_create_api(self):
        """
        Ensure that `folder_create`:
        - is located at defined URL;
        - folder can't be created with wrong (non-existent) user id;
        - folder can't be created for user another that authenticated one;
        - returns newly created Folder object.
        """
        new_folder_title = "New Folder 1"
        url = "/api/v1/folders/create/"
        response = self.client.post(
            url,
            {
                "user_id": self.new_user.pk,
                "title": new_folder_title,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        folder_data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(folder_data["user_id"], self.new_user.pk)
        self.assertEqual(folder_data["title"], new_folder_title)

        # Try with non-existent user id
        response = self.client.post(
            url,
            {
                "user_id": 100,
                "title": new_folder_title,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        self.assertEqual(response.status_code, 400)

        # Try with another user
        new_user2 = CustomUser.objects.create_user(
            "testuser2",
            password="password2",
        )
        response = self.client.post(
            url,
            {
                "user_id": new_user2.pk,
                "title": new_folder_title,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        self.assertEqual(response.status_code, 403)

    def test_folder_update_api(self):
        """
        Ensure that `FolderUpdateView`:
        - is located at defined URL;
        - partially updates folder data with "PATCH" method;
        - returns updated data.
        """
        updated_folder_title = "Updated Folder Title"
        folder = Folder.objects.all().first()
        serializer = FolderSerializer(instance=folder, many=False)
        data = serializer.data
        data["title"] = updated_folder_title
        url = f"/api/v1/folders/update/{folder.pk}/"
        response = self.client.patch(
            url,
            data=data,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        folder_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(folder_data["title"], updated_folder_title)

    def test_folder_delete_api(self):
        """
        Ensure that `FolderDeleteView`:
        - is located at defined URL;
        - Set `folder=None` for all bookmarks in the folder before actually deleting it.
        """
        folder = Folder.objects.all().first()
        bookmark_ids = list(folder.bookmarks.all().values_list("id", flat=True))
        url = f"/api/v1/folders/delete/{folder.pk}/"
        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        self.assertEqual(response.status_code, 204)
        # Check that bookmarks from the folder are still alive:
        for _id in bookmark_ids:
            self.assertEqual(Bookmark.objects.get(pk=_id).folder, None)

    def test_bookmark_list_api(self):
        """
        Ensure that `BookmarkListView`:
        - is located at defined URL;
        - returns all authenticated user's bookmarks.
        """
        url = "/api/v1/bookmarks/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        bookmark_list = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(bookmark_list), NUMBER_OF_FOLDERS * NUMBER_OF_BOOKMARKS_IN_FOLDER + 1
        )

    def test_bookmark_create_from_telegram_api(self):
        """
        Ensure that `bookmark_create_from_telegram`:
        - is located at defined URL;
        - properly creates the bookmark when correct `telegram_id` passed;
        - return 400 code if there's no user with `telegram_id` in the database.
        """
        url = "/api/v1/bookmarks/create_from_telegram/"
        response = self.client.post(
            url,
            {
                "user": {
                    "telegram_id": self.telegram_id,
                },
                "url": "https://ya.ru",
            },
            format="json",
        )

        bookmark = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(bookmark["url"], "https://ya.ru")

        # Test with wrong `telegram_id`:
        response = self.client.post(
            url,
            {
                "user": {
                    "telegram_id": "123456789",
                },
                "url": "https://ya.ru",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_bookmark_create_from_web_api(self):
        """
        Ensure that `bookmark_create_from_web`:
        - is located at defined URL;
        - properly creates the bookmark for authenticated user when correct `url` passed;
        - return 400 code if the URL is incorrect.
        """
        url = "/api/v1/bookmarks/create/"
        response = self.client.post(
            url,
            {
                "url": "https://ya.ru",
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        bookmark = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(bookmark["url"], "https://ya.ru")
        self.assertEqual(bookmark["user"], self.new_user.pk)

        # Try with wrong URL:
        response = self.client.post(
            url,
            {
                "url": "https://.ru",
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        self.assertEqual(response.status_code, 400)

    def test_bookmark_update_api(self):
        """
        Ensure that `BookmarkUpdateView`:
        - is located at defined URL;
        - partially updates bookmark with "PATCH" method.
        """
        bookmark = Bookmark.objects.all().first()
        tag = Tag.objects.all().first()
        folder = Folder.objects.filter(user_id__exact=self.new_user.pk).first()

        url = f"/api/v1/bookmarks/update/{bookmark.pk}/"
        response = self.client.patch(
            url,
            {
                "title": "New title",
                "tags": [
                    {
                        "id": tag.pk,
                        "title": tag.title,
                    },
                ],
                "folder": {
                    "id": folder.pk,
                    "user": folder.user.pk,
                    "title": folder.title,
                },
            },
            format="json",  # Don't forget this to handle nested objects and arrays
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        bookmark_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bookmark_data["title"], "New title")
        self.assertEqual(bookmark_data["tags"][0]["id"], tag.pk)
        self.assertEqual(bookmark_data["folder"]["id"], folder.pk)
        self.assertEqual(bookmark_data["url"], bookmark.url)
        self.assertEqual(bookmark_data["description"], bookmark.description)
        self.assertEqual(bookmark_data["is_read"], bookmark.is_read)
        self.assertEqual(bookmark_data["is_favorite"], bookmark.is_favorite)
        self.assertEqual(bookmark_data["is_archived"], bookmark.is_archived)

        # Check that folder is set to None if no folder is passed to API:
        url = f"/api/v1/bookmarks/update/{bookmark.pk}/"
        response = self.client.patch(
            url,
            {
                "title": "New title 2",
            },
            format="json",  # Don't forget this to handle nested objects and arrays
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        bookmark_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bookmark_data["title"], "New title 2")
        self.assertEqual(bookmark_data["folder"], None)

    def test_bookmark_delete_view(self):
        """
        Ensure that `BookmarkDeleteView`:
        - is located at defined URL;
        - actually deletes the bookmark;
        - only owner can delete a bookmark.
        """
        bookmark = Bookmark.objects.all().first()
        bookmark_pk = bookmark.pk
        url = f"/api/v1/bookmarks/delete/{bookmark.pk}/"
        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Bookmark.objects.all().filter(pk=bookmark_pk)), 0)

        # Try to delete another user's bookmark
        new_user2 = CustomUser.objects.create_user(
            "testuser2",
            password="password2",
        )
        others_bookmark = Bookmark.objects.create(
            title="Other's bookmark",
            url="https://www.hazadus.ru/",
            user=new_user2,
        )
        url = f"/api/v1/bookmarks/delete/{others_bookmark.pk}/"
        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        self.assertEqual(response.status_code, 403)
