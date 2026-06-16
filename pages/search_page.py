class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_input = page.locator("div.search-container input")
    

    def open_search(self):
        self.page.get_by_role("button").filter(has=self.page.locator("mat-icon:has-text('search')")).click()



    def search(self, keyword):
    
        self.search_input.wait_for(state="visible", timeout=5000)
        self.search_input.fill("")
        self.search_input.fill(keyword)
        self.search_input.press("Enter")