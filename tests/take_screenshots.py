"""Takes the screenshots (390 by 844, light and dark).

Run from the project folder:  python3 tests/take_screenshots.py <output folder>
The output folder is required so screenshots never land in the repository by accident.
"""
import os
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright  # noqa: E402

from conftest import CHROME, SAMPLE_ROWS, SERVE, SUB, App, free_port, make_card, make_state, make_v2_state  # noqa: E402

PIN = {"lat": 51.04471, "lng": -114.07188, "accuracyM": 25, "capturedAt": "2026-11-10T18:00:00.000Z"}
CARDS = [
    make_card("card-a", "American Express Cobalt Card", nickname="Cobalt", last4="1234", issuer="American Express Canada",
              networks=("American Express",), colour="rose", catalogue_id="amex-cobalt"),
    make_card("card-b", "TD Access Card", kind="debit", issuer="TD", networks=("Interac", "Visa Debit"),
              last4="0042", colour="green", catalogue_id="td-access-card"),
    make_card("card-c", "KOHO Prepaid Mastercard", kind="prepaid", issuer="KOHO", networks=("Mastercard",), colour="indigo",
              catalogue_id="koho-prepaid-mastercard"),
    make_card("card-d", "Old store card", issuer="", networks=(), colour="slate", archived=True),
    make_card("card-e", "TD Cash Back Visa Infinite Card", issuer="TD", networks=("Visa",), last4="7788", colour="blue",
              catalogue_id="td-cash-back-visa-infinite"),
]
CARD_FOR = {"credit": "card-a", "debit": "card-b"}


def sample_state():
    rows = []
    for i, r in enumerate(SAMPLE_ROWS):
        card = CARD_FOR.get(r[3])
        if i == 8:
            card = "card-d"
        rows.append(r + (card, PIN if i in (0, 1, 3, 6, 9) else None))
    rows.append(("2026-11-08", 2500, "entertainment", "prepaid", "Cineplex", "", "card-c", None))
    rows.append(("2026-11-13", 475, "dining", "debit", "Tim Hortons", "", "card-b", PIN))
    rows.append(("2026-11-06", 14200, "insurance.health-dental-insurance", "pad", "Sun Life", "", None, None))
    rows.append(("2026-11-04", 9800, "transportation.car-insurance", "pad", "", "", None, None))
    rows.append(("2026-11-11", 5640, "groceries", "credit", "Safeway", "", "card-e", None))
    rows.append(("2026-10-17", 12999, "shopping", "credit", "Best Buy", "", "card-e", None))
    rows += [("2026-09-01", 185000, "housing", "etransfer", "", "Rent"), ("2026-09-12", 21050, "groceries", "debit", "Co-op", "", "card-b"),
             ("2026-08-01", 185000, "housing", "etransfer", "", "Rent"), ("2026-08-20", 64000, "travel", "credit", "WestJet", "", "card-a"),
             ("2026-07-01", 185000, "housing", "etransfer", "", "Rent"), ("2026-06-01", 185000, "housing", "etransfer", "", "Rent"),
             ("2026-06-15", 33000, "car", "credit", "Toyota", "", "card-a"), ("2026-10-01", 185000, "housing", "etransfer", "", "Rent")]
    return make_state(rows, cards=CARDS)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    port = free_port()
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                              cwd=SERVE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}{SUB}"
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(base + "/index.html", timeout=1).close()
                break
            except Exception:
                time.sleep(0.1)
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True)
            for scheme in ("light", "dark"):
                app = App(browser, base, width=390, height=844, scheme=scheme, reduced_motion="reduce",
                          cards="real", skip_welcome=False,
                          geolocation={"latitude": 51.0447, "longitude": -114.0719, "accuracy": 25})
                shot = lambda name: app.page.screenshot(path=os.path.join(out, f"{name}-{scheme}.png"))
                ui = app.ui
                # first-run setup: two steps
                shot("first-run-1")
                ui.locator("#ob-next").click()
                shot("first-run-2-location")
                ui.locator("#ob-skip").click()

                # the one-time notice after the move to budget groups (a version 0.2.1 state)
                app.page.evaluate("s => localStorage.setItem('dailyspend.state', JSON.stringify(s))", make_v2_state(SAMPLE_ROWS))
                app.page.reload()
                ui.locator("#mig-ok").wait_for()
                shot("migration-notice")
                ui.locator("#mig-ok").click()

                app.seed(sample_state())
                # Add: empty (red outlines, grey Save), amount only, ready (green Save), a pick from More
                shot("add")
                shot("add-1-empty")
                app.type_amount("23.40")
                shot("add-2-amount-only")
                app.chip("Groceries").click()
                shot("add-3-ready")
                ui.locator(".chip-more").click()
                shot("add-more-sheet-groups")
                ui.locator('#all-categories [data-pick="insurance.life-insurance"]').scroll_into_view_if_needed()
                ui.locator('#all-categories [data-pick="insurance.life-insurance"]').click()
                shot("add-4-selected-from-more")
                app.chip("Life Insurance").click()
                for _ in range(5):
                    ui.locator('[data-key="back"]').click()
                app.type_amount("4.75")
                ui.locator("#details-row").click()
                ui.locator('#d-pay label:has-text("TD Access")').click()
                ui.locator("#d-merchant").fill("Tim Hortons")
                ui.locator("#d-loc-add").scroll_into_view_if_needed()
                ui.locator("#d-loc-add").click()
                ui.locator("#d-loc-remove").wait_for()
                shot("add-details-sheet")
                ui.locator(".sheet-body").evaluate("(e) => { e.scrollTop = 0; }")
                shot("add-details-sheet-payment")
                ui.locator("#d-done").click()
                shot("add-usual-pill")
                ui.locator("#usual-pill").click()
                app.save()
                shot("add-saved-toast")
                ui.locator(".toast-undo").click()
                app.page.wait_for_timeout(2300)
                ui.locator("#btn-recent").click()
                shot("add-recent-sheet")
                app.page.keyboard.press("Escape")
                # History
                app.tab("history")
                shot("history")
                box = ui.locator('.row[data-id="seed-002"]').bounding_box()
                app.page.mouse.move(box["x"] + 200, box["y"] + 28)
                app.page.mouse.down()
                app.page.mouse.move(box["x"] + 160, box["y"] + 28)
                app.page.mouse.move(box["x"] + 120, box["y"] + 28)
                app.page.mouse.up()
                shot("history-swipe-delete")
                ui.locator("#h-search").click()
                app.page.wait_for_timeout(400)
                ui.locator("#h-search").fill("co")
                ui.locator("#f-category").click()
                ui.locator('#fc-list label:has-text("Groceries")').click()
                shot("history-category-filter-sheet")
                ui.locator("#fc-done").click()
                ui.locator("#f-card").click()
                ui.locator('#fk-list .item-check:has-text("Cobalt")').click()
                ui.locator("#fk-done").click()
                shot("history-filters")
                ui.locator("#f-clear").click()
                ui.locator("#f-card").click()
                ui.locator('#fk-list input[data-inst="td"]').check()
                shot("history-card-or-institution-sheet")
                ui.locator("#fk-done").click()
                shot("history-filtered-by-institution")
                ui.locator("#f-clear").click()
                ui.locator('.row[data-id="seed-000"]').click()
                ui.locator("#e-maps").scroll_into_view_if_needed()
                shot("history-edit-location")
                app.page.keyboard.press("Escape")
                # Summary
                app.tab("summary")
                ui.locator('#range-seg [data-range="3"]').click()
                shot("summary-3-months")
                ui.locator('#range-seg [data-range="12"]').click()
                shot("summary-12-months")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = document.getElementById('by-group').offsetTop - 60; }")
                shot("summary-12-months-by-group")
                ui.locator('#range-seg [data-range="month"]').click()
                shot("summary-charts")
                shot("summary-month-matched-colours")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = document.getElementById('by-group').offsetTop - 300; }")
                shot("summary-month-by-group")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = 0; }")
                ui.locator('#donut .slice[data-group="food"]').dispatch_event("click")
                shot("summary-group-view")
                ui.locator("#group-back").click()
                ui.locator('#by-group .grp-row:has-text("Miscellaneous")').click()
                ui.locator("#by-group").scroll_into_view_if_needed()
                ui.locator("#view").evaluate("(v) => { v.scrollTop = document.getElementById('by-group').offsetTop - 40; }")
                shot("summary-by-group-open")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = v.scrollHeight; }")
                shot("summary-tax-time")
                ui.locator("#by-card").scroll_into_view_if_needed()
                ui.locator("#view").evaluate("(v) => { v.scrollTop = v.scrollHeight; }")
                shot("summary-by-card")
                # Profile and cards
                app.tab("profile")
                app.page.wait_for_timeout(300)
                shot("my-cards")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = document.getElementById('category-list').offsetTop - 60; }")
                shot("profile-categories")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = v.scrollHeight; }")
                shot("profile")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = 0; }")
                # the institution-first card picker (the site's real card list)
                ui.locator("#btn-add-card").click()
                ui.locator("#ac-list .row").first.wait_for()
                shot("picker-1-institutions")
                ui.locator("#ac-search").fill("cash")
                shot("picker-1-search")
                ui.locator("#ac-search").fill("")
                ui.locator('#ac-list [data-issuer="RBC Royal Bank"]').click()
                shot("picker-2-types")
                ui.locator('#ac-types [data-kind="credit"]').click()
                shot("picker-3-cards")
                ui.locator("#ac-cards .row").nth(1).click()
                ui.locator("#cf-nick").fill("Groceries card")
                ui.locator("#cf-last4").fill("7788")
                shot("picker-4-confirm")
                ui.locator("[data-sheet-back]").click()
                ui.locator("#ac-manual-here").click()
                shot("picker-by-hand")
                ui.locator("[data-sheet-close]").click()
                app.close()
            # one Add screen on a small phone (375 by 667)
            small = App(browser, base, width=375, height=667, reduced_motion="reduce", cards="real")
            small.seed(sample_state())
            small.type_amount("23.40")
            small.chip("Groceries").click()
            small.page.screenshot(path=os.path.join(out, "add-375x667-light.png"))
            small.close()
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    print("\n".join(sorted(os.listdir(out))))


if __name__ == "__main__":
    main()
