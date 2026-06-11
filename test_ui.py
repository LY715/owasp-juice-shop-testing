import logging
import time
from conftest import close_popups
from playwright.sync_api import sync_playwright
import random

#Logger for recording test logs
logger = logging.getLogger(__name__)

Base_URL = "http://localhost:3000"


def search_keywords(page, keyword):

    search_input = page.locator("div.search-container input")
    search_input.wait_for(state="visible", timeout=5000)
    search_input.fill("")
    search_input.fill(keyword)
    search_input.press("Enter")

def test_empty_string():
    
    """
    測試：Click search on the top right -> Click search -> Validate the result of searching
    """

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True, slow_mo=500)
        page = browser.new_page()
        page.goto(Base_URL)
        close_popups(page)

        # 紀錄搜尋空字串前應有的商品數量
        before_searching = page.locator(".mat-mdc-paginator-range-label").inner_text()
        total_quantities = before_searching.split(" ")[-1]
        print(total_quantities)

        # 點擊搜尋放大鏡圖示
        page.get_by_role("button").filter(has=page.locator("mat-icon:has-text('search')")).click()
        logger.info("Clicked search button！")

        # 點擊搜尋放大鏡後按下 Enter
        search_input = page.locator("div.search-container input")
        search_input.wait_for(state="visible", timeout=5000)
        search_input.press("Enter")

        after_searching = page.locator(".mat-mdc-paginator-range-label").inner_text()
        after_total_quantities = after_searching.split(" ")[-1]
        
        assert total_quantities == after_total_quantities, "Search results after empty string search does not match the original quantity!"
        logger.info(f"Empty string search shows the same number of products as before searching:\n Before searching -> {total_quantities} \n After searching -> {after_total_quantities}）！")


def test_search_juice(page):
    """
    測試：Click search on the top right -> Input "juice" -> Validate the result of searching
    """

    page.goto(Base_URL)
    close_popups(page)

    # Search for juice
    page.get_by_role("button").filter(has=page.locator("mat-icon:has-text('search')")).click()

    search_input = page.locator("div.search-container input")
    search_input.wait_for(state="visible", timeout=5000)
    search_input.fill("juice")
    search_input.press("Enter")


    # 驗證畫面上是不是只剩下 juice 相關字眼的商品
    product_title = page.locator('text=Apple Juice (1000ml)')
    assert product_title.is_visible(), "Apple Juice not found in search results！"
    logger.info("Apple Juice is visible in search results！")

    all_products = []
    while True:
        product_titles = page.locator("div.name").all_text_contents()
        all_products.extend(product_titles)

        next_page_button = page.get_by_role("button", name="Next page")
        if next_page_button.is_disabled():
            break
        next_page_button.click()
        page.wait_for_timeout(5000)

    logger.info(f"Search results : {all_products}, Total: {len(all_products)} items")
    

    # 確認是否每個商品名稱都包含 "juice"
    failed_titles = []
    for title in all_products:
        if "juice" not in title.lower():
            failed_titles.append(title)
    
    if len(failed_titles) > 0:
        logger.warning(f"Found {len(failed_titles)} non juice products：{failed_titles}")
    else:
        logger.info("Search results are relevant to 'juice'！")


    
def test_search_case_insensitive(page):
    
    page.goto(Base_URL)
    close_popups(page)

    
    keywords = ['juice', 'JUICE', ''.join(random.choice([c.lower(), c.upper()]) for c in 'juice')]

    page.get_by_role("button").filter(has=page.locator("mat-icon:has-text('search')")).click()

    all_product_titles = []
    for keyword in keywords:
        search_keywords(page, keyword)
        count = page.locator(".mat-mdc-paginator-range-label").inner_text().split(" ")[-1]
        all_product_titles.append(count)

    assert all_product_titles[0] == all_product_titles[1] == all_product_titles[2]
        



        