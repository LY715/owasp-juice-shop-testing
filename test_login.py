import pytest
import logging
import time
from playwright.sync_api import sync_playwright
from conftest import close_popups

logger = logging.getLogger(__name__)
Base_URL = "http://localhost:3000/#/login"

def get_login_elements(page):
    return {

        "email_input": page.locator("#email"),
        "password_input": page.locator("#password"),
        "login_button": page.locator("#loginButton")

    }



def test_login_success(page):
    
    """
    帶入各種正確的帳密以及密碼-> Click Log in
    """

    # Arrange - 關閉popup，準備好頁面
    page.goto(Base_URL)
    close_popups(page)

    # 帶入正確的帳密, 輸出結果需要確認是否有出現Token
    
    # 尚未登入前, 確認是否有無Token存在
    token_before = page.evaluate("() => localStorage.getItem('token')")
    assert token_before is None, "登入前不應該出現Token"

    # 正確的帳號密碼
    elements = get_login_elements(page)
    email = "admin@juice-sh.op"
    password = "admin123"

    elements['email_input'].fill(email)
    elements['password_input'].fill(password)
    elements['login_button'].click()

    token_after = page.evaluate("() => localStorage.getItem('token')")
    assert token_after is not None, "登入後應該要有 Token, 但卻沒有!"
    logger.info(f"【SUCCESS】token 長度：{len(token_after)}")
    

def test_login_wrong_password(page):

    """
    帶入錯誤的帳密, 以及測試空值
    """

    page.goto(Base_URL)
    close_popups(page)

    




    
    
