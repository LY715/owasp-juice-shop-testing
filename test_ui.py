import logging
import time
from conftest import close_popups
from playwright.sync_api import sync_playwright

#Logger for recording test logs
logger = logging.getLogger(__name__)

Base_URL = "http://localhost:3000"

def test_empty_string():
    
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
        logger.info("【SUCCESS】Clicked search button！")

        # 點擊搜尋放大鏡後按下 Enter
        search_input = page.locator("div.search-container input")
        search_input.wait_for(state="visible", timeout=5000)
        search_input.press("Enter")

        after_searching = page.locator(".mat-mdc-paginator-range-label").inner_text()
        after_total_quantities = after_searching.split(" ")[-1]
        
        assert total_quantities == after_total_quantities, "【ERROR】搜尋空白字串後的結果與原本數量不同"

        logger.info(f"【SUCCESS】搜尋空字串顯示了與搜尋前相同數量的商品:\n Before searching -> {total_quantities} \n After searching -> {after_total_quantities}）！")

def test_search_juice(page):
    """
    自動化測試：Close popup -> Click search on the top right -> Input "juice" -> Validate the result of searching
    """

    # Arrange - 關閉popup，準備好頁面
    page.goto(Base_URL)
    close_popups(page)

        
    # Act - 執行搜尋

    # 點擊搜尋放大鏡圖示
    page.get_by_role("button").filter(has=page.locator("mat-icon:has-text('search')")).click()
    logger.info("【SUCCESS】Clicked search button！")

    # 點擊搜尋放大鏡後在搜尋輸入框內輸入 juice 並按下 Enter
    search_input = page.locator("div.search-container input")
    search_input.wait_for(state="visible", timeout=5000)
    search_input.fill("juice")
    search_input.press("Enter")
    logger.info("【SUCCESS】Successfully searched juice！")


    # Assert - 驗證結果
    # 驗證畫面上是不是只剩下 juice 相關字眼的商品
    product_title = page.locator('text=Apple Juice (1000ml)')
    assert product_title.is_visible(), "錯誤！搜尋結果沒有看到 Apple Juice！"
    logger.info("【SUCCESS】成功在畫面上驗證 Apple Juice 商品存在！")

    # 確認是否每個商品名稱都包含 "juice"
    all_products = []
    while True:
        product_titles = page.locator("div.name").all_text_contents()
        all_products.extend(product_titles)
        logger.info(f"【INFO】目前頁面商品 : {product_titles}")

        next_page_button = page.get_by_role("button", name="Next page")
        if next_page_button.is_disabled():
            break
        next_page_button.click()
        page.wait_for_timeout(5000)

    logger.info(f"【INFO】搜尋商品結果 : {all_products}, 共有 {len(all_products)} 項商品")
    

    # 確認是否每個商品名稱都包含 "juice"
    failed_titles = []
    for title in all_products:
        if "juice" not in title.lower():
            failed_titles.append(title)
    
    assert len(failed_titles) == 0, f"以下商品不是 juice 相關：{failed_titles}"


    
    



        