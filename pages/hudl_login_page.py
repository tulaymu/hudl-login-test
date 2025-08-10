from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait


class HudlLoginPage(BasePage):
    """Login page object + top‑nav logout."""

    HOME_URL = "https://www.hudl.com/"

    # Public site
    LOGIN_DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a[data-qa-id='login-select']")
    LOGIN_OPTION_HUDL     = (By.CSS_SELECTOR, "a[data-qa-id='login-hudl']")

    # Identity screens
    EMAIL_FIELD     = (By.ID, "username")
    PASSWORD_FIELD  = (By.ID, "password")
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue' and not(@disabled)]")

    # App (logged-in) marker
    TOP_NAV = (By.CSS_SELECTOR, "[data-qa-id='webnav'], nav")

    # User menu + logout (simple, robust selectors)
    USER_MENU_BUTTON = (By.CSS_SELECTOR, "[data-qa-id='webnav-user-menu'], .hui-globalusermenu")
    LOGOUT_BUTTON    = (By.CSS_SELECTOR, "[data-qa-id*='logout'], a[href*='/logout']")

    # --- small helper 
    def _visible(self, locator, timeout: int = 3) -> bool:
        """Return True if locator becomes visible within `timeout` seconds."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    # --- actions 
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
        """Reusable login flow used by tests."""
        self.open_home()
        self.open_login_dropdown_and_choose_hudl()
        self.enter_email(email)
        self.enter_password(password)

    # --- checks 
    def is_dashboard_visible(self) -> bool:
        """True when we land on the app home/dashboard."""
        try:
            self.wait.until(EC.presence_of_element_located(self.TOP_NAV))
            self.url_contains("/home")
            return True
        except Exception:
            return False

    def is_logged_out(self) -> bool:
        """
        True when we’re no longer on /home and we see either:
        - the identity login (email field), or
        - the public site’s Log in dropdown.
        """
        if "/home" in self.driver.current_url:
            return False
        return self._visible(self.EMAIL_FIELD) or self._visible(self.LOGIN_DROPDOWN_TOGGLE)

    # --- logout 
    def logout(self):
        """Open the user menu and click Log out."""
        try:
            # open the user menu
            btn = self.wait_visible(self.USER_MENU_BUTTON)
            try:
                btn.click()
            except Exception:
                ActionChains(self.driver).move_to_element(btn).perform()
                self.wait_clickable(self.USER_MENU_BUTTON).click()

            # click Log out and wait for navigation/visibility change
            old = self.driver.current_url
            self.click(self.LOGOUT_BUTTON)
            try:
                self.wait.until(EC.url_changes(old))
            except Exception:
                pass
        except TimeoutException:
            raise
