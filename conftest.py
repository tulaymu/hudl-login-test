import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def test_config():
    """Load test configuration from environment."""
    load_dotenv()
    return {
        "browser": os.getenv("BROWSER", "chrome").lower(),
        "headless": os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes"),
        "window_size": os.getenv("WINDOW_SIZE", "1400,900"),
        "implicit_wait": int(os.getenv("IMPLICIT_WAIT", "2")),
        "page_load_timeout": int(os.getenv("PAGE_LOAD_TIMEOUT", "25"))
    }


@pytest.fixture(scope="session")
def creds():
    """Read credentials from .env (kept out of Git)."""
    load_dotenv()
    email = os.getenv("HUDL_EMAIL")
    pwd = os.getenv("HUDL_PASSWORD")
    
    if not email or not pwd:
        pytest.fail(
            "Missing credentials: Please set HUDL_EMAIL and HUDL_PASSWORD in your .env file\n"
            "Copy .env.example to .env and fill in your credentials"
        )
    
    return {"email": email, "password": pwd}


@pytest.fixture
def driver(test_config):
    """Initialize browser driver with configuration."""
    browser = test_config["browser"]
    
    if browser == "chrome":
        options = ChromeOptions()
        if test_config["headless"]:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument(f"--window-size={test_config['window_size']}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        
    elif browser == "firefox":
        options = FirefoxOptions()
        if test_config["headless"]:
            options.add_argument("--headless")
        width, height = test_config["window_size"].split(",")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")
        
        driver = webdriver.Firefox(options=options)
        
    else:
        pytest.fail(f"Unsupported browser: {browser}. Use 'chrome' or 'firefox'")
    
    # Configure timeouts
    driver.set_page_load_timeout(test_config["page_load_timeout"])
    driver.implicitly_wait(test_config["implicit_wait"])
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(autouse=True)
def test_cleanup(driver):
    """Cleanup after each test."""
    yield
    # Clear cookies and local storage after each test
    try:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
    except Exception:
        pass  # Ignore cleanup errors


@pytest.fixture
def test_data():
    """Provide test data for various scenarios."""
    return {
        "invalid_emails": [
            "notanemail",
            "@invalid.com",
            "missing-domain@",
            "spaces in@email.com"
        ],
        "invalid_passwords": [
            "",
            "short",
            "definitely-not-the-right-password"
        ],
        "timeouts": {
            "quick": 3,
            "normal": 10,
            "slow": 30
        }
    }
