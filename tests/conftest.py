"""Shared fixtures for the Daily Spend acceptance tests.

Run from the project folder:  python3 -m pytest tests -q
The folder's parent is served with `python3 -m http.server` on a free port, so the site is
opened from a subpath (http://127.0.0.1:PORT/<folder>/), the way GitHub Pages serves it.
"""
import datetime
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

import pytest
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVE = os.path.dirname(ROOT)          # the site is served from a subpath, like GitHub Pages
SUB = "/" + os.path.basename(ROOT)
CHROME = "/usr/bin/google-chrome"
KEY = "dailyspend.state"
LEGACY_KEY = "dailyspend.v1"
# Fixed clock so day labels and month maths are deterministic.
NOW = datetime.datetime(2026, 11, 15, 12, 0, 0)
TZ = "America/Edmonton"
IPHONE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def base_url():
    port = free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=SERVE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            urllib.request.urlopen(url + SUB + "/index.html", timeout=1).close()
            break
        except Exception:
            time.sleep(0.1)
    yield url + SUB
    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, headless=True)
        yield b
        b.close()


# Maple Bank has credit, debit and prepaid cards; American Express has credit cards only;
# The Northern Trust has one debit card (and sorts under N); one card has an unknown kind.
FIXTURE_CARDS = {
    "version": "test", "lastChecked": "2026-11-15",
    "issuers": [{"id": "maple", "name": "Maple Bank"}, {"id": "prairie", "name": "Prairie Credit Union"},
                {"id": "amex", "name": "American Express"}, {"id": "northern", "name": "The Northern Trust"}],
    "cards": [
        {"id": "maple-rewards-visa", "issuerId": "maple", "name": "Maple Rewards Visa", "kind": "credit", "networks": ["Visa"], "extra": 1},
        {"id": "maple-travel-mc", "issuerId": "maple", "name": "Maple Travel World Mastercard", "kind": "credit", "networks": ["Mastercard"]},
        {"id": "maple-everyday-debit", "issuerId": "maple", "name": "Maple Everyday Debit", "kind": "debit", "networks": ["Interac", "Visa Debit"]},
        {"id": "maple-prepaid", "issuerId": "maple", "name": "Maple Travel Prepaid", "kind": "prepaid", "networks": ["Visa"]},
        {"id": "prairie-cash-mc", "issuerId": "prairie", "name": "Prairie Cash Back Mastercard", "kind": "credit", "networks": ["Mastercard"]},
        {"id": "prairie-prepaid", "issuerId": "prairie", "name": "Prairie Reloadable Prepaid", "kind": "prepaid", "networks": ["Mastercard"]},
        {"id": "amex-cobalt", "issuerId": "amex", "name": "American Express Cobalt Card", "kind": "credit", "networks": ["American Express"]},
        {"id": "amex-green", "issuerId": "amex", "name": "American Express Green Card", "kind": "credit", "networks": ["American Express"]},
        {"id": "northern-client", "issuerId": "northern", "name": "Northern Client Card", "kind": "debit", "networks": ["Interac"]},
        {"id": "bad-kind", "issuerId": "amex", "name": "Ignored card", "kind": "charge", "networks": ["Visa"]},
    ],
}


class App:
    """A mobile-emulated page plus the things the tests watch.

    Service workers are blocked unless a test asks for them, so each test starts from the
    network and route interception can serve the fixture card list.
    """

    def __init__(self, browser, base_url, width=390, height=844, scheme="light",
                 init_scripts=(), now=NOW, path="/", open_page=True,
                 reduced_motion="no-preference", service_workers="block", cards="fixture",
                 skip_welcome=True, geolocation=None, fixed_clock=True):
        self.base_url = base_url
        self.skip_welcome = skip_welcome
        opts = dict(
            viewport={"width": width, "height": height}, device_scale_factor=2,
            is_mobile=True, has_touch=True, user_agent=IPHONE_UA, service_workers=service_workers,
            color_scheme=scheme, reduced_motion=reduced_motion, locale="en-CA", timezone_id=TZ, accept_downloads=True)
        if geolocation:
            opts["geolocation"] = geolocation
            opts["permissions"] = ["geolocation"]
        self.context = browser.new_context(**opts)
        for script in init_scripts:
            self.context.add_init_script(script)
        self.context.set_default_timeout(6000)
        self.card_requests = 0
        if cards is not None:
            def card_route(route):
                self.card_requests += 1
                if cards == "fixture":
                    route.fulfill(status=200, content_type="application/json", body=json.dumps(FIXTURE_CARDS))
                elif cards == "fail":
                    route.fulfill(status=404, content_type="text/plain", body="not found")
                else:
                    route.continue_()
            self.context.route("**/data/cards-ca.json", card_route)
        self.page = self.context.new_page()
        if fixed_clock:
            self.page.clock.set_fixed_time(now)
        self.console_errors, self.requests, self.dialogs = [], [], []
        self.page.on("console", lambda m: self.console_errors.append(m.text) if m.type == "error" else None)
        self.page.on("pageerror", lambda e: self.console_errors.append(str(e)))
        self.context.on("request", lambda r: self.requests.append(r.url))
        self.page.on("dialog", lambda d: (self.dialogs.append(d.message), d.dismiss()))
        self.ui = self.page  # Page or FrameLocator that holds the app
        if open_page:
            self.goto(path)

    def goto(self, path="/"):
        self.page.goto(self.base_url + path)
        self.ready()

    def ready(self):
        """Wait for the app; dismiss the first-run welcome unless the test wants it."""
        self.ui.locator("#amount").wait_for()
        if self.skip_welcome and self.ui.locator("#ob-skip").count():
            self.ui.locator("#ob-skip").click()

    def reload(self):
        self.page.reload()
        self.ready()

    # ----- actions -----
    def tab(self, name):
        self.ui.locator(f'.tab[data-tab="{name}"]').click()

    def type_amount(self, text):
        for ch in text:
            self.ui.locator(f'[data-key="{ch}"]').click()

    def amount(self):
        return self.ui.locator("#amount").inner_text()

    def chip(self, name):
        return self.ui.locator(".chip").filter(has=self.ui.locator(f'.chip-name:text-is("{name}")'))

    def add(self, amount, category):
        self.type_amount(amount)
        self.chip(category).click()

    def pick_card(self, issuer, card, kind=None):
        """In the open Add a card sheet: institution, then type (when asked for), then card. Ends on the confirm step."""
        self.ui.locator(f'#ac-list [data-issuer="{issuer}"]').click()
        if kind:
            self.ui.locator(f'#ac-types [data-kind="{kind}"]').click()
        self.ui.locator(f'#ac-cards .row:has-text("{card}")').click()
        self.ui.locator("#cf-save").wait_for()

    def toast(self):
        return self.ui.locator("#toast-region .toast-text")

    def sheet_hidden(self):
        return self.ui.locator("#sheet-root").is_hidden()

    # ----- data -----
    def state(self):
        return self.page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}'))")

    def expenses(self):
        s = self.state()
        return s["expenses"] if s else []

    def cards(self):
        s = self.state()
        return s["cards"] if s else []

    def seed(self, state, key=KEY):
        self.page.evaluate("([k, s]) => localStorage.setItem(k, JSON.stringify(s))", [key, state])
        self.reload()

    def close(self):
        self.context.close()


@pytest.fixture
def make_app(browser, base_url):
    apps = []

    def factory(**kw):
        app = App(browser, base_url, **kw)
        apps.append(app)
        return app

    yield factory
    for a in apps:
        a.close()


@pytest.fixture
def app(make_app):
    return make_app()


def cents(text):
    """'$1,234.56' -> 123456"""
    t = text.strip().replace("$", "").replace(",", "")
    whole, _, frac = t.partition(".")
    return int(whole) * 100 + int((frac + "00")[:2])


DEFAULT_CATS = [
    ("groceries", "🛒", "Groceries", None), ("dining", "☕", "Dining & coffee", None),
    ("gas", "⛽", "Gas & parking", None), ("transit", "🚇", "Transit", None),
    ("shopping", "🛍️", "Shopping", None), ("phone", "📱", "Phone & internet", None),
    ("utilities", "💡", "Hydro & utilities", None), ("housing", "🏠", "Rent or mortgage", None),
    ("condo", "🏢", "Condo fees", None), ("propertytax", "🏛️", "Property tax", None),
    ("car", "🚗", "Car costs", None), ("medical", "🩺", "Medical & dental", "medical"),
    ("childcare", "🧸", "Childcare", "childcare"), ("donations", "🎗️", "Donations", "donation"),
    ("subscriptions", "📺", "Subscriptions", None), ("entertainment", "🎟️", "Entertainment", None),
    ("travel", "✈️", "Travel", None), ("personalcare", "💇", "Personal care", None),
    ("gifts", "🎁", "Gifts", None), ("other", "📦", "Other", None),
]


def make_cats():
    return [{"id": c[0], "emoji": c[1], "name": c[2], "taxTag": c[3], "hidden": False,
             "builtIn": True, "order": i + 1} for i, c in enumerate(DEFAULT_CATS)]


def make_expenses(rows):
    """rows: (date, cents, categoryId, paymentId, merchant, note[, cardId[, location]])"""
    out = []
    for i, r in enumerate(rows):
        stamp = f"{r[0]}T{8 + i % 12:02d}:{i % 60:02d}:00.000Z"
        out.append({"id": f"seed-{i:03d}", "date": r[0], "amountCents": r[1], "categoryId": r[2],
                    "paymentMethodId": r[3], "cardId": r[6] if len(r) > 6 else None,
                    "merchant": r[4], "note": r[5], "location": r[7] if len(r) > 7 else None,
                    "createdAt": stamp, "updatedAt": stamp})
    return out


def make_card(card_id, name, kind="credit", issuer="Maple Bank", networks=("Visa",), nickname="", last4="",
              colour="teal", archived=False, catalogue_id=None):
    return {"id": card_id, "catalogueId": catalogue_id, "issuer": issuer, "name": name, "kind": kind,
            "networks": list(networks), "nickname": nickname, "last4": last4, "colour": colour,
            "archived": archived, "createdAt": "2026-10-01T12:00:00.000Z"}


def make_state(rows, test_notice_dismissed=False, cards=(), onboarded=True, auto_location=False):
    """A schema 2 state, as the app stores it."""
    return {"schemaVersion": 2, "expenses": make_expenses(rows), "categories": make_cats(), "cards": list(cards),
            "settings": {"lastPayment": {"methodId": "credit", "cardId": None},
                         "testNoticeDismissed": test_notice_dismissed, "autoLocation": auto_location,
                         "mapsNoticeShown": False, "onboarded": onboarded}}


def make_v1_state(rows, last_payment="credit"):
    """A schema 1 state, as the v1 test page stored it under dailyspend.v1."""
    expenses = make_expenses(rows)
    for e in expenses:
        del e["cardId"], e["location"]
    return {"schemaVersion": 1, "expenses": expenses, "categories": make_cats(),
            "settings": {"lastPaymentMethodId": last_payment, "testNoticeDismissed": True}}


SAMPLE_ROWS = [
    ("2026-11-15", 8412, "groceries", "credit", "Co-op", "Weekly shop"),
    ("2026-11-15", 475, "dining", "debit", "Tim Hortons", ""),
    ("2026-11-14", 6230, "gas", "credit", "Petro-Canada", ""),
    ("2026-11-14", 3899, "dining", "credit", "Phil & Sebastian", "Brunch"),
    ("2026-11-13", 11200, "transit", "debit", "Calgary Transit", "Monthly pass"),
    ("2026-11-12", 2150, "donations", "credit", "Calgary Food Bank", ""),
    ("2026-11-10", 18500, "medical", "credit", "Dentist", "Cleaning"),
    ("2026-11-09", 9575, "groceries", "debit", "Superstore", ""),
    ("2026-11-07", 6499, "shopping", "credit", "Canadian Tire", "Wiper blades"),
    ("2026-11-05", 8500, "phone", "pad", "Telus", ""),
    ("2026-11-03", 13260, "utilities", "pad", "Enmax", "October bill"),
    ("2026-11-01", 185000, "housing", "etransfer", "", "November rent"),
    ("2026-11-01", 1699, "subscriptions", "credit", "Netflix", ""),
    ("2026-10-28", 7250, "groceries", "credit", "Co-op", ""),
    ("2026-10-20", 5000, "donations", "credit", "United Way", ""),
    ("2026-10-11", 42000, "childcare", "etransfer", "Day home", "October"),
    ("2026-03-02", 9900, "medical", "credit", "Pharmacy", ""),
    ("2025-12-20", 12000, "medical", "credit", "Physio", "Last year"),
]
