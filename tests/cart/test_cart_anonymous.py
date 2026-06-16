import random
import pytest
from conftest import close_popups
import time


Base_URL = "http://localhost:3000"

def test_add_item_to_cart(page):
    
    page.goto(Base_URL)
    close_popups(page)

    before = page.locator('.fa-layers-counter').inner_text()

    page.locator('button[aria-label="Add to Basket"]').first.click() # add item button
    after = page.locator('.fa-layers-counter').inner_text()

    assert int(after) > int(before), "Cart count did not increase after adding item"
    

def test_add_all_item_to_cart(page):
    
    page.goto(Base_URL)
    close_popups(page)

    total_buttons = 0

    while True:
        buttons = page.locator('button[aria-label="Add to Basket"]')
        count = buttons.count()
        for i in range(count):
            buttons.nth(i).click()
        total_buttons += count

        next_page_button = page.get_by_role('button', name='Next page')
        if next_page_button.is_disabled():
            break

        next_page_button.click()
        page.wait_for_selector('.btn-basket')

    total_quantities = int(page.locator('.fa-layers-counter').inner_text())

    assert total_quantities == total_buttons, "Cart count did not increase after adding item"

def test_random_cart_item_count(page):

    page.goto(Base_URL)
    close_popups(page)
    
    buttons = page.locator('button[aria-label="Add to Basket"]')
    all_buttons = buttons.all()
    #names = page.locator("div.name").all_text_contents()

    random_count = random.randint(1, buttons.count())
    indices = random.sample(range(len(all_buttons)), random_count) # 從 all_buttons 的長度範圍內，隨機取出 random_count 個不重複的編號
    #print(f"總共要找的數量: {random_count}, 商品: {[i+1 for i in indices]}")


    for i in indices:
        #print(names[i])
        all_buttons[i].click()


    total_quantities = int(page.locator('.fa-layers-counter').inner_text())
    assert total_quantities == random_count, "Cart count does not match the number of items added"


def test_remove_item_from_cart(page):

    page.goto(Base_URL)
    close_popups(page)

    # Add items into basket

    buttons = page.locator('button[aria-label="Add to Basket"]')
    all_buttons = buttons.all()
    names = page.locator("div.name").all_text_contents()
    random_count = random.randint(1, len(all_buttons))
    print()
    total_added = 0
    for i in range(random_count):
        random_increase = random.randint(1, 2)
        total_added += random_increase
        
        for j in range(random_increase):
            print(f"{names[i]} clicked: {j+1}")
            buttons.nth(i).click()
            
    
    total_quantities = int(page.locator('.fa-layers-counter').inner_text())
    assert total_quantities == total_added, "Cart count does not match"


    # Remove from basket
    page.locator('button[aria-label="Show the shopping cart"]').click()
    
    remove_button = page.locator('button:has(svg.fa-trash-alt)')
    quantities = page.locator('span.cell-initial-font')
    random_idx = random.randint(0, remove_button.count() - 1)
    n = int(quantities.nth(random_idx).inner_text())
    remove_button.nth(random_idx).click()
    
    result = total_quantities - n
    basket_result = int(page.locator('.fa-layers-counter').inner_text())

    assert result == basket_result, "Remove action not work!"


    