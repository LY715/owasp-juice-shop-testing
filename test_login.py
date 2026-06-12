import logging
import json
import random
import string
from conftest import close_popups
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)
Base_URL = "http://localhost:3000/#/login"


# 帳密
CORRECT_EMAIL = "admin@juice-sh.op"
CORRECT_PASSWORD = "admin123"
WRONG_EMAIL = "wrong@email.com"
WRONG_PASSWORD = "wrongpassword"


def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def test_login_success(page):
    
    """
    帶入正確的帳密以及密碼-> Click Log in -> 輸出結果需要確認是否有出現Token -> 若有, 視為正確登入; 若無則視為登入失敗
    """

    page.goto(Base_URL)
    close_popups(page)
    
    # 確認是否有無Token存在
    token_before = page.evaluate("() => localStorage.getItem('token')")
    assert token_before is None, "Token should not exist before login"

    # 正確的帳號密碼
    login_page = LoginPage(page)
    login_page.login(CORRECT_EMAIL, CORRECT_PASSWORD)

    token_after = page.evaluate("() => localStorage.getItem('token')")
    assert token_after is not None, "Token should exist after login, but it was not found"
    logger.info(f"Length of Token：{len(token_after)}")
    

def test_login_wrong_password(page):

    """
    帶入錯誤的帳密, 以及測試空值
    """

    page.goto(Base_URL)
    close_popups(page)

    login_page = LoginPage(page)
    
    # log in button是無法點選的
    assert login_page.login_button.is_disabled(), "Login button should be disabled when email and password are empty"
    logger.info("Login button is confirmed disabled and cannot be clicked")
    
    # 輸入錯誤帳號密碼
    login_page.login(WRONG_EMAIL, WRONG_PASSWORD)

    invalid_message = page.locator(".error")
    
    invalid_message.wait_for(state='visible', timeout=5000)
    print(invalid_message.inner_text())
    assert invalid_message.is_visible(), "Invalid message should appear but was not found"
    logger.info("Invalid message is confirmed visible")


def test_password_plaintext(page):

    page.goto(Base_URL)
    close_popups(page)
    login_page = LoginPage(page)

    password_collections = []
    for i in range(5):
        password = random_password()
        password_collections.append(password)


    for wrong_password in password_collections:
        
        request_data = []
        page.on("request", lambda request: request_data.append(request))

        login_page.login(WRONG_EMAIL, wrong_password)

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
    
    login_page = LoginPage(page)

    login_page.email.fill(invalid_email)
    login_page.password.fill(random_password())
    
    
    assert login_page.login_button.is_disabled(), "Login button should be disabled for invalid email format"



def test_login_sql_injection(page):

    page.goto(Base_URL)
    close_popups(page)

    sqlInjection = "' OR 1=1--"

    login_page = LoginPage(page)

    login_page.login(sqlInjection, random_password())

    token = page.evaluate("() => localStorage.getItem('token')")
    
    assert token is None, "SQL Injection succeeded! Vulnerability detected!"
    