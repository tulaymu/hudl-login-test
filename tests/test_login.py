"""
Hudl Login Test Suite

Tests login functionality including positive and negative scenarios.
Organized into logical test classes with descriptive assertions.
"""
import pytest
from pages.hudl_login_page import HudlLoginPage


class TestSuccessfulLogin:
    """Tests for successful login scenarios."""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_credentials_login_success(self, driver, creds):
        """Test that valid credentials successfully log in to fan.hudl.com."""
        page = HudlLoginPage(driver)
        
        # Perform login
        page.login(creds["email"], creds["password"])
        
        # Verify successful login
        assert page.is_on_fan_hudl(), (
            f"Expected to be redirected to fan.hudl.com after successful login with email: {creds['email']}. "
            f"Current URL: {driver.current_url}"
        )


class TestLogout:
    """Tests for logout functionality."""
    
    @pytest.mark.smoke
    @pytest.mark.logout
    def test_logout_after_successful_login(self, driver, creds):
        """Test that user can successfully logout after logging in."""
        page = HudlLoginPage(driver)
        
        # Setup: Login first
        page.login(creds["email"], creds["password"])
        assert page.is_on_fan_hudl(), (
            f"Precondition failed: Could not login with credentials {creds['email']}. "
            f"Current URL: {driver.current_url}"
        )
        
        # Perform logout
        page.logout()
        
        # Verify logout was successful
        assert page.is_logged_out(), (
            f"Expected to be logged out with login elements visible. "
            f"Current URL: {driver.current_url}. "
            f"Login dropdown visible: {page.is_element_present(page.LOGIN_DROPDOWN_TOGGLE)}"
        )


class TestInvalidCredentials:
    """Tests for invalid credential scenarios."""
    
    @pytest.mark.login
    @pytest.mark.validation
    def test_wrong_password_prevents_login(self, driver, creds):
        """Test that wrong password prevents successful login."""
        page = HudlLoginPage(driver)
        invalid_password = "definitely-not-the-right-password"
        
        # Attempt login with wrong password
        page.open_home()
        page.open_login_dropdown_and_choose_hudl()
        page.enter_email(creds["email"])
        page.enter_password(invalid_password)
        
        # Verify login was not successful
        assert not page.is_on_fan_hudl(), (
            f"Should not be able to login to fan.hudl.com with wrong password '{invalid_password}' "
            f"for email {creds['email']}. Current URL: {driver.current_url}"
        )
    
    @pytest.mark.login
    @pytest.mark.validation
    def test_invalid_email_format_shows_validation(self, driver):
        """Test that invalid email format shows validation and prevents progression."""
        page = HudlLoginPage(driver)
        invalid_email = "notanemail"
        
        # Attempt to enter invalid email
        page.open_home()
        page.open_login_dropdown_and_choose_hudl()
        page.enter_email(invalid_email)
        
        # Verify still on login screen
        assert page.is_on_login_screen(), (
            f"Invalid email format '{invalid_email}' should keep user on login screen with email field visible. "
            f"Current URL: {driver.current_url}"
        )


class TestEmptyFields:
    """Tests for empty field validation."""
    
    @pytest.mark.validation
    def test_empty_email_field_validation(self, driver):
        """Test that empty email field prevents progression."""
        page = HudlLoginPage(driver)
        
        # Attempt to continue with empty email
        page.open_home()
        page.open_login_dropdown_and_choose_hudl()
        page.click(page.CONTINUE_BUTTON)
        
        # Verify still on login screen
        assert page.is_on_login_screen(), (
            f"Empty email field should keep user on login screen with email field visible. "
            f"Current URL: {driver.current_url}"
        )
    
    @pytest.mark.validation
    def test_empty_password_field_prevents_login(self, driver, creds):
        """Test that empty password field prevents successful login."""
        page = HudlLoginPage(driver)
        
        # Attempt login with empty password
        page.open_home()
        page.open_login_dropdown_and_choose_hudl()
        page.enter_email(creds["email"])
        page.click(page.CONTINUE_BUTTON)
        
        # Verify login was not successful
        assert not page.is_on_fan_hudl(), (
            f"Empty password should not allow login to fan.hudl.com for email {creds['email']}. "
            f"Current URL: {driver.current_url}"
        )
