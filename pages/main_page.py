from playwright.sync_api import Page, expect

from core.base_page import BasePage


class MainPage(BasePage):

    path = "/dashboard"
    title = "Task Management Board"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_block = page.locator('[data-qa="dashboard-page"]')
        self.page_title = page.locator('[data-qa="dashboard-title"]')
        self.user_button = page.locator('[data-qa="header-user-info"]')
        self.username = page.locator('[data-qa="header-username"]')
        self.logout_button = page.locator('[data-qa="header-logout-button"]')
        self.boards_link = page.locator('[data-qa="sidebar-boards-link"]')
        self.tasks_link = page.locator('[data-qa="sidebar-tasks-link"]')

    def open(self):
        self.goto(self.path)

    def verify_page_opened(self):
        super().verify_page_opened(self.path, self.title)
        expect(self.page_block).to_be_visible()
        expect(self.page_title).to_have_text("Панель управления")

    def open_user_menu(self):
        self.user_button.click()

    def verify_user_info(self, username: str, email: str):
        self.open_user_menu()
        expect(self.username).to_have_text(username)
        expect(self.page.locator(".header-user-dropdown-email")).to_have_text(email)

    def logout(self):
        self.open_user_menu()
        self.logout_button.click()

    def go_to_boards(self):
        self.boards_link.click()

    def go_to_tasks(self):
        self.tasks_link.click()
