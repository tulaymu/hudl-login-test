from pages.hudl_login_page import HudlLoginPage

# happy path
def test_login_success(driver, creds):
    page = HudlLoginPage(driver)
    page.login(creds["email"], creds["password"])
    assert page.is_dashboard_visible(), "Expected dashboard after valid login."

# logout 
def test_logout_after_login(driver, creds):
    page = HudlLoginPage(driver)
    page.login(creds["email"], creds["password"])
    assert page.is_dashboard_visible(), "Precondition failed: not logged in."
    page.logout()
    assert page.is_logged_out(), "Expected to be logged out and back on login screen."

#  negative: wrong password 
def test_login_wrong_password_shows_error(driver, creds):
    page = HudlLoginPage(driver)
    page.open_home()
    page.open_login_dropdown_and_choose_hudl()
    page.enter_email(creds["email"])
    page.enter_password("definitely-not-the-right-password")
    assert not page.is_dashboard_visible(), "Should not be logged in with wrong password."

#  negative: invalid email format 
def test_login_invalid_email_format(driver):
    page = HudlLoginPage(driver)
    page.open_home()
    page.open_login_dropdown_and_choose_hudl()
    page.enter_email("notanemail")
    assert page.is_logged_out(), "Invalid email should keep you on login with an error."

#  negative: empty fields 
def test_login_empty_email_field(driver):
    page = HudlLoginPage(driver)
    page.open_home()
    page.open_login_dropdown_and_choose_hudl()
    page.click(page.CONTINUE_BUTTON)
    assert page.is_logged_out(), "Empty email should keep you on login page."

def test_login_empty_password(driver, creds):
    page = HudlLoginPage(driver)
    page.open_home()
    page.open_login_dropdown_and_choose_hudl()
    page.enter_email(creds["email"])
    page.click(page.CONTINUE_BUTTON)
    assert not page.is_dashboard_visible(), "Empty password must not log you in."
