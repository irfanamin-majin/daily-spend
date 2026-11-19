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
                # Motion is on; each shot waits for it to end. The site's own card list and tax file are used.
                app = App(browser, base, width=390, height=844, scheme=scheme, cards="real", tax="real")
                ui = app.ui

                def shot(name, wait=600):
                    app.page.wait_for_timeout(wait)
                    app.page.screenshot(path=os.path.join(out, f"{name}-{scheme}.png"))

                state = sample_state()
                for cat in state["categories"]:
                    if cat["id"] == "transportation.parking":
                        cat["hidden"] = True
                app.seed(state)
                # Add, with the most recently logged categories first
                shot("add-recent-chips")
                # More: sections, a section, search results, no matches
                app.type_amount("23.40")
                app.chip("Groceries").click()
                ui.locator(".chip-more").click()
                shot("more-1-sections")
                ui.locator('#cp-tiles [data-section="food"]').click()
                shot("more-2-section-food")
                ui.locator("[data-sheet-back]").click()
                ui.locator('#cp-tiles [data-section="misc"]').click()
                shot("more-2-section-miscellaneous")
                ui.locator("[data-sheet-back]").click()
                ui.locator("#cp-search").fill("insur")
                shot("more-3-search-results")
                ui.locator("#cp-search").fill("xyz")
                shot("more-4-no-matches")
                app.close_sheet()
                app.chip("Groceries").click()
                for _ in range(5):
                    ui.locator('[data-key="back"]').click()
                # Profile with Modify categories
                app.tab("profile")
                ui.locator("#view").evaluate("(v) => { v.scrollTop = document.getElementById('category-settings').offsetTop - 260; }")
                shot("profile-modify-categories")
                # Manager: sections, a section with a hidden item, the edit sheet opened from it, search
                ui.locator("#btn-modify-categories").click()
                shot("manager-1-sections")
                ui.locator('#cp-tiles [data-section="transportation"]').click()
                shot("manager-2-section-with-hidden")
                ui.locator('#cm-list .row:has-text("Parking")').click()
                shot("manager-3-edit-sheet")
                ui.locator("[data-sheet-back]").click()
                ui.locator("[data-sheet-back]").click()
                ui.locator("#cp-search").fill("park")
                shot("manager-4-search-with-hidden")
                app.close_sheet()
                app.close()
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    print("\n".join(sorted(os.listdir(out))))


if __name__ == "__main__":
    main()
