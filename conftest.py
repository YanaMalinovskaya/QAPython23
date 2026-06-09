import pytest

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:3000"


@pytest.fixture
def login_page(page):
    from pages.login_page import LoginPage

    login = LoginPage(page)
    login.open()
    login.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    return page
