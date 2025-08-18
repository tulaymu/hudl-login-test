"""Hudl Login Page Object Model"""
import time
from selenium.webdriver.common.by import By
from .base_page import BasePage


class HudlLoginPage(BasePage):
    """Page object for Hudl login functionality."""

    HOME_URL = "https://www.hudl.com/"

    LOGIN_DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a[data-qa-id='login-select']")
    LOGIN_OPTION_HUDL     = (By.CSS_SELECTOR, "a[data-qa-id='login-hudl']")
    EMAIL_FIELD     = (By.ID, "username")
    PASSWORD_FIELD  = (By.ID, "password")
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue' and not(@disabled)]")

    def open_home(self):
        self.driver.get(self.HOME_URL)

    def open_login_dropdown_and_choose_hudl(self):
        self.click(self.LOGIN_DROPDOWN_TOGGLE)
        self.click(self.LOGIN_OPTION_HUDL)

    def enter_email(self, email: str):
        self.type(self.EMAIL_FIELD, email)
        self.click(self.CONTINUE_BUTTON)

    def enter_password(self, password: str):
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.CONTINUE_BUTTON)

    def login(self, email: str, password: str):
        self.open_home()
        self.open_login_dropdown_and_choose_hudl()
        self.enter_email(email)
        self.enter_password(password)
        time.sleep(3)

    def is_on_fan_hudl(self) -> bool:
        try:
            return "fan.hudl.com" in self.driver.current_url
        except Exception:
            return False

    def is_on_login_screen(self) -> bool:
        try:
            self.wait_visible(self.EMAIL_FIELD)
            return True
        except:
            return False

    def is_logged_out(self) -> bool:
        try:
            # Check if login button is visible (indicates logged out)
            self.wait_visible(self.LOGIN_DROPDOWN_TOGGLE, timeout=5)
            return True
        except:
            # Check if user elements are not visible (indicates logged out)
            user_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='displayName'], [class*='user-name']")
            return len(user_elements) == 0

    def logout(self):
        # Direct logout and return to home page
        self.driver.get("https://www.hudl.com/logout")
        time.sleep(2)
        self.driver.get(self.HOME_URL)
        time.sleep(3)
