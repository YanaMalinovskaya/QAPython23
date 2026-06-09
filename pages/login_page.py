from playwright.sync_api import Page, expect

from core.base_page import BasePage


class LoginPage(BasePage):

    path = "/login"
    title = "Task Management Board"

    def __init__(self, page: Page):
        super().__init__(page)
        self.form = page.locator('[data-qa="login-form"]')
        self.title_text = page.locator('[data-qa="login-title"]')
        self.email_input = page.locator('[data-qa="login-email-input"]')
        self.password_input = page.locator('[data-qa="login-password-input"]')
        self.submit_button = page.locator('[data-qa="login-submit-button"]')

    def open(self):
        self.goto(self.path)

    def verify_page_opened(self):
        super().verify_page_opened(self.path, self.title)
        expect(self.form).to_be_visible()
        expect(self.title_text).to_have_text("Вход в систему")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
        expect(self.page).to_have_url(f"{self.domain}/dashboard")
