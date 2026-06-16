import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.search_page import SearchPage

def close_popups(page):
    # 關閉 Welcome popup
    dismiss_welcome = page.locator('button[aria-label="Close Welcome Banner"]')
    if dismiss_welcome.is_visible():
        dismiss_welcome.click()

    # 關閉 Cookie popup
    cookie_button = page.locator('text=Me want it!')
    cookie_button.wait_for(state="visible", timeout=5000)
    cookie_button.click()


@pytest.fixture
def page():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        
        browser.close()

@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def search_page(page):
    return SearchPage(page)


@pytest.fixture
def logged_in_page(page):
    page.goto("http://localhost:3000/#/login")
    close_popups(page)
    login_page = LoginPage(page)
    login_page.login("admin@juice-sh.op", "admin123")
    page.wait_for_function("() => localStorage.getItem('token') !== null")
    return page
        