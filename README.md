# Hudl Login Test Suite

Automated tests for Hudl login and logout using **Selenium** and **pytest**.

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
│   └── hudl_login_page.py    # Page Object for Hudl login, logout, and dashboard checks
│
├── tests/
│   └── test_login.py         # Test cases for login and logout functionality
│
├── .env.example              # Placeholder for environment variables (no real credentials)
├── .gitignore                # Git ignore rules (includes .env, .venv, etc.)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

**Notes**
- `.env` is ignored by git and should contain your personal credentials.

- `.env.example` contains only placeholder values for reference.

- Make sure Chrome and ChromeDriver are installed.