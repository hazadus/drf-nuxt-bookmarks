"""
Functional test for the Frontend.

Running the test:
    make docker_functest

NB: This test uses copy of the real database, which is deleted after test.
NB: We do not use `self.browser.get(self.live_server_url)` because our frontend works separately.
"""
import os
import shutil
import time

from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class NewVisitorTest(LiveServerTestCase):
    """
    Test the real Nuxt frontend as new user.
    """

    username = "testuser123"
    password = "testpassword"
    first_name = "Ivan"
    last_name = "Petrov"
    telegram_id = "123456789"
    # Use short YouTube video to test downloading
    bookmark_url = "https://www.youtube.com/watch?v=F161MWDg-48"
    bookmark_title = "Baby Blue"
    bookmark_title_changed = "Baby Blue - changed"

    def setUp(self) -> None:
        # Backup existing DB file
        shutil.copy(
            src=os.path.join(settings.BASE_DIR, "db.sqlite3"),
            dst=os.path.join(settings.BASE_DIR, "db.sqlite3.backup"),
        )
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        # Delete DB used in test, and restore original DB from backup copy.
        os.remove(
            path=os.path.join(settings.BASE_DIR, "db.sqlite3"),
        )
        os.rename(
            src=os.path.join(settings.BASE_DIR, "db.sqlite3.backup"),
            dst=os.path.join(settings.BASE_DIR, "db.sqlite3"),
        )
        self.browser.quit()

    def click_navbar_menu_bookmarks(self):
        """
        Click "Bookmarks" menu item in the navbar
        """
        menu_item = self.browser.find_element(By.ID, value="navbar-menu-item-bookmarks")
        menu_item.click()
        menu_item.click()
        time.sleep(1)

    def click_bookmarks_table_first_row_edit_button(self):
        """
        Clicks "Edit" button for the bookmark in the first row of the table.
        """
        button = self.browser.find_element(
            By.XPATH,
            value="//table[@id='table-bookmarks']/tbody/tr[1]/td[3]/button",
        )
        button.click()
        time.sleep(1)

    def test_all(self):
        """
        Run all tests in the right order, because we sign up and log in in the beginning.
        """
        # Sign up and log in must be done in the first place, or other tests won't work.
        self.do_test_signup_and_login()
        # Test profile update page
        self.do_test_update_profile()
        # Then we add a bookmark...
        self.do_test_add_bookmark()
        # Edit bookmark
        self.do_test_edit_bookmark()
        # These two can be executed separately (we want to run `...delete`, though, to delete downloaded file):
        self.do_test_download_bookmark()
        self.do_test_delete_bookmark()

    def do_test_signup_and_login(self):
        """
        Test basic app features:
        - Open the site.
        - Click "Sign Up" button in the navbar, and create new account.
        - Login.
        """
        self.browser.get(
            # We assume that the app is running from Docker Compose on `localhost`
            "http://localhost/",
        )
        time.sleep(1)

        # Check that the app is started
        self.assertIn("| Bookmarks", self.browser.title)

        # Click "Sign up" button
        button = self.browser.find_element(By.ID, value="navbar-button-signup")
        button.click()

        self.assertIn("Create new user account", self.browser.title)

        # Fill the form
        inputbox = self.browser.find_element(By.ID, value="input-username")
        inputbox.send_keys(self.username)

        inputbox = self.browser.find_element(By.ID, value="input-password")
        inputbox.send_keys(self.password)

        inputbox = self.browser.find_element(By.ID, value="input-password2")
        inputbox.send_keys(self.password)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assertIn("Log in", self.browser.title)
        time.sleep(1)

        """
        Test log in with new account.
        """
        inputbox = self.browser.find_element(By.ID, value="username")
        inputbox.send_keys(self.username)

        inputbox = self.browser.find_element(By.ID, value="password")
        inputbox.send_keys(self.password)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assertIn("Your Bookmarks", self.browser.title)

    def do_test_add_bookmark(self):
        """
        Test Add bookmark page.
        - Click "Add" menu item in the navbar.
        - Enter an YouTube URL, hit Enter key.
        - Click "Bookmarks" in the navbar.
        - Check that the bookmark is listed in the table.
        """
        # Click "Add" menu item in the navbar
        menu_item = self.browser.find_element(By.ID, value="navbar-menu-item-add")
        menu_item.click()
        menu_item.click()

        # Add an URL
        inputbox = self.browser.find_element(By.ID, value="input-url")
        inputbox.send_keys(self.bookmark_url)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        self.click_navbar_menu_bookmarks()

        table = self.browser.find_element(By.ID, value="table-bookmarks")
        self.assertIn(self.bookmark_title, table.text)

    def do_test_edit_bookmark(self):
        """
        Edit the bookmark using EditBookmarkModal.
        """
        self.click_navbar_menu_bookmarks()
        self.click_bookmarks_table_first_row_edit_button()

        # Change bookmark's title and save it
        inputbox = self.browser.find_element(By.ID, value="input-title")
        inputbox.click()
        # NB: `COMMAND` may be changed to `CONTROL` on Windows
        inputbox.send_keys(Keys.COMMAND, "a")
        inputbox.send_keys(self.bookmark_title_changed)
        button = self.browser.find_element(By.ID, value="button-save")
        button.click()
        time.sleep(2)

        table = self.browser.find_element(By.ID, value="table-bookmarks")
        self.assertIn(self.bookmark_title_changed, table.text)

    def do_test_download_bookmark(self):
        """
        Test video download for added bookmark.
        - Click "Bookmarks" in the navbar.
        - Open "Edit bookmark" modal for added URL, click "Download", close modal.
        - Wait for download to end, open modal, check if downloaded file displayed.
        """
        self.click_navbar_menu_bookmarks()
        self.click_bookmarks_table_first_row_edit_button()

        # Click "Download"
        button = self.browser.find_element(By.ID, value="button-download")
        button.click()

        # Click "Close" and wait for the download
        button = self.browser.find_element(By.ID, value="button-close")
        button.click()
        time.sleep(15)

        # Click "Refresh"
        button = self.browser.find_element(By.ID, value="button-refresh")
        button.click()
        time.sleep(3)

        self.click_bookmarks_table_first_row_edit_button()

        # Check if file info displayed
        span = self.browser.find_element(By.ID, value="downloaded-file-info")
        self.assertIn("Video file", span.text)

        # Click "Close"
        button = self.browser.find_element(By.ID, value="button-close")
        button.click()

    def do_test_delete_bookmark(self):
        """
        Test "Delete" button in EditBookmarlModal.
        """
        self.click_navbar_menu_bookmarks()
        self.click_bookmarks_table_first_row_edit_button()

        # Click "Delete" button, confirmation modal will popup
        button = self.browser.find_element(By.ID, value="button-delete")
        button.click()
        time.sleep(1)

        # Wait for modal to show, and "click" OK
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()
        time.sleep(1)

        # Check that deleted bookmark is not listed on the page (there must be no table at all)
        table = self.browser.find_element(By.TAG_NAME, value="body")
        self.assertNotIn(self.bookmark_title, table.text)

        time.sleep(1)

    def do_test_update_profile(self):
        """
        Test "Edit profile" page.
        """
        menu = self.browser.find_element(By.ID, value="navbar-menu-user")
        menu.click()
        menu = self.browser.find_element(By.ID, value="navbar-menu-user-profile")
        menu.click()
        button = self.browser.find_element(By.ID, value="button-edit-profile")
        button.click()

        # Fill the form and save
        inputbox = self.browser.find_element(By.ID, value="input-first-name")
        inputbox.click()
        inputbox.send_keys(self.first_name)
        inputbox = self.browser.find_element(By.ID, value="input-last-name")
        inputbox.click()
        inputbox.send_keys(self.last_name)
        inputbox = self.browser.find_element(By.ID, value="input-telegram-id")
        inputbox.click()
        inputbox.send_keys(self.telegram_id)

        button = self.browser.find_element(By.ID, value="button-save-profile")
        button.click()
        time.sleep(1)

        body = self.browser.find_element(By.TAG_NAME, value="body")
        self.assertIn(self.first_name, body.text)
        self.assertIn(self.last_name, body.text)
        self.assertIn(self.telegram_id, body.text)

        time.sleep(1)
