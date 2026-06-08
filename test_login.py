import pytest
import logging
import time
from playwright.sync_api import sync_playwright
from conftest import close_popups

logger = logging.getLogger(__name__)

Base_URL = "http://localhost:3000/#/login"


def test_login_page(page):
    
    """
    自動化測試：自動帶入各種不同的email以及密碼(include 'OR 1=1 --'-> Click Log in
    """

    # Arrange - 關閉popup，準備好頁面
    page.goto(Base_URL)
    close_popups(page)

    # 登入前的 Token
    token_before = page.evaluate("() => localStorage.getItem('token')")
    assert token_before is None

    # 帶入正確的帳密
    email = "admin@juice-sh.op"
    password = "admin123"

    email_input = page.locator("#email")
    email_input.fill(email)
    
    password_input = page.locator("#password")
    password_input.fill(password)

    login_button = page.locator("#loginButton")
    login_button.click()

    token_after = page.evaluate("() => localStorage.getItem('token')")
    assert token_after is not None, "登入後應該要有 Token, 但卻沒有!"
    

    
    
