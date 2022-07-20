"""Tests against the webpage https://verdantfox.com/games/connect-4"""
import re
from typing import Callable

from playwright.sync_api import Locator, Page, expect

GAME_PAGE = "https://verdantfox.com/games/connect-4"


def circle_locator(page: Page, col: int, row: int) -> Locator:
    """Return the id of a circle on the game board"""
    return page.locator(f"#circle-{col}-{row}")


def click_circle(page: Page, col: int, row: int) -> None:
    """Click a circle on the game board, then wait 100 ms"""
    circle_locator(page=page, col=col, row=row).click()
    page.wait_for_timeout(timeout=100)


def assert_red_wld(page: Page, wins: int, losses: int, draws: int) -> None:
    """Assert wins losses and draws for win-loss-draw counter"""
    for wld, count in [("wins", wins), ("losses", losses), ("draws", draws)]:
        expect(page.locator(f"#red-{wld}")).to_have_text(str(count))


def test_single_move_no_helpers(page: Page, assert_snapshot: Callable) -> None:
    """Test that a single move by human, followed by AI behaves as expected"""
    page.goto("https://verdantfox.com/games/connect-4")
    page.locator("#circle-3-5").click()
    expect(page.locator("#circle-3-5")).to_have_class(re.compile(r"color-red"))
    expect(page.locator("#circle-3-5")).to_have_css(
        "background-color", "rgb(255, 0, 0)"
    )
    expect(page.locator("#circle-3-4")).to_have_class(re.compile(r"color-blue"))
    expect(page.locator("#circle-3-4")).to_have_css(
        "background-color", "rgb(0, 0, 255)"
    )
    assert_snapshot(page.locator("#board").screenshot())


def test_single_move_with_helpers(page: Page, assert_snapshot: Callable) -> None:
    """Test that a single move by human, followed by AI behaves as expected"""
    page.goto(GAME_PAGE)
    click_circle(page=page, col=3, row=2)
    expect(circle_locator(page=page, col=3, row=5)).to_have_class(
        re.compile(r"color-red")
    )
    expect(circle_locator(page=page, col=3, row=5)).to_have_css(
        "background-color", "rgb(255, 0, 0)"
    )
    expect(circle_locator(page=page, col=3, row=4)).to_have_class(
        re.compile(r"color-blue")
    )
    expect(circle_locator(page=page, col=3, row=4)).to_have_css(
        "background-color", "rgb(0, 0, 255)"
    )
    assert_snapshot(page.locator("#board").screenshot())


def test_full_game(page: Page, assert_snapshot: Callable) -> None:
    """Test that a full game and reset between 2 human players behaves as expected"""
    page.goto(GAME_PAGE)
    # Turn AI for blue off
    page.locator("#blue-settings >> text=Is Computer").click()
    # Turn off move animations
    page.locator('label:has-text("Show move animations")').click()
    # Play out the game in as few moves as possible
    for col, row in [(1, 5), (6, 5), (1, 4), (5, 5), (1, 3), (4, 5), (1, 2)]:
        click_circle(page=page, col=col, row=row)

    # Assert red has 1-0-0 WLD
    assert_red_wld(page=page, wins=1, losses=0, draws=0)
    # Assert one of the winning circles has the winning class for red
    expect(circle_locator(page=page, col=1, row=4)).to_have_class(
        re.compile(r"color-red-win")
    )

    # Take picture of the game board after a win
    # Fails because of changing color
    # assert_snapshot(page.locator("#board").screenshot(), name="bad_winning_board.png")

    # Note threshold. This allows for a pixel color difference between
    # 0 and 1 with 1 being greater difference allowed
    assert_snapshot(
        page.locator("#board").screenshot(), name="winning_board.png", threshold=0.5
    )
    masked_circles = [
        circle_locator(page, col, row) for col, row in [(1, 5), (1, 4), (1, 3), (1, 2)]
    ]
    # This passes by "masking" the color-changing circles
    # "masked" elements are covered by a pink foreground color
    assert_snapshot(
        page.locator("#board").screenshot(mask=masked_circles),
        name="winning-masked-circles.png",
    )

    # Click "Reset board" button
    page.locator('button:has-text("Reset Board")').click()
    page.wait_for_timeout(timeout=100)
    # WLD counter remains unchanged
    assert_red_wld(page=page, wins=1, losses=0, draws=0)
    # Assert one of the winning circles no longer has winning class or red
    expect(circle_locator(page=page, col=1, row=4)).not_to_have_class(
        re.compile(r"color-red-win")
    )
    expect(circle_locator(page=page, col=1, row=4)).not_to_have_class(
        re.compile(r"color-red")
    )
    assert_snapshot(page.locator("#board").screenshot(), name="post_reset.png")
    # Click "Reset Score" button
    page.locator('button:has-text("Reset Score")').click()
    page.wait_for_timeout(timeout=100)
    # WLD counter is reset to 0-0-0
    assert_red_wld(page=page, wins=0, losses=0, draws=0)
