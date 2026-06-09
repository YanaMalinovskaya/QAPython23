from playwright.sync_api import Page, expect

from core.base_page import BasePage


class BoardsPage(BasePage):

    path = "/boards"
    title = "Task Management Board"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_block = page.locator('[data-qa="boards-page"]')
        self.page_title = page.locator('[data-qa="boards-page-title"]')
        self.create_button = page.locator('[data-qa="boards-create-board-button"]')

    def open(self):
        self.goto(self.path)

    def verify_page_opened(self):
        super().verify_page_opened(self.path, self.title)
        expect(self.page_block).to_be_visible()
        expect(self.page_title).to_have_text("Доски")
        expect(self.create_button).to_be_visible()
