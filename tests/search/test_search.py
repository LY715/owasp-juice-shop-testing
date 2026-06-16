import logging
import random
import string
from conftest import close_popups
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

Base_URL = "http://localhost:3000"


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

        # Click on search button
        page.get_by_role("button").filter(has=page.locator("mat-icon:has-text('search')")).click()
        logger.info("Clicked search button！")

        # Search
        search_input = page.locator("div.search-container input")
        search_input.wait_for(state="visible", timeout=5000)
        search_input.press("Enter")

        after_searching = page.locator(".mat-mdc-paginator-range-label").inner_text()
        after_total_quantities = after_searching.split(" ")[-1]
        
        assert total_quantities == after_total_quantities, "Search results after empty string search does not match the original quantity!"


def test_search_juice(page, search_page):
    """
    測試：Click search on the top right -> Input "juice" -> Validate the result of searching
    """

    page.goto(Base_URL)
    close_popups(page)
    
    # Search for juice
    search_page.open_search()
    search_page.search("juice")


    product_title = page.locator('div.name').first.inner_text()
    assert 'juice' in product_title.lower(), "Apple Juice not found in search results！"
    logger.info("Apple Juice is visible in search results！")

    all_products = []
    while True:
        product_titles = page.locator("div.name").all_text_contents()
        all_products.extend(product_titles)

        next_page_button = page.get_by_role("button", name="Next page")
        if next_page_button.is_disabled():
            break
        next_page_button.click()
        page.wait_for_selector("div.name")

    logger.info(f"Search results : {all_products}, Total: {len(all_products)} items")
    

    # Verify all search results are juice related
    failed_titles = []
    for title in all_products:
        if "juice" not in title.lower():
            failed_titles.append(title)
    
    assert len(failed_titles) == 0, f"Found {len(failed_titles)} non juice products: {failed_titles}"


    
def test_search_case_insensitive(page, search_page):
    
    page.goto(Base_URL)
    close_popups(page)
    search_page.open_search()
    
    keywords = ['juice', 'JUICE', ''.join(random.choice([c.lower(), c.upper()]) for c in 'juice')]

    product_quantities = []
    for keyword in keywords:
        search_page.search(keyword)
        count = page.locator(".mat-mdc-paginator-range-label").inner_text().split(" ")[-1]
        product_quantities.append(count)

    assert product_quantities[0] == product_quantities[1] == product_quantities[2]
        

def test_search_special_characters(page, search_page):
    
    page.goto(Base_URL)
    close_popups(page)
    search_page.open_search()
    
    keywords = ["<script>test</script>","' OR 1=1--", ''.join(random.choices(string.punctuation, k=10))]

    for keyword in keywords:
        search_page.search(keyword)
        assert page.locator("span:has-text('Search Results')").is_visible(), f"Page crashed after input: {keyword}"


def test_search_trim(page, search_page):

    """Test for trim in the front and back"""
    
    page.goto(Base_URL)
    close_popups(page)
    search_page.open_search()

    product_quantities = []
    keywords = [" juice", "juice ", " juice "]
    for keyword in keywords:
        search_page.search(keyword)
        count = page.locator(".mat-mdc-paginator-range-label").inner_text().split(" ")[-1]
        product_quantities.append(count)

    assert product_quantities[0] == product_quantities[1] == product_quantities[2], "Trim is not working, search results are different"

