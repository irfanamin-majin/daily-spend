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

from conftest import CHROME, SAMPLE_ROWS, SERVE, SUB, App, free_port, make_card, make_state  # noqa: E402

PIN = {"lat": 51.04471, "lng": -114.07188, "accuracyM": 25, "capturedAt": "2026-11-10T18:00:00.000Z"}
CARDS = [
    make_card("card-a", "American Express Cobalt Card", nickname="Cobalt", last4="1234", issuer="American Express",
              networks=("American Express",), colour="rose", catalogue_id="amex-cobalt"),
    make_card("card-b", "TD Access Card", kind="debit", issuer="TD Canada Trust", networks=("Interac", "Visa Debit"),
              last4="0042", colour="green", catalogue_id="td-access-card"),
    make_card("card-c", "KOHO Prepaid Mastercard", kind="prepaid", issuer="KOHO", networks=("Mastercard",), colour="indigo",
              catalogue_id="koho-prepaid-mastercard"),
    make_card("card-d", "Old store card", issuer="", networks=(), colour="slate", archived=True),
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

                app.seed(sample_state())
                # Add
                shot("add")
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
                ui.locator('#fk-list .row:has-text("Cobalt")').click()
                shot("history-filters")
                ui.locator("#f-clear").click()
                ui.locator('.row[data-id="seed-000"]').click()
                ui.locator("#e-maps").scroll_into_view_if_needed()
                shot("history-edit-location")
                app.page.keyboard.press("Escape")
                # Summary
                app.tab("summary")
                shot("summary-charts")
                ui.locator("#by-card").scroll_into_view_if_needed()
                ui.locator("#view").evaluate("(v) => { v.scrollTop = v.scrollHeight; }")
                shot("summary-by-card")
                # Profile and cards
                app.tab("profile")
                shot("my-cards")
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
                ui.locator("#ac-list [data-issuer]").filter(has=ui.locator('.row-title:text-is("TD")')).click()
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
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    print("\n".join(sorted(os.listdir(out))))


if __name__ == "__main__":
    main()
