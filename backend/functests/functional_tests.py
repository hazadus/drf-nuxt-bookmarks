import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        pass
        self.browser.quit()

    def test_first_visit(self):
        self.browser.get("http://localhost:3000/")
        time.sleep(1)

        # Check that the app is started
        self.assertIn("| Bookmarks", self.browser.title)

        # Try to log in
        # Enter username and password
        inputbox = self.browser.find_element(By.ID, value="username")
        inputbox.send_keys("testuser1")

        inputbox = self.browser.find_element(By.ID, value="password")
        inputbox.send_keys("drbzdrbz")
        inputbox.send_keys(Keys.ENTER)

        # Click "Add" menu item in the navbar
        menu_item = self.browser.find_element(By.ID, value="navbar-menu-item-add")
        menu_item.click()
        menu_item.click()

        # Add an URL
        inputbox = self.browser.find_element(By.ID, value="input-url")
        inputbox.send_keys("https://testdriven.io/blog/django-drf-elasticsearch/")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        # Click "Bookmarks" menu item in the navbar
        menu_item = self.browser.find_element(By.ID, value="navbar-menu-item-bookmarks")
        menu_item.click()
        menu_item.click()

        # self.fail("End the test.")
        time.sleep(5)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
