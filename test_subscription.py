import re

import pytest
from playwright.sync_api import Page, expect

SUBSCRIPTION_URL = "http://localhost:3000/automation-lab/subscription"


def test_open_form(page: Page):
    page.goto(SUBSCRIPTION_URL)

    expect(page).to_have_url(SUBSCRIPTION_URL)
    expect(page).to_have_title("Task Management Board")
    expect(page.get_by_text("Подключение подписки StreamVibe")).to_be_visible()
    expect(page.locator('[data-testid="period-section"]')).to_be_visible()
    expect(page.locator('[data-testid="tariffs-section"]')).to_be_visible()
    expect(page.locator(".promo-section")).to_be_visible()
    expect(page.locator(".payment-card-visual")).to_be_visible()
    expect(page.get_by_test_id("summary-section")).to_be_visible()
    expect(page.get_by_role("textbox", name="Введите промокод")).to_be_visible()
    expect(page.get_by_placeholder("0000 0000 0000 0000")).to_be_visible()
    expect(page.get_by_test_id("pay-button")).to_be_visible()


def test_promo_always_ok(page: Page):
    page.goto(SUBSCRIPTION_URL)

    page.get_by_test_id("promo-input").fill("ALWAYS")
    page.get_by_role("button", name="Применить").click()

    promo_message = page.get_by_test_id("promo-message")
    expect(promo_message).to_be_visible()
    expect(promo_message).to_have_class(re.compile(r"success"))
    expect(promo_message).to_contain_text("Промокод применён")


def test_promo_basic199_ok(page: Page):
    page.goto(SUBSCRIPTION_URL)

    page.locator('[data-tariff="basic"]').click()
    page.get_by_test_id("promo-input").type("BASIC199")
    page.get_by_test_id("promo-apply-btn").click()

    promo_message = page.get_by_test_id("promo-message")
    expect(promo_message).to_be_visible()
    expect(promo_message).to_contain_text("Промокод применён")


@pytest.mark.parametrize(
    "code, text",
    [
        ("WELCOME10", "истек"),
        ("BASIC199", "только для"),
    ],
)
def test_promo_bad(page: Page, code, text):
    page.goto(SUBSCRIPTION_URL)

    page.get_by_test_id("promo-input").fill(code)
    page.get_by_test_id("promo-apply-btn").click()

    promo_message = page.locator('[data-testid="promo-message"]')
    expect(promo_message).to_be_visible()
    expect(promo_message).to_have_class(re.compile(r"error"))
    expect(promo_message).to_contain_text(text)


def test_card_visa_ok(page: Page):
    page.goto(SUBSCRIPTION_URL)

    page.get_by_test_id("card-number").fill("4111111111111111")
    page.get_by_test_id("card-expiry").fill("12/29")
    page.get_by_test_id("card-cvv").fill("123")
    page.get_by_test_id("pay-button").click()

    expect(page.locator('[data-testid="success-modal"]')).to_be_visible()
    expect(page.get_by_text("Успешно!")).to_be_visible()


def test_card_master_ok(page: Page):
    page.goto(SUBSCRIPTION_URL)

    page.locator('[data-testid="card-number"]').fill("5555555555554444")
    page.locator('[data-testid="card-expiry"]').fill("12/29")
    page.locator('[data-testid="card-cvv"]').fill("123")
    page.get_by_role("button", name=re.compile(r"Подключить за")).click()

    expect(page.get_by_test_id("success-modal")).to_be_visible()


def test_card_amex_ok(page: Page):
    page.goto(SUBSCRIPTION_URL)

    page.get_by_test_id("card-number").fill("378282246310005")
    page.get_by_test_id("card-expiry").fill("12/29")
    page.get_by_test_id("card-cvv").fill("1234")
    page.get_by_test_id("pay-button").click()

    expect(page.get_by_test_id("success-modal")).to_contain_text("Успешно!")


def test_card_fail(page: Page):
    page.goto(SUBSCRIPTION_URL)

    page.get_by_test_id("card-number").fill("4000000000000002")
    page.get_by_test_id("card-expiry").fill("12/29")
    page.get_by_test_id("card-cvv").fill("123")
    page.get_by_test_id("pay-button").click()

    expect(page.locator('[data-testid="card-errors"]')).to_be_visible()
    expect(page.get_by_text("Карта отклонена")).to_be_visible()


def test_card_no_money(page: Page):
    page.goto(SUBSCRIPTION_URL)

    page.get_by_test_id("card-number").fill("4000000000009995")
    page.get_by_test_id("card-expiry").fill("12/29")
    page.get_by_test_id("card-cvv").fill("123")
    page.get_by_test_id("pay-button").click()

    expect(page.get_by_test_id("card-errors")).to_contain_text("Недостаточно средств")
