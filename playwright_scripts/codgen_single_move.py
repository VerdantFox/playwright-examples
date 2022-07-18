from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://verdantfox.com/games/connect-4
    page.goto("https://verdantfox.com/games/connect-4")

    # Click #circle-3-5
    page.locator("#circle-3-5").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
