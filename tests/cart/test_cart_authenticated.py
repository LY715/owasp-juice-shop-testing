import pytest
from conftest import close_popups

Base_URL = "http://localhost:3000"

@pytest.mark.authenticated
def test_add_item_to_cart_authenticated(page, logged_in_page):

    page = logged_in_page
    page.goto(Base_URL)
    

    before = page.locator('.fa-layers-counter').inner_text()

    page.locator('button[aria-label="Add to Basket"]').first.click() # add item button
    after = page.locator('.fa-layers-counter').inner_text()

    assert int(after) > int(before), "Cart count did not increase after adding item"    


