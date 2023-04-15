from django.test import TestCase

from bookmarks.models import Bookmark, Folder, Tag
from users.models import CustomUser


class BookmarkModelTest(TestCase):
    """
    Test Bookmark, Folder, Tag models.
    """

    username = "testuser"
    password = "password"
    bookmark_title = "Bookmarks App"
    bookmark_url = "https://bookmarks.hazadus.ru"
    bookmark_description = "Site bookmarking web app"
    folder_title = "Hot Stuff"
    tag_title = "App"

    @classmethod
    def setUpTestData(cls):
        new_user = CustomUser.objects.create_user(cls.username, password=cls.password)
        new_folder = Folder.objects.create(
            user=new_user,
            title=cls.folder_title,
        )
        new_tag = Tag.objects.create(title=cls.tag_title)
        new_bookmark = Bookmark.objects.create(
            user=new_user,
            title=cls.bookmark_title,
            url=cls.bookmark_url,
            description=cls.bookmark_description,
            folder=new_folder,
        )
        new_bookmark.tags.add(new_tag)

    def test_bookmark_created(self):
        """
        Ensure that:
        - the bookmark, folder and tag were correctly created.
        - __str__ methods of bookmark, folder and tag works as expected.
        """
        bookmark = Bookmark.objects.first()
        self.assertEqual(bookmark.title, self.bookmark_title)
        self.assertEqual(bookmark.url, self.bookmark_url)
        self.assertEqual(bookmark.description, self.bookmark_description)

        self.assertEqual(str(bookmark), self.bookmark_title)
        self.assertEqual(str(bookmark.folder), self.folder_title)
        self.assertEqual(str(bookmark.tags.all().first()), self.tag_title)
