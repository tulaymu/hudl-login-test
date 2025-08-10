from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Small base with common waits/helpers to keep tests clean."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---- waits/helpers ----
    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.wait_clickable(locator).click()

    def type(self, locator, text: str, clear=True):
        el = self.wait_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def url_contains(self, fragment: str) -> bool:
        try:
            self.wait.until(EC.url_contains(fragment))
            return True
        except Exception:
            return False
