import pytest
import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def close_popups(page):
    # 關閉 Welcome popup
    dismiss_welcome = page.locator('button[aria-label="Close Welcome Banner"]')
    if dismiss_welcome.is_visible():
        dismiss_welcome.click()
        logger.info("【SUCCESS】1. Welcome popup closed！")

    # 關閉 Cookie popup
    cookie_button = page.locator('text=Me want it!')
    cookie_button.wait_for(state="visible", timeout=5000)
    cookie_button.click()
    logger.info("【SUCCESS】2. Cookie popup closed！")

@pytest.fixture
def page():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        browser.close()
        