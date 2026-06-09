from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.domain = "http://localhost:3000"

    def goto(self, url: str):
        self.page.goto(f"{self.domain}{url}")

    def verify_page_opened(self, url: str, title: str):
        expect(self.page).to_have_url(f"{self.domain}{url}")
        expect(self.page).to_have_title(title)
