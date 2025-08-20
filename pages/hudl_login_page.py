"""Hudl Login Page Object Model"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class HudlLoginPage(BasePage):
    """Page object for Hudl login functionality."""

    HOME_URL = "https://www.hudl.com/"
    FAN_HUDL_URL_FRAGMENT = "fan.hudl.com"

    # Login Selectors
    LOGIN_DROPDOWN_TOGGLE = (By.CSS_SELECTOR, "a[data-qa-id='login-select']")
    LOGIN_OPTION_HUDL     = (By.CSS_SELECTOR, "a[data-qa-id='login-hudl']")
    EMAIL_FIELD     = (By.ID, "username")
    PASSWORD_FIELD  = (By.ID, "password")
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue' and not(@disabled)]")
    
    # User Menu and Logout Selectors (for when logged in)
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
        """Check if user is logged out."""
        # Check if login dropdown is visible
        if self.is_element_present(self.LOGIN_DROPDOWN_TOGGLE, timeout=5):
            return True
        
        # Check if user elements are absent
        return self.is_element_absent(self.USER_NAME_ELEMENTS, timeout=3)

    def logout(self):
        """Logout by hovering over user menu and clicking logout."""
        from selenium.webdriver.common.action_chains import ActionChains
        
        try:
            # First, try to find user menu/profile elements to hover over
            user_menu_selectors = [
                (By.CSS_SELECTOR, "[data-qa-id*='user'], [data-qa-id*='profile']"),
                (By.CSS_SELECTOR, ".user-menu, .profile-menu, [class*='user-menu']"),
                (By.CSS_SELECTOR, "img[class*='avatar'], [class*='avatar']"),
                (By.XPATH, "//div[contains(@class, 'user') or contains(@class, 'profile')]"),
                (By.XPATH, "//button[contains(@class, 'user')]"),
                (By.CSS_SELECTOR, "[class*='display-name'], [class*='user-name']")
            ]
            
            user_menu_found = False
            for selector in user_menu_selectors:
                try:
                    user_menu = self.wait_visible(selector, timeout=3)
                    
                    # Hover over the user menu
                    actions = ActionChains(self.driver)
                    actions.move_to_element(user_menu).perform()
                    
                    # Wait a moment for dropdown to appear
                    import time
                    time.sleep(2)
                    
                    user_menu_found = True
                    break
                except:
                    continue
            
            if user_menu_found:
                # Now try to find and click logout button
                logout_selectors = [
                    (By.XPATH, "//a[contains(text(), 'Log out') or contains(text(), 'Logout')]"),
                    (By.XPATH, "//button[contains(text(), 'Log out') or contains(text(), 'Logout')]"),
                    (By.CSS_SELECTOR, "[data-qa-id*='logout']"),
                    (By.CSS_SELECTOR, "a[href*='logout']"),
                    (By.CSS_SELECTOR, ".logout, [class*='logout']")
                ]
                
                for logout_selector in logout_selectors:
                    try:
                        logout_button = self.wait_clickable(logout_selector, timeout=2)
                        logout_button.click()
                        
                        # Wait for logout to complete
                        time.sleep(2)
                        return
                    except:
                        continue
            
            # If UI logout fails, fallback to cookie clearing
            print("UI logout failed, using cookie clearing fallback")
            self.driver.delete_all_cookies()
            
            try:
                self.driver.execute_script("localStorage.clear();")
                self.driver.execute_script("sessionStorage.clear();")
            except:
                pass
            
            # Go back to home page
            self.driver.get(self.HOME_URL)
            
        except Exception as e:
            print(f"Logout failed: {e}")
            # Fallback to cookie clearing
            self.driver.delete_all_cookies()
            self.driver.get(self.HOME_URL)
