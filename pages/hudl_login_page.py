"""
Hudl Login Page Object Model
Handles login flow, logout functionality, and login state detection.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage


class HudlLoginPage(BasePage):
    """
    Page object for Hudl login functionality.
    
    Handles:
    - Login flow from homepage through email/password entry
    - Logout with hover-based user menu interaction  
    - Login state detection (fan.hudl.com vs login screens)
    """

    HOME_URL = "https://www.hudl.com/"

    # Public site
    LOGIN_DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a[data-qa-id='login-select']")
    LOGIN_OPTION_HUDL     = (By.CSS_SELECTOR, "a[data-qa-id='login-hudl']")

    # Identity screens
    EMAIL_FIELD     = (By.ID, "username")
    PASSWORD_FIELD  = (By.ID, "password")
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue' and not(@disabled)]")

    # User menu + logout (improved selectors with fallbacks)
    USER_MENU_BUTTON = (By.CSS_SELECTOR, "[data-qa-id='webnav-user-menu'], .hui-globalusermenu, [class*='user'], [class*='avatar'], [class*='profile']")
    LOGOUT_BUTTON    = (By.CSS_SELECTOR, "[data-qa-id*='logout'], a[href*='/logout']")
    LOGOUT_BUTTON_XPATH = (By.XPATH, "//a[contains(text(), 'Log out')] | //a[contains(text(), 'Logout')] | //button[contains(text(), 'Log out')] | //button[contains(text(), 'Logout')]")
    
    # Login button for logged-out state detection
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[href*='login'], .login-button")
    LOGIN_BUTTON_XPATH = (By.XPATH, "//button[contains(text(), 'Log In')] | //a[contains(text(), 'Log In')]")

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
        # Wait for login to complete and redirect
        time.sleep(3)

    # --- checks 
    def is_on_fan_hudl(self) -> bool:
        """True when we successfully logged in and are on fan.hudl.com"""
        try:
            current_url = self.driver.current_url
            return "fan.hudl.com" in current_url
        except Exception:
            return False

    def is_on_login_screen(self) -> bool:
        """True when we're on the login screen (email field visible)"""
        return self._visible(self.EMAIL_FIELD, timeout=3)

    def is_logged_out(self) -> bool:
        """
        True when we can see the Log In button (indicating logged out state)
        OR when we're still on the login/email screens
        """
        return (self._visible(self.LOGIN_BUTTON, timeout=5) or 
                self._visible(self.LOGIN_DROPDOWN_TOGGLE, timeout=5) or
                self._visible(self.LOGIN_BUTTON_XPATH, timeout=5) or
                self._visible(self.EMAIL_FIELD, timeout=5))

    # --- logout with improved hover mechanism
    def logout(self):
        """Open the user menu using hover and click Log out."""
        try:
            # Find the user menu button with more robust search
            user_menu_elements = self.driver.find_elements(*self.USER_MENU_BUTTON)
            if not user_menu_elements:
                raise TimeoutException("User menu button not found")
            
            btn = user_menu_elements[0]
            
            # Use ActionChains to hover over the user menu to reveal logout
            actions = ActionChains(self.driver)
            actions.move_to_element(btn).perform()
            
            # Wait a moment for the dropdown to appear
            time.sleep(1)
            
            # Try to find logout button with CSS selector first, then XPath
            logout_elements = self.driver.find_elements(*self.LOGOUT_BUTTON)
            if not logout_elements:
                logout_elements = self.driver.find_elements(*self.LOGOUT_BUTTON_XPATH)
            
            if logout_elements:
                logout_elements[0].click()
            else:
                # Fallback: click the user menu first then try logout
                btn.click()
                time.sleep(1)
                
                # Try CSS selector first
                try:
                    logout_element = self.wait_visible(self.LOGOUT_BUTTON)
                    logout_element.click()
                except:
                    # Try XPath selector
                    logout_element = self.wait_visible(self.LOGOUT_BUTTON_XPATH)
                    logout_element.click()
            
            # Wait for logout to complete
            time.sleep(2)
            
        except TimeoutException:
            raise
        except Exception as e:
            # Final fallback: try just clicking user menu and any logout link
            try:
                btn = self.wait_visible(self.USER_MENU_BUTTON)
                btn.click()
                time.sleep(1)
                
                # Try to find any element with "logout" text
                logout_element = self.driver.find_element(By.XPATH, "//*[contains(translate(text(), 'LOGOUT', 'logout'), 'logout')]")
                logout_element.click()
                time.sleep(2)
            except Exception:
                raise Exception(f"Logout failed: {str(e)}")
