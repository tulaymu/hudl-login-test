# Hudl Login Test Suite

Automated tests for Hudl login and logout functionality using **Selenium** and **pytest**.

## Features

✅ **Login Success**: Tests successful login and detection of landing on `fan.hudl.com`  
✅ **Logout Functionality**: Tests logout using hover-based user menu interaction  
✅ **Error Handling**: Tests various error scenarios (wrong password, invalid email, empty fields)  
✅ **Robust Selectors**: Uses multiple fallback selectors for reliable element detection

## Test Cases

- `test_login_success` - Verifies successful login lands on fan.hudl.com
- `test_logout_after_login` - Tests complete login -> logout flow 
- `test_login_wrong_password_shows_error` - Verifies wrong password doesn't log in
- `test_login_invalid_email_format` - Tests invalid email stays on login screen
- `test_login_empty_email_field` - Tests empty email validation
- `test_login_empty_password` - Tests empty password validation

## Setup

### 1. **Clone the repository**
```bash
git clone https://github.com/tulaymu/hudl-login-test.git
cd hudl-login-test
```

### 2. **Create a .env file**

Copy the `.env.example` file and fill in your own credentials:

```bash
cp .env.example .env
```

**Example `.env`:**

```bash
HUDL_EMAIL=your-email@example.com
HUDL_PASSWORD=your-password
HEADLESS=true
```

### 3. **Create a virtual environment & install dependencies**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. **Run tests**
```bash
pytest -q
```
or to see more details you can use:

```bash
pytest -vv -s
```

### **Project Structure**

```bash
hudl-login-test/
│
├── pages/
│   ├── base_page.py          # Base class with common Selenium helper methods
│   └── hudl_login_page.py    # Page Object for Hudl login, logout, and state detection
│
├── tests/
│   └── test_login.py         # Test cases for login success, logout, and error scenarios
│
├── .env.example              # Placeholder for environment variables (no real credentials)
├── .gitignore                # Git ignore rules (includes .env, .venv, etc.)
├── conftest.py               # Pytest configuration and fixtures
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Technical Details

- **Page Object Model**: Clean separation between test logic and page interactions
- **Robust Element Selection**: Multiple fallback selectors (CSS + XPath) for reliability  
- **Login State Detection**: Accurately detects fan.hudl.com vs login screens
- **Hover-based Logout**: Handles user menu interactions that require mouse hover
- **Environment Configuration**: Supports headless mode and credential management

**Notes**
- `.env` is ignored by git and should contain your personal credentials.
- `.env.example` contains only placeholder values for reference.
- Make sure Chrome and ChromeDriver are installed.
- Tests automatically detect successful login by checking for `fan.hudl.com` URL.