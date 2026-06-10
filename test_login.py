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

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def test_login_success(page):
    
    """
    帶入正確的帳密以及密碼-> Click Log in -> 輸出結果需要確認是否有出現Token -> 若有, 視為正確登入; 若無則視為登入失敗
    """

    page.goto(Base_URL)
    close_popups(page)
    
    # 尚未登入前, 確認是否有無Token存在
    token_before = page.evaluate("() => localStorage.getItem('token')")
    assert token_before is None, "Token should not exist before login"

    # 正確的帳號密碼
    elements = get_login_elements(page)

    elements['email_input'].fill(CORRECT_EMAIL)
    elements['password_input'].fill(CORRECT_PASSWORD)
    elements['login_button'].click()

    token_after = page.evaluate("() => localStorage.getItem('token')")
    assert token_after is not None, "Token should exist after login, but it was not found"
    logger.info(f"Length of Token：{len(token_after)}")
    

def test_login_wrong_password(page):

    """
    帶入錯誤的帳密, 以及測試空值
    """

    page.goto(Base_URL)
    close_popups(page)

    elements = get_login_elements(page)

    # 確認剛進頁面的情況下, 是否log in button是無法點選的
    assert elements['login_button'].is_disabled(), "Login button should be disabled when email and password are empty"
    logger.info("Login button is confirmed disabled and cannot be clicked")
    
    # 輸入錯誤帳號密碼
    elements['email_input'].fill(WRONG_EMAIL)
    elements['password_input'].fill(WRONG_PASSWORD)
    elements['login_button'].click()

    invalid_message = page.locator(".error")
    
    invalid_message.wait_for(state='visible', timeout=5000)
    print(invalid_message.inner_text())
    assert invalid_message.is_visible(), "Invalid message should appear but was not found"
    logger.info("Invalid message is confirmed visible")


def test_password_plaintext(page):

    page.goto(Base_URL)
    close_popups(page)
    elements = get_login_elements(page)

    password_collections = []
    for i in range(5):
        password = random_password()
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
            logger.warning("Log in Post request not found")
        elif plaintext_password == wrong_password:
            logger.warning(f"Password is transmitted in plaintext！ Password: {wrong_password}")
        else:
            logger.info("Password is not transmitted in plaintext")
    
    
def test_login_invalid_email(page):
    
    invalid_email = "admin#juice-sh.op"

    page.goto(Base_URL)
    close_popups(page)
    
    elements = get_login_elements(page)

    elements['email_input'].fill(invalid_email)
    elements['password_input'].fill(random_password())
    
    
    if elements['login_button'].is_disabled():
        logger.info("Login button is disabled for invalid email format - Frontend validation is working")
    else:
        logger.warning("Login button is not disabled for invalid email format - Frontend validation is not working")



def test_login_sql_injection(page):

    page.goto(Base_URL)
    close_popups(page)

    sqlInjection = "' OR 1=1--"

    elements = get_login_elements(page)

    elements['email_input'].fill(sqlInjection)
    elements['password_input'].fill(random_password())
    elements['login_button'].click()

    token = page.evaluate("() => localStorage.getItem('token')")
    
    if token is not None:
        logger.warning("SQL Injection succeeded! Vulnerability detected!")
    else:
        logger.info("SQL Injection failed!")
    