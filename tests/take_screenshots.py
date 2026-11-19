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
                # Motion is on (the confetti frame needs it); each shot waits for the motion to end.
                # The estimate uses the site's own tax file (data/tax-ca-2026.json).
                app = App(browser, base, width=390, height=844, scheme=scheme, cards="real", tax="real")
                ui = app.ui

                def shot(name, wait=700):
                    app.page.wait_for_timeout(wait)
                    app.page.screenshot(path=os.path.join(out, f"{name}-{scheme}.png"))

                state = sample_state()
                state["settings"]["pay"] = None
                state["settings"]["paySkipped"] = False
                app.seed(state)
                # Add: empty, a selected chip, ready Save
                shot("add-1-empty")
                app.chip("Groceries").click()
                shot("add-2-selected-chip")
                app.type_amount("23.40")
                shot("add-3-ready-save")
                app.chip("Groceries").click()
                for _ in range(5):
                    ui.locator('[data-key="back"]').click()
                # History, and Summary (Month) with the compare button
                app.tab("history")
                shot("history")
                app.tab("summary")
                shot("summary-month-compare-button", wait=1000)
                # Pay sheet with an estimate and a second earner
                ui.locator("#btn-compare").click()
                shot("pay-sheet-empty")
                ui.locator("#pay-1").fill("85,000")
                ui.locator("#pay-add-earner").click()
                ui.locator("#pay-2").fill("62,500")
                ui.locator("#pay-province").select_option("ON")
                ui.locator("#pay-2").blur()
                shot("pay-sheet-estimate-two-earners")
                app.page.keyboard.press("Escape")
                # the report with one earner, so it has both wins and groups over typical
                state["settings"]["pay"] = {"earners": [6000000], "province": "ON", "takeHomeOverrideCents": None, "taxYear": 2026,
                                            "updatedAt": "2026-11-15T12:00:00.000Z"}
                app.seed(state)
                app.tab("summary")
                ui.locator("#btn-compare").click()
                ui.locator("#report").wait_for()
                # Report: score, a win (a confetti frame), an over with its tip, savings, wrap-up
                shot("report-1-score")
                kinds = ui.locator("#report .rp-card").evaluate_all("(els) => els.map((e) => e.dataset.kind)")
                done = set()
                for i, kind in enumerate(kinds[1:], start=1):
                    ui.locator("#rp-next").click()
                    name = {"win": "report-2-win-confetti", "over": "report-3-over-with-tip", "savings": "report-4-savings",
                            "notlogged": "report-5-not-logged", "wrap": "report-6-wrap-up"}[kind]
                    if kind in done:
                        app.page.wait_for_timeout(500)
                        continue
                    done.add(kind)
                    shot(name, wait=330 if kind == "win" else 1100)
                app.page.keyboard.press("Escape")
                # the same report without pay (spending split)
                split = sample_state()
                split["settings"]["pay"] = None
                split["settings"]["paySkipped"] = True
                saved_pay = app.state()["settings"]["pay"]
                app.seed(split)
                app.tab("summary")
                ui.locator("#btn-compare").click()
                ui.locator("#report").wait_for()
                shot("report-split-score")
                app.page.keyboard.press("Escape")
                # Profile with the Pay row
                split["settings"]["pay"] = saved_pay
                split["settings"]["paySkipped"] = False
                app.seed(split)
                app.tab("profile")
                ui.locator("#pay-summary").wait_for()
                ui.locator("#view").evaluate("(v) => { v.scrollTop = document.getElementById('pay-settings').offsetTop - 120; }")
                shot("profile-pay-row")
                app.close()
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    print("\n".join(sorted(os.listdir(out))))


if __name__ == "__main__":
    main()
