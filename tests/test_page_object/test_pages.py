from playwright.sync_api import expect

from pages.boards_page import BoardsPage
from pages.login_page import LoginPage
from pages.main_page import MainPage


def test_open_login_page(page):
    login = LoginPage(page)
    login.open()
    login.verify_page_opened()


def test_open_main_page(login_page):
    main = MainPage(login_page)
    main.open()
    main.verify_page_opened()


def test_open_boards_page(login_page):
    main = MainPage(login_page)
    main.open()
    main.go_to_boards()

    boards = BoardsPage(login_page)
    boards.verify_page_opened()

    main.go_to_tasks()
    expect(login_page.locator('[data-qa="tasks-page"]')).to_be_visible()
    expect(login_page.locator('[data-qa="tasks-page-title"]')).to_have_text("Все задачи")


def test_login_ok(page):
    login = LoginPage(page)
    login.open()
    login.login("admin@example.com", "admin123")

    main = MainPage(page)
    main.verify_page_opened()


def test_user_name(login_page):
    main = MainPage(login_page)
    main.open()
    main.verify_user_info("admin", "admin@example.com")


def test_logout_ok(login_page):
    main = MainPage(login_page)
    main.open()
    main.logout()

    login = LoginPage(login_page)
    login.verify_page_opened()
