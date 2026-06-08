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

    page.goto(Base_URL)
    close_popups(page)

    logger.info("我正在睡覺")
    time.sleep(5)
