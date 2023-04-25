"""
Functional test for the Frontend.

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
    Test the real Nuxt frontend as new user, by the following algorithm:
    1. Open the site.
    2. Click "Sign Up" button in the navbar, and create new account.
    3. Login.
    4. Click "Add" menu item in the navbar.
    5. Enter an URL, hit Enter key.
    """

    username = "testuser123"
    password = "testpassword"
    bookmark_url = "https://www.youtube.com/watch?v=F161MWDg-48"
    bookmark_title = "Baby Blue"

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

    def test_sign_up(self):
        """
        Create new user account.
        """
        self.browser.get(
            settings.FRONTEND_URL,
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

        """
        Test Add bookmark page.
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

        # Click "Bookmarks" menu item in the navbar
        menu_item = self.browser.find_element(By.ID, value="navbar-menu-item-bookmarks")
        menu_item.click()
        menu_item.click()
        time.sleep(1)

        table = self.browser.find_element(By.ID, value="table-bookmarks")
        self.assertIn(self.bookmark_title, table.text)

        # Find "Edit bookmark" button for added bookmark
        button = self.browser.find_element(
            By.XPATH,
            value="//table[@id='table-bookmarks']/tbody/tr[1]/td[3]/button",
        )
        button.click()
        time.sleep(1)

        # Click "Delete" button, confirmation modal will popup
        button = self.browser.find_element(By.ID, value="button-delete")
        button.click()

        # Wait for modal to show, and "click" OK
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()

        self.assertNotIn(self.bookmark_title, self.browser.title)

        # self.fail("End the test.")
        time.sleep(3)
