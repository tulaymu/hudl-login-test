"""Hudl Login Page Object Model"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class HudlLoginPage(BasePage):
    """Page object for Hudl login functionality with robust wait strategies."""

    HOME_URL = "https://www.hudl.com/"
    FAN_HUDL_URL_FRAGMENT = "fan.hudl.com"
    LOGOUT_URL = "https://www.hudl.com/logout"

    # Selectors
    LOGIN_DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a[data-qa-id='login-select']")
    LOGIN_OPTION_HUDL     = (By.CSS_SELECTOR, "a[data-qa-id='login-hudl']")
    EMAIL_FIELD     = (By.ID, "username")
    PASSWORD_FIELD  = (By.ID, "password")
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue' and not(@disabled)]")
    USER_NAME_ELEMENTS = (By.CSS_SELECTOR, "[class*='displayName'], [class*='user-name']")

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
        """Complete login flow with proper waits."""
        self.open_home()
        self.open_login_dropdown_and_choose_hudl()
        self.enter_email(email)
        self.enter_password(password)
        # Wait for successful login by checking URL change
        self.wait_url_contains(self.FAN_HUDL_URL_FRAGMENT, timeout=15)

    def is_on_fan_hudl(self) -> bool:
        """Check if user is on fan.hudl.com with timeout."""
        return self.url_contains(self.FAN_HUDL_URL_FRAGMENT, timeout=5)

    def is_on_login_screen(self) -> bool:
        """Check if user is on login screen by email field visibility."""
        return self.is_element_present(self.EMAIL_FIELD, timeout=3)

    def is_logged_out(self) -> bool:
        """Check if user is logged out by presence of login elements or absence of user elements."""
        # First check if login dropdown is visible (most reliable indicator)
        if self.is_element_present(self.LOGIN_DROPDOWN_TOGGLE, timeout=5):
            return True
        
        # Fallback: check if user name elements are absent
        return self.is_element_absent(self.USER_NAME_ELEMENTS, timeout=3)

    def logout(self):
        """Logout using direct URL and wait for logout confirmation."""
        # Navigate to logout URL
        self.driver.get(self.LOGOUT_URL)
        
        # Navigate back to home page
        self.driver.get(self.HOME_URL)
        
        # Wait for logout to complete by checking for login elements
        self.wait_visible(self.LOGIN_DROPDOWN_TOGGLE, timeout=10)
