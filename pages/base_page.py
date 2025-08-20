from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class BasePage:
    """Base page with wait strategies."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_visible(self, locator, timeout=None):
        """Wait for element to be visible."""
        wait = WebDriverWait(self.driver, timeout or 10)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator, timeout=None):
        """Wait for element to be clickable."""
        wait = WebDriverWait(self.driver, timeout or 10)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator, timeout=10):
        """Wait for element to become invisible."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_url_contains(self, fragment: str, timeout=10):
        """Wait for URL to contain specific fragment."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(fragment))

    def wait_elements_present(self, locator, min_count=1, timeout=10):
        """Wait for minimum number of elements to be present."""
        wait = WebDriverWait(self.driver, timeout)
        elements = wait.until(lambda driver: driver.find_elements(*locator))
        if len(elements) < min_count:
            raise TimeoutException(f"Expected at least {min_count} elements, found {len(elements)}")
        return elements

    def click(self, locator, timeout=None):
        """Click element with explicit wait."""
        element = self.wait_clickable(locator, timeout)
        element.click()
        return element

    def type(self, locator, text: str, clear=True, timeout=None):
        """Type text with explicit wait."""
        element = self.wait_visible(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)
        return element

    def is_element_present(self, locator, timeout=3):
        """Check if element is present."""
        try:
            self.wait_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_absent(self, locator, timeout=3):
        """Check if element is absent."""
        try:
            elements = self.driver.find_elements(*locator)
            return len(elements) == 0
        except Exception:
            return True

    def url_contains(self, fragment: str, timeout=10) -> bool:
        """Check if URL contains fragment."""
        try:
            self.wait_url_contains(fragment, timeout)
            return True
        except TimeoutException:
            return False
