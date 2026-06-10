import time

import pytest
import logging
from playwright.sync_api import sync_playwright
from conftest import close_popups
import json
import random
import string

logger = logging.getLogger(__name__)
Base_URL = "http://localhost:3000/#/login"


# 帳密
CORRECT_EMAIL = "admin@juice-sh.op"
CORRECT_PASSWORD = "admin123"
WRONG_EMAIL = "wrong@email.com"
WRONG_PASSWORD = "wrongpassword"

# Helper Function
def get_login_elements(page):
    return {

        "email_input": page.locator("#email"),
        "password_input": page.locator("#password"),
        "login_button": page.locator("#loginButton")

    }



def test_login_success(page):
    
    """
    帶入正確的帳密以及密碼-> Click Log in
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

    elements['email_input'].fill(CORRECT_EMAIL)
    elements['password_input'].fill(CORRECT_PASSWORD)
    elements['login_button'].click()

    token_after = page.evaluate("() => localStorage.getItem('token')")
    assert token_after is not None, "登入後應該要有 Token, 但卻沒有!"
    logger.info(f"【SUCCESS】Token 長度：{len(token_after)}")
    

def test_login_wrong_password(page):

    """
    帶入錯誤的帳密, 以及測試空值
    """

    page.goto(Base_URL)
    close_popups(page)

    elements = get_login_elements(page)

    # 確認剛進頁面的情況下, 是否log in button是無法點選的
    assert elements['login_button'].is_disabled(), "帳密空白時, Log in 按鈕應為 disabled !"
    logger.info("【SUCCESS】Log in 按鈕已確認為 disabled, 無法點擊!")
    
    # 輸入錯誤帳號密碼
    elements['email_input'].fill(WRONG_EMAIL)
    elements['password_input'].fill(WRONG_PASSWORD)
    elements['login_button'].click()

    invalid_message = page.locator(".error")
    
    invalid_message.wait_for(state='visible', timeout=5000)
    print(invalid_message.inner_text())
    assert invalid_message.is_visible(), "應該要出現Invalid messages 卻沒有!"
    logger.info("【SUCCESS】確認有出現Invalid messages!")


def test_password_plaintext(page):

    page.goto(Base_URL)
    close_popups(page)
    elements = get_login_elements(page)

    password_collections = []
    for i in range(5):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        password_collections.append(password)



    for wrong_password in password_collections:
        
        request_data = []
        page.on("request", lambda request: request_data.append(request))

        elements['email_input'].fill(WRONG_EMAIL)
        elements['password_input'].fill(wrong_password)
        elements['login_button'].click()

        plaintext_password = None

        for request in request_data:
            if "login" in request.url and request.method == "POST":
                post_data = request.post_data
                plaintext_password = json.loads(post_data)["password"]
        
        if plaintext_password is None:
            logger.warning("【WARNING】找不到登入的 POST 請求！")
        elif plaintext_password == wrong_password:
            logger.warning(f"【WARNING】密碼以明文傳輸！發現資安漏洞！ Password: {wrong_password}")
        else:
            logger.info("【SUCCESS】密碼沒有以明文傳輸")
    
    
    
