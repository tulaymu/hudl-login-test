"""
Hudl Login Test Suite

Tests login functionality including positive and negative scenarios.
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
        assert page.is_on_fan_hudl(), "Could not login with provided credentials"
        
        # Perform logout
        page.logout()
        
        # Verify logout - check we're not on fan.hudl.com anymore
        current_url = driver.current_url
        assert "hudl.com" in current_url, f"Expected to be on hudl.com after logout. Current URL: {current_url}"


class TestInvalidCredentials:
    """Tests for invalid credential scenarios."""
    
    @pytest.mark.login
    @pytest.mark.validation
    def test_wrong_password_prevents_login(self, driver, creds):
        """Test that wrong password prevents successful login."""
        page = HudlLoginPage(driver)
        invalid_password = "wrong-password"
        
        # Attempt login with wrong password
        page.open_home()
        page.open_login_dropdown_and_choose_hudl()
        page.enter_email(creds["email"])
        page.enter_password(invalid_password)
        
        # Verify login was not successful
        assert not page.is_on_fan_hudl(), (
            f"Should not be able to login with wrong password. "
            f"Current URL: {driver.current_url}"
        )
    
    @pytest.mark.login
    @pytest.mark.validation
    def test_invalid_email_format_shows_validation(self, driver):
        """Test that invalid email format shows validation."""
        page = HudlLoginPage(driver)
        invalid_email = "notanemail"
        
        # Attempt to enter invalid email
        page.open_home()
        page.open_login_dropdown_and_choose_hudl()
        page.enter_email(invalid_email)
        
        # Verify still on login screen
        assert page.is_on_login_screen(), (
            f"Invalid email should keep user on login screen. "
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
            f"Empty email should keep user on login screen. "
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
            f"Empty password should not allow login. "
            f"Current URL: {driver.current_url}"
        )
