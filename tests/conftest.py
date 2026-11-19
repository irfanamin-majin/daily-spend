"""Shared fixtures for the Daily Spend acceptance tests.

Run from the project folder:  python3 -m pytest tests -q
The folder's parent is served with `python3 -m http.server` on a free port, so the site is
opened from a subpath (http://127.0.0.1:PORT/<folder>/), the way GitHub Pages serves it.
"""
import datetime
import json
import os
import re
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
# The Northern Trust has one debit card, sorts under N and has no short name (its badge falls back
# to initials); American Express has the id of a popular institution; one card has an unknown kind.
FIXTURE_CARDS = {
    "version": "test", "lastChecked": "2026-11-15",
    "issuers": [{"id": "maple", "name": "Maple Bank", "short": "Maple"}, {"id": "prairie", "name": "Prairie Credit Union", "short": "PCU"},
                {"id": "amex", "name": "American Express", "short": "Amex"}, {"id": "northern", "name": "The Northern Trust"}],
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


def _plain(**extra):
    """A province with flat settings; the cases below override what they exercise."""
    base = {"name": "", "brackets": [{"upTo": 100000, "rate": 0.10}, {"upTo": None, "rate": 0.15}], "creditRate": 0.10,
            "bpa": {"max": 20000, "min": None, "phaseOutStart": None, "phaseOutEnd": None}, "employmentAmount": None,
            "credits": {"cppBase": True, "ei": True, "qpip": False}, "employmentDeduction": None, "surtax": None,
            "taxReduction": None, "healthPremium": None, "notes": "", "src": []}
    base.update(extra)
    return base


PROVINCE_NAMES = {"AB": "Alberta", "BC": "British Columbia", "MB": "Manitoba", "NB": "New Brunswick",
                  "NL": "Newfoundland and Labrador", "NS": "Nova Scotia", "NT": "Northwest Territories", "NU": "Nunavut",
                  "ON": "Ontario", "PE": "Prince Edward Island", "QC": "Quebec", "SK": "Saskatchewan", "YT": "Yukon"}

# Synthetic tax figures in the real file's schema. Round numbers chosen so the expected values in
# test_v2_4.py can be worked by hand. They are NOT real rates.
FIXTURE_TAX = {
    "year": 2026, "asOf": "2026-11-19", "placeholder": False, "sources": [],
    "federal": {"brackets": [{"upTo": 50000, "rate": 0.10}, {"upTo": 100000, "rate": 0.20}, {"upTo": None, "rate": 0.30}],
                "creditRate": 0.10, "bpa": {"max": 10000, "min": 5000, "phaseOutStart": 100000, "phaseOutEnd": 200000},
                "employmentAmount": 1000, "quebecAbatement": 0.20, "src": []},
    "cpp": {"ympe": 60000, "yampe": 70000, "exemption": 5000, "baseRate": 0.05, "firstAdditionalRate": 0.01, "secondAdditionalRate": 0.04, "src": []},
    "qpp": {"ympe": 60000, "yampe": 70000, "exemption": 5000, "baseRate": 0.06, "firstAdditionalRate": 0.01, "secondAdditionalRate": 0.04, "src": []},
    "ei": {"maxInsurable": 50000, "rate": 0.02, "rateQuebec": 0.01, "src": []},
    "qpip": {"maxInsurable": 80000, "rate": 0.005, "src": []},
    "provinces": {code: _plain(name=name) for code, name in PROVINCE_NAMES.items()},
    "referenceCases": [],
}
FIXTURE_TAX["provinces"].update({
    "YT": _plain(name="Yukon", employmentAmount=1000),
    "ON": _plain(name="Ontario", brackets=[{"upTo": 40000, "rate": 0.05}, {"upTo": 80000, "rate": 0.10}, {"upTo": None, "rate": 0.15}],
                 creditRate=0.05, bpa={"max": 10000, "min": None, "phaseOutStart": None, "phaseOutEnd": None},
                 surtax=[{"over": 3000, "rate": 0.20}, {"over": 5000, "rate": 0.36}], taxReduction={"type": "ON", "basic": 300},
                 healthPremium=[{"over": 20000, "rate": 0.06, "max": 300}, {"over": 36000, "rate": 0.06, "max": 150}]),
    "QC": _plain(name="Quebec", brackets=[{"upTo": 50000, "rate": 0.14}, {"upTo": None, "rate": 0.19}], creditRate=0.14,
                 bpa={"max": 18000, "min": None, "phaseOutStart": None, "phaseOutEnd": None},
                 credits={"cppBase": False, "ei": False, "qpip": False}, employmentDeduction={"max": 1400, "rate": 0.06}),
    "BC": _plain(name="British Columbia", brackets=[{"upTo": 50000, "rate": 0.05}, {"upTo": None, "rate": 0.10}], creditRate=0.05,
                 bpa={"max": 12000, "min": None, "phaseOutStart": None, "phaseOutEnd": None},
                 taxReduction={"type": "linear", "max": 500, "rate": 0.04, "phaseOutStart": 25000}),
    "MB": _plain(name="Manitoba", brackets=[{"upTo": None, "rate": 0.10}], creditRate=0.08,
                 bpa={"max": 15000, "min": 0, "phaseOutStart": 200000, "phaseOutEnd": 400000}),
})


class App:
    """A mobile-emulated page plus the things the tests watch.

    Service workers are blocked unless a test asks for them, so each test starts from the
    network and route interception can serve the fixture card list.
    """

    def __init__(self, browser, base_url, width=390, height=844, scheme="light",
                 init_scripts=(), now=NOW, path="/", open_page=True,
                 reduced_motion="no-preference", service_workers="block", cards="fixture",
                 skip_welcome=True, geolocation=None, fixed_clock=True, tax="fixture"):
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
        # tax: "fixture" serves FIXTURE_TAX, "real" the file in data/, "fail" a 404, None leaves the request alone
        self.tax_requests = 0
        if tax is not None:
            def tax_route(route):
                self.tax_requests += 1
                if tax == "fixture":
                    route.fulfill(status=200, content_type="application/json", body=json.dumps(FIXTURE_TAX))
                elif tax == "fail":
                    route.fulfill(status=404, content_type="text/plain", body="not found")
                else:
                    route.continue_()
            self.context.route("**/data/tax-ca-2026.json", tax_route)
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
        if self.skip_welcome and self.ui.locator("#mig-ok").count():      # the one-time "categories updated" notice
            self.ui.locator("#mig-ok").click()

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

    def save(self):
        """Press Save expense (v2.3: choosing a category only selects it)."""
        self.ui.locator("#btn-save").click()

    def add(self, amount, category):
        """Type the amount, select the category chip, press Save."""
        self.type_amount(amount)
        self.chip(category).click()
        self.save()

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


# The budgeting template behind the typical shares, and its publisher, must never be named in the
# app or the repository, tests included. So the check works from hashes of the name, not the name.
UNNAMED = {"a64bd62526e63dd53e143aaeb2c319dbc1d6e213b2572345a08a26a8a933d35b", "722bdaf552dcb4950e0b17443f3c6ceb8f15d0ffff9d77e8ad8b562646ef3c34"}


def names_the_template(text):
    """True if any word pair (or run-together pair) in the text hashes to the unnamed publisher."""
    import hashlib
    words = re.findall(r"[a-z]+", text.lower())
    grams = set(words) | {a + " " + b for a, b in zip(words, words[1:])}
    return any(hashlib.sha256(g.encode()).hexdigest() in UNNAMED for g in grams)


def cents(text):
    """'$1,234.56' -> 123456"""
    t = text.strip().replace("$", "").replace(",", "")
    whole, _, frac = t.partition(".")
    return int(whole) * 100 + int((frac + "00")[:2])


GROUPS = [("housing", "Housing"), ("debt", "Debt Payments"), ("communications", "Communications"), ("food", "Food"),
          ("transportation", "Transportation"), ("recreation", "Recreation"), ("misc", "Miscellaneous"), ("insurance", "Insurance")]
# (group id, name, emoji, tax tag): the 45 built-in items of version 0.2.2, in order
ITEMS = [
    ("housing", "Mortgage / Rent", "🏠", None), ("housing", "Property Taxes", "🏛️", None), ("housing", "Water & Sewage", "🚰", None),
    ("housing", "Gas & Hydro", "💡", None), ("housing", "Property / Tenant Insurance", "🛡️", None), ("housing", "Home maintenance", "🔧", None),
    ("housing", "Condo fees", "🏢", None), ("housing", "Other housing", "🏠", None),
    ("debt", "Card interest & fees", "💳", None), ("debt", "Line of Credit", "🏦", None), ("debt", "Personal Loan", "🤝", None),
    ("debt", "Student Loan", "🎓", None), ("debt", "Other debt", "💳", None),
    ("communications", "Cell / Telephone", "📱", None), ("communications", "Television", "📺", None),
    ("communications", "Internet", "🌐", None), ("communications", "Subscriptions", "🔁", None),
    ("food", "Groceries", "🛒", None), ("food", "Restaurant / Take-Out", "🍔", None),
    ("transportation", "Car Loan / Lease Payments", "🚗", None), ("transportation", "Car Insurance", "🛡️", None),
    ("transportation", "Gas / Diesel", "⛽", None), ("transportation", "Car maintenance", "🔧", None),
    ("transportation", "Parking", "🅿️", None), ("transportation", "Transit", "🚇", None),
    ("recreation", "Travel / Vacation", "✈️", None), ("recreation", "Concerts / Sport Events", "🎟️", None),
    ("recreation", "Club Memberships", "🏋️", None), ("recreation", "Other Entertainment", "🎮", None),
    ("misc", "Education", "📚", None), ("misc", "Medical", "🩺", "medical"), ("misc", "Clothing", "👕", None), ("misc", "Gifts", "🎁", None),
    ("misc", "Donations", "🎗️", "donation"), ("misc", "Childcare", "🧸", "childcare"), ("misc", "Shopping", "🛍️", None),
    ("misc", "Personal Care", "💇", None), ("misc", "Pets", "🐾", None), ("misc", "Fees", "🧾", None), ("misc", "Other", "📦", None),
    ("insurance", "Life Insurance", "❤️", None), ("insurance", "Disability Insurance", "♿", None),
    ("insurance", "Critical Illness Insurance", "🏥", None), ("insurance", "Health / Dental Insurance", "🦷", "medical"),
    ("insurance", "Other insurance", "🛡️", None),
]


def item_id(group, name):
    return group + "." + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# The 20 categories of versions 0.1 and 0.2: (old id, emoji, old name, tax tag), and where each one went.
OLD_CATS = [
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
CAT = {
    "groceries": "food.groceries", "dining": "food.restaurant-take-out", "gas": "transportation.gas-diesel",
    "transit": "transportation.transit", "shopping": "misc.shopping", "phone": "communications.cell-telephone",
    "utilities": "housing.gas-hydro", "housing": "housing.mortgage-rent", "condo": "housing.condo-fees",
    "propertytax": "housing.property-taxes", "car": "transportation.car-maintenance", "medical": "misc.medical",
    "childcare": "misc.childcare", "donations": "misc.donations", "subscriptions": "communications.subscriptions",
    "entertainment": "recreation.other-entertainment", "travel": "recreation.travel-vacation",
    "personalcare": "misc.personal-care", "gifts": "misc.gifts", "other": "misc.other",
}


def make_cats():
    return [{"id": item_id(c[0], c[1]), "groupId": c[0], "name": c[1], "emoji": c[2], "taxTag": c[3], "hidden": False,
             "builtIn": True, "order": i + 1} for i, c in enumerate(ITEMS)]


def make_old_cats():
    return [{"id": c[0], "emoji": c[1], "name": c[2], "taxTag": c[3], "hidden": False,
             "builtIn": True, "order": i + 1} for i, c in enumerate(OLD_CATS)]


def make_expenses(rows, old_ids=False):
    """rows: (date, cents, categoryId, paymentId, merchant, note[, cardId[, location]])

    Rows may name a category by its short pre-0.2.2 id ("groceries"); it is stored as the new
    item id ("food.groceries") unless old_ids is set.
    """
    out = []
    for i, r in enumerate(rows):
        stamp = f"{r[0]}T{8 + i % 12:02d}:{i % 60:02d}:00.000Z"
        out.append({"id": f"seed-{i:03d}", "date": r[0], "amountCents": r[1], "categoryId": r[2] if old_ids else CAT.get(r[2], r[2]),
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
    """A schema 3 state, as the app stores it."""
    return {"schemaVersion": 3, "expenses": make_expenses(rows), "categories": make_cats(), "cards": list(cards),
            "settings": {"lastPayment": {"methodId": "credit", "cardId": None},
                         "testNoticeDismissed": test_notice_dismissed, "autoLocation": auto_location,
                         "mapsNoticeShown": False, "onboarded": onboarded, "groupsNotice": False,
                         "pay": None, "paySkipped": False}}


def make_v2_state(rows, cards=(), onboarded=True):
    """A schema 2 state, as version 0.2.0 and 0.2.1 stored it: 20 flat categories, old ids."""
    return {"schemaVersion": 2, "expenses": make_expenses(rows, old_ids=True), "categories": make_old_cats(), "cards": list(cards),
            "settings": {"lastPayment": {"methodId": "credit", "cardId": None}, "testNoticeDismissed": False,
                         "autoLocation": False, "mapsNoticeShown": False, "onboarded": onboarded}}


def make_v1_state(rows, last_payment="credit"):
    """A schema 1 state, as the v1 test page stored it under dailyspend.v1."""
    expenses = make_expenses(rows, old_ids=True)
    for e in expenses:
        del e["cardId"], e["location"]
    return {"schemaVersion": 1, "expenses": expenses, "categories": make_old_cats(),
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
