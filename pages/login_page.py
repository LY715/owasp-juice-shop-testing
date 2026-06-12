class LoginPage:
    def __init__(self, page):
        self.email = page.locator("#email")
        self.password = page.locator("#password")
        self.login_button = page.locator("#loginButton")

    def login(self, email, password):
        self.email.fill(email)
        self.password.fill(password)
        self.login_button.click()
