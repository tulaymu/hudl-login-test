import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def creds():
    """Read credentials from .env (kept out of Git)."""
    load_dotenv()
    email = os.getenv("HUDL_EMAIL")
    pwd = os.getenv("HUDL_PASSWORD")
    assert email and pwd, "Please set HUDL_EMAIL and HUDL_PASSWORD in your .env"
    return {"email": email, "password": pwd}

@pytest.fixture
def driver():
    """Start Chrome (headless optional), tidy timeouts, and clean up."""
    opts = Options()
    if os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes"):
        opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    opts.add_argument("--window-size=1400,900")

    drv = webdriver.Chrome(options=opts)  # Selenium Manager resolves the driver
    drv.set_page_load_timeout(25)
    drv.implicitly_wait(2)
    yield drv
    drv.quit()
