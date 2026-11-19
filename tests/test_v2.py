"""Acceptance tests from the v2 brief, section 8 (test numbers match the brief).

Most tests block the service worker and serve a small fixture card list by route interception.
Tests 1 to 3 run with the real service worker and the site's own files.
"""
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time
import urllib.request

import pytest

from conftest import (App, CAT, FIXTURE_CARDS, LEGACY_KEY, ROOT, SAMPLE_ROWS, cents, free_port, make_card, make_state,
                      make_v1_state)
from test_v1 import ADD_FITS, CAPTURE_CLIPBOARD, HEADER, COL, LAYOUT_CHECK, SIZES, copied_csv, parse_csv, source

PRIVACY = ("Your entries stay on this device. No account, no tracking. Nothing is sent anywhere, "
           "except that opening a location in Google Maps shares that location with Google.")
DENIED = "Location is off for Daily Spend. You can allow it in your phone's settings."
FAILED = "Couldn't get your location. Try again in a moment."
CALGARY = {"latitude": 51.0447123, "longitude": -114.0718832, "accuracy": 25}
PIN = {"lat": 51.04471, "lng": -114.07188, "accuracyM": 25, "capturedAt": "2026-11-10T18:00:00.000Z"}
MAPS = "https://www.google.com/maps/search/?api=1&query=51.04471,-114.07188"
CACHE = "ds-0.2.2"
# A location service the test controls: each request waits until the test answers it.
STUB_GEO = """
  window.__geo = [];
  Object.defineProperty(navigator, 'geolocation', { configurable: true, value: {
    getCurrentPosition: (ok, err, opts) => { window.__geo.push({ ok, err, opts }); } } });
"""
CSP_WATCH = "window.__csp = []; document.addEventListener('securitypolicyviolation', (e) => window.__csp.push(e.blockedURI + ' ' + e.violatedDirective));"


def wait_cached(page, cache=CACHE, files=10):
    """Wait until the service worker controls the page and has stored the app's files."""
    page.evaluate("""async ([name, n]) => {
      await navigator.serviceWorker.ready;
      for (let i = 0; i < 100; i++) {
        const keys = await caches.keys();
        if (keys.includes(name) && (await (await caches.open(name)).keys()).length >= n && navigator.serviceWorker.controller) return;
        await new Promise((r) => setTimeout(r, 50));
      }
      throw new Error('service worker cache not ready: ' + JSON.stringify(await caches.keys()));
    }""", [cache, files])


def wait_until(check, timeout=5.0):
    """Poll from Python (the page's policy forbids evaluating strings, so no wait_for_function)."""
    end = time.time() + timeout
    while time.time() < end:
        if check():
            return
        time.sleep(0.05)
    assert check()


def tap_inside(app, locator):
    """Click a point that really belongs to an SVG shape (a slice's box centre can be the hole)."""
    point = locator.evaluate("""(el) => {
      const b = el.getBoundingClientRect();
      for (let i = 1; i < 12; i++) for (let j = 1; j < 12; j++) {
        const x = b.left + b.width * i / 12, y = b.top + b.height * j / 12;
        if (document.elementFromPoint(x, y) === el) return [x, y];
      }
      return null;
    }""")
    assert point, "no visible point"
    app.page.mouse.click(point[0], point[1])


def drag(app, locator, dx, dy=0, steps=8, hold=False):
    box = locator.bounding_box()
    x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    app.page.mouse.move(x, y)
    app.page.mouse.down()
    for i in range(1, steps + 1):
        app.page.mouse.move(x + dx * i / steps, y + dy * i / steps)
    if not hold:
        app.page.mouse.up()


def restore(app, text):
    app.tab("profile")
    app.ui.locator("#btn-restore").click()
    app.ui.locator("#r-text").fill(text)
    app.ui.locator("#r-go").click()
    result = app.ui.locator("#r-result").inner_text()
    app.page.keyboard.press("Escape")
    return result


def pick_payment(app, label):
    app.tab("add")
    app.ui.locator("#details-row").click()
    app.ui.locator(f'#d-pay label:has-text("{label}")').click()
    app.ui.locator("#d-done").click()


# ---------------------------------------------------------------- 1
def test_01_subpath_same_origin_only(make_app):
    app = make_app(service_workers="allow", cards=None, init_scripts=[CSP_WATCH], skip_welcome=False)
    assert re.search(r"^http://127\.0\.0\.1:\d+/[^/]+/$", app.page.url)       # served from a subpath
    wait_cached(app.page)
    # walk through the app, including the card list and a save
    assert app.ui.locator("#ob-privacy").inner_text() == PRIVACY
    app.ui.locator("#ob-skip").click()
    app.add("12.34", "Groceries")
    for tab in ["history", "summary", "profile"]:
        app.tab(tab)
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()
    app.page.wait_for_timeout(300)
    prefix = app.base_url + "/"
    outside = [u for u in app.requests if not u.startswith(prefix) and not u.startswith("data:")]
    assert outside == [], outside
    loaded = {u[len(prefix):] for u in app.requests if u.startswith(prefix)}
    assert {"", "styles.css", "app.js", "sw.js", "data/cards-ca.json"} <= loaded, loaded
    assert not any(u.startswith("tests") for u in loaded)
    assert app.page.evaluate("window.__csp") == []
    assert app.console_errors == [] and app.dialogs == []
    # the policy itself, and nothing inline
    csp = app.page.locator('meta[http-equiv="Content-Security-Policy"]').get_attribute("content")
    assert csp == ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; "
                   "connect-src 'self'; manifest-src 'self'; worker-src 'self'; base-uri 'none'; form-action 'none'")
    assert app.page.locator("script:not([src])").count() == 0
    # the policy really blocks: a request to another origin fails and is reported
    blocked = app.page.evaluate("fetch('https://example.invalid/x').then(() => 'sent', () => 'blocked')")
    assert blocked == "blocked" and len(app.page.evaluate("window.__csp")) == 1
    assert not any("example.invalid" in u for u in app.requests)


# ---------------------------------------------------------------- 2
def test_02_works_offline_after_one_visit(make_app):
    app = make_app(service_workers="allow", cards=None)
    wait_cached(app.page)
    app.add("4.50", "Transit")
    app.context.set_offline(True)
    app.reload()
    assert app.page.evaluate("navigator.onLine") is False
    assert app.amount() == "$0" and app.ui.locator("#chips .chip").count() == 8
    app.add("12.34", "Groceries")
    assert app.toast().inner_text() == "Saved $12.34 · Groceries"
    assert sorted(e["amountCents"] for e in app.expenses()) == [450, 1234]
    app.tab("history")
    assert app.ui.locator("#month-total").inner_text() == "$16.84"
    app.tab("summary")
    assert app.ui.locator("#donut .slice").count() == 2
    # the card list is available offline too
    app.tab("profile")
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()
    app.ui.locator("#ac-search").fill("cobalt")
    found = app.ui.locator("#ac-list [data-cat-id] .row-title").all_inner_texts()
    assert found and all("Cobalt" in name for name in found)
    app.page.keyboard.press("Escape")
    # a second offline reload still opens, with the data
    app.reload()
    assert len(app.expenses()) == 2
    assert app.console_errors == []
    app.context.set_offline(False)


# ---------------------------------------------------------------- 3
def test_03_update_ready_banner(browser, tmp_path):
    # A private copy of the site, so the test can publish a "new version" of the worker.
    site = tmp_path / "daily-spend"
    shutil.copytree(ROOT, site, ignore=shutil.ignore_patterns("tests", "tools", "__pycache__", ".pytest_cache", "_build"))
    port = free_port()
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                              cwd=tmp_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}/daily-spend"
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(base + "/index.html", timeout=1).close()
                break
            except Exception:
                time.sleep(0.1)
        app = App(browser, base, service_workers="allow", cards=None, fixed_clock=False)
        try:
            wait_cached(app.page)
            assert app.ui.locator("#banner-update").count() == 0
            app.add("9", "Groceries")
            # publish the next version
            sw = (site / "sw.js").read_text()
            assert "const VERSION = '0.2.2';" in sw
            (site / "sw.js").write_text(sw.replace("const VERSION = '0.2.2';", "const VERSION = '0.2.3';"))
            app.reload()                                       # the browser checks for a new worker on navigation
            banner = app.ui.locator("#banner-update")
            banner.wait_for()
            assert "Update ready" in banner.inner_text() and banner.locator("button").inner_text() == "Reload"
            # until Reload is pressed the old version keeps serving and both caches exist
            assert sorted(app.page.evaluate("caches.keys()")) == ["ds-0.2.2", "ds-0.2.3"]
            with app.page.expect_navigation():
                banner.locator("button").click()
            app.ready()
            wait_cached(app.page, cache="ds-0.2.3")
            wait_until(lambda: len(app.page.evaluate("caches.keys()")) == 1)
            assert app.page.evaluate("caches.keys()") == ["ds-0.2.3"]                 # old cache deleted on activate
            assert app.ui.locator("#banner-update").count() == 0
            assert len(app.expenses()) == 1                                            # data untouched
            assert app.console_errors == []
        finally:
            app.close()
    finally:
        server.terminate()
        server.wait(timeout=5)


# ---------------------------------------------------------------- 4
def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", path
    return struct.unpack(">II", head[16:24])


def test_04_manifest_and_icons():
    manifest = json.loads(source("manifest.webmanifest"))
    assert manifest["name"] == "Daily Spend" and manifest["display"] == "standalone"
    assert manifest["start_url"] == "./" and manifest["scope"] == "./"
    assert re.match(r"^#[0-9A-Fa-f]{6}$", manifest["theme_color"]) and re.match(r"^#[0-9A-Fa-f]{6}$", manifest["background_color"])
    icons = manifest["icons"]
    assert any(i.get("purpose") == "maskable" for i in icons)
    assert {i["sizes"] for i in icons} >= {"192x192", "512x512"}
    for icon in icons:
        assert not re.match(r"([a-z]+:|/)", icon["src"])                          # relative, for the subpath
        w, h = png_size(os.path.join(ROOT, icon["src"]))
        assert f"{w}x{h}" == icon["sizes"] and icon["type"] == "image/png"
    assert png_size(os.path.join(ROOT, "icons", "apple-touch-icon.png")) == (180, 180)
    html = source("index.html")
    assert '<link rel="manifest" href="manifest.webmanifest">' in html
    assert '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">' in html
    assert 'name="apple-mobile-web-app-capable" content="yes"' in html and 'name="apple-mobile-web-app-title" content="Daily Spend"' in html
    assert html.count('name="theme-color"') == 2                                   # light and dark
    # the worker's file list: every file exists, and the versions agree
    sw = source("sw.js")
    assets = re.findall(r"'([^']+)'", sw[sw.index("const ASSETS"):sw.index("];", sw.index("const ASSETS"))])
    assert len(assets) == 10 and "data/cards-ca.json" in assets
    for a in assets:
        assert os.path.isfile(os.path.join(ROOT, "index.html" if a == "./" else a)), a
    assert all(os.path.join("icons", os.path.basename(i["src"])) in [a.replace("/", os.sep) for a in assets] for i in icons)
    assert "const VERSION = '0.2.2';" in sw and "version: '0.2.2'," in source("app.js")
    assert os.path.isfile(os.path.join(ROOT, ".nojekyll")) and os.path.isfile(os.path.join(ROOT, "README.md"))
    cards = json.loads(source("data/cards-ca.json"))
    assert {"version", "lastChecked", "issuers", "cards"} <= set(cards)


# ---------------------------------------------------------------- 5
def test_05a_manual_location_and_maps_link(make_app):
    app = make_app(geolocation=CALGARY)
    app.context.route("https://www.google.com/**", lambda r: r.fulfill(status=200, content_type="text/html", body="<p>maps stub</p>"))
    app.type_amount("12")
    row = app.ui.locator("#details-row")
    assert "📍" not in row.inner_text()
    row.click()
    assert app.ui.locator("#d-loc-add").inner_text() == "📍 Add current location"
    app.ui.locator("#d-loc-add").click()
    status = app.ui.locator("#d-loc-status")
    status.filter(has_text="Location added").wait_for()
    assert status.inner_text() == "📍 Location added (±25 m)"
    # Remove, then add again
    app.ui.locator("#d-loc-remove").click()
    assert app.ui.locator("#d-loc-add").is_visible() and "📍" not in row.inner_text()
    app.ui.locator("#d-loc-add").click()
    status.filter(has_text="Location added").wait_for()
    app.ui.locator("#d-done").click()
    assert "Today · Credit card · 📍" in row.inner_text()
    app.chip("Groceries").click()
    e = app.expenses()[0]
    assert e["location"]["lat"] == 51.04471 and e["location"]["lng"] == -114.07188 and e["location"]["accuracyM"] == 25
    assert set(e["location"]) == {"lat", "lng", "accuracyM", "capturedAt"} and e["location"]["capturedAt"].endswith("Z")
    assert "📍" not in row.inner_text()                                            # the next entry starts clean
    app.add("3", "Transit")
    assert [x for x in app.expenses() if x["amountCents"] == 300][0]["location"] is None

    # History marks it; the Edit sheet links to Google Maps
    app.tab("history")
    assert app.ui.locator(".row-pin").count() == 1
    assert app.ui.locator('.row[data-act="edit"]:has-text("Groceries") .row-pin').count() == 1
    app.ui.locator('.row[data-act="edit"]:has-text("Groceries")').click()
    assert app.ui.locator("#e-loc-status").inner_text() == "📍 Location (±25 m)"
    link = app.ui.locator("#e-maps")
    assert link.inner_text() == "Open in Google Maps"
    assert link.get_attribute("href") == MAPS
    assert link.get_attribute("target") == "_blank" and link.get_attribute("rel") == "noopener noreferrer"
    assert app.ui.locator("#e-loc-remove").inner_text() == "Remove"
    # first tap: a one-time notice instead of opening anything
    link.click()
    notice = app.ui.locator("#e-maps-notice")
    assert notice.is_visible()
    assert app.ui.locator("#e-maps-notice-text").inner_text() == "This opens Google Maps and shares this location with Google."
    assert len(app.context.pages) == 1 and not any("google" in u for u in app.requests)
    assert app.state()["settings"]["mapsNoticeShown"] is True
    assert app.ui.locator("#e-maps-continue").get_attribute("href") == MAPS
    app.ui.locator("#e-maps-cancel").click()
    assert notice.is_hidden() and len(app.context.pages) == 1
    # from now on the link just opens (a plain link in a new tab)
    with app.context.expect_page() as popup:
        link.click()
    assert popup.value.url == MAPS
    popup.value.close()
    assert notice.is_hidden()
    # Remove in the Edit sheet, saved with Save
    app.ui.locator("#e-loc-remove").click()
    assert app.ui.locator("#e-loc-add").inner_text() == "Add current location"
    assert "where you are now" in app.ui.locator("#e-loc-note").inner_text()
    app.ui.locator("#e-save").click()
    assert all(x["location"] is None for x in app.expenses()) and app.ui.locator(".row-pin").count() == 0
    # ...and add the current location to an existing expense
    app.ui.locator('.row[data-act="edit"]:has-text("Transit")').click()
    app.ui.locator("#e-loc-add").click()
    app.ui.locator("#e-loc-status").filter(has_text="±25 m").wait_for()
    app.ui.locator("#e-save").click()
    assert [x for x in app.expenses() if x["amountCents"] == 300][0]["location"]["lat"] == 51.04471
    assert app.console_errors == [] and app.dialogs == []


def test_05b_continue_opens_maps(make_app):
    app = make_app()
    app.context.route("https://www.google.com/**", lambda r: r.fulfill(status=200, content_type="text/html", body="<p>maps stub</p>"))
    app.seed(make_state([("2026-11-10", 500, "dining", "credit", "Cafe", "", None, PIN)]))
    app.tab("history")
    app.ui.locator('.row[data-act="edit"]').click()
    app.ui.locator("#e-maps").click()
    with app.context.expect_page() as popup:
        app.ui.locator("#e-maps-continue").click()
    assert popup.value.url == MAPS
    assert app.ui.locator("#e-maps-notice").is_hidden() and app.ui.locator("#e-maps").is_visible()


def test_05c_location_denied_and_unavailable(make_app):
    app = make_app()                                         # no permission granted
    app.type_amount("5")
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-loc-add").click()
    err = app.ui.locator("#d-loc-error")
    err.wait_for()
    assert err.inner_text() == DENIED
    assert app.ui.locator("#d-loc-add").is_visible()         # no retry loop: it waits for another tap
    app.ui.locator("#d-done").click()
    app.chip("Groceries").click()
    assert app.expenses()[0]["location"] is None
    # Edit sheet shows the same message
    app.tab("history")
    app.ui.locator('.row[data-act="edit"]').click()
    app.ui.locator("#e-loc-add").click()
    app.ui.locator("#e-loc-error").wait_for()
    assert app.ui.locator("#e-loc-error").inner_text() == DENIED
    app.page.keyboard.press("Escape")
    # the Profile switch turns itself back off when permission is refused
    app.tab("profile")
    app.ui.locator("#set-auto-loc").check()
    app.ui.locator("#auto-loc-error").wait_for()
    assert app.ui.locator("#auto-loc-error").inner_text() == DENIED
    assert not app.ui.locator("#set-auto-loc").is_checked() and app.state()["settings"]["autoLocation"] is False

    # timeout or unavailable
    b = make_app(init_scripts=[STUB_GEO])
    b.type_amount("5")
    b.ui.locator("#details-row").click()
    b.ui.locator("#d-loc-add").click()
    assert b.ui.locator("#d-loc-status").inner_text() == "Finding your location…"
    opts = b.page.evaluate("window.__geo[0].opts")
    assert opts == {"enableHighAccuracy": True, "timeout": 15000, "maximumAge": 60000}
    b.page.evaluate("window.__geo[0].err({ code: 3, message: 'timeout' })")
    assert b.ui.locator("#d-loc-error").inner_text() == FAILED
    # no location service at all
    c = make_app(init_scripts=["Object.defineProperty(navigator, 'geolocation', { configurable: true, value: undefined });"])
    c.ui.locator("#details-row").click()
    c.ui.locator("#d-loc-add").click()
    assert c.ui.locator("#d-loc-error").inner_text() == FAILED
    assert app.console_errors == [] and b.console_errors == [] and c.console_errors == []


def test_05d_automatic_location(make_app):
    # off by default; switching it on in Profile asks for permission
    a = make_app(geolocation=CALGARY)
    assert a.state() is None or a.state()["settings"]["autoLocation"] is False
    a.add("2", "Groceries")
    assert a.expenses()[0]["location"] is None
    a.tab("profile")
    assert not a.ui.locator("#set-auto-loc").is_checked()
    a.ui.locator("#set-auto-loc").check()
    assert a.state()["settings"]["autoLocation"] is True
    a.tab("add")
    a.type_amount("5")                                         # capture starts with the first key
    a.ui.locator('#details-row:has-text("📍")').wait_for()
    wait_until(lambda: "· 📍" in a.ui.locator("#details-row").inner_text() and "📍…" not in a.ui.locator("#details-row").inner_text())
    a.chip("Transit").click()
    assert [e for e in a.expenses() if e["amountCents"] == 500][0]["location"]["accuracyM"] == 25

    # the save never waits: the fix arrives after it and is attached to the saved expense
    app = make_app(init_scripts=[STUB_GEO])
    app.seed(make_state([], auto_location=True))
    assert app.page.evaluate("window.__geo.length") == 0       # nothing is asked before a key is pressed
    app.type_amount("7")
    assert app.page.evaluate("window.__geo.length") == 1
    assert "📍…" in app.ui.locator("#details-row").inner_text()
    app.chip("Groceries").click()
    assert app.toast().inner_text() == "Saved $7.00 · Groceries"
    assert app.expenses()[0]["location"] is None and app.amount() == "$0"
    assert "📍" not in app.ui.locator("#details-row").inner_text()
    app.page.evaluate("window.__geo[0].ok({ coords: { latitude: 53.5461234, longitude: -113.4937012, accuracy: 12.4 } })")
    loc = app.expenses()[0]["location"]
    assert (loc["lat"], loc["lng"], loc["accuracyM"]) == (53.54612, -113.4937, 12)
    assert "📍" not in app.ui.locator("#details-row").inner_text()      # not attached to the next entry

    # more than 30 s after the save, a fix is dropped
    app.type_amount("8")
    app.chip("Transit").click()
    app.page.clock.set_fixed_time("2026-11-15T12:00:31")
    app.page.evaluate("window.__geo[1].ok({ coords: { latitude: 1, longitude: 2, accuracy: 3 } })")
    assert [e for e in app.expenses() if e["amountCents"] == 800][0]["location"] is None
    # undo before the fix arrives: nothing to attach to, no error
    app.type_amount("9")
    app.chip("Transit").click()
    app.ui.locator(".toast-undo").click()
    app.page.evaluate("window.__geo[2].ok({ coords: { latitude: 1, longitude: 2, accuracy: 3 } })")
    assert len(app.expenses()) == 2
    # permission refused: said once, and not asked again in a loop
    app.page.wait_for_timeout(2200)
    app.type_amount("4")
    app.page.evaluate("window.__geo[3].err({ code: 1 })")
    assert app.toast().inner_text() == DENIED
    app.chip("Transit").click()
    app.type_amount("6")
    app.chip("Transit").click()
    assert app.page.evaluate("window.__geo.length") == 4
    assert app.console_errors == []


# ---------------------------------------------------------------- 6
def test_06_cards(app):
    app.tab("profile")
    heads = app.ui.locator("#view .section-head").all_inner_texts()
    assert heads == ["My cards", "Location", "Categories", "Backup", "About"]
    assert app.ui.locator('.tab[data-tab="profile"] span').inner_text() == "Profile"
    assert app.ui.locator("#no-cards").inner_text() == "Add the cards you use to see spending by card."
    assert app.ui.locator("#btn-add-card").inner_text() == "Add a card"

    # the list loads; institution, then card (the full picker is covered in test_v2_1.py)
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()
    assert app.ui.locator("#ac-list [data-issuer]").count() == 4                # the card with an unknown kind is ignored
    app.ui.locator("#ac-search").fill("zzz")
    assert "Nothing matches" in app.ui.locator("#ac-list").inner_text()
    app.ui.locator("#ac-search").fill("cobalt")                                 # search finds a fixture card
    app.ui.locator('#ac-list [data-cat-id]:has-text("Cobalt")').click()
    assert app.ui.locator("#cf-note").inner_text() == "Only the card's name is stored. Never enter your full card number."

    # confirmation: nickname, last 4 (validated), colour
    assert "American Express Cobalt Card" in app.ui.locator("#cf-summary").inner_text()
    assert app.ui.locator("#cf-nick").get_attribute("maxlength") == "24"
    assert app.ui.locator("#cf-colours input").count() == 8
    app.ui.locator("#cf-nick").fill("Cobalt")
    app.ui.locator("#cf-last4").fill("12")
    app.ui.locator("#cf-save").click()
    assert app.ui.locator("#cf-error").inner_text() == "Enter exactly 4 digits, or leave it empty."
    assert app.cards() == []
    app.ui.locator("#cf-last4").fill("1a2b")                                  # digits only, four at most
    assert app.ui.locator("#cf-last4").input_value() == "12"
    assert app.ui.locator("#cf-last4").get_attribute("maxlength") == "4" and app.ui.locator("#cf-last4").get_attribute("inputmode") == "numeric"
    app.ui.locator("#cf-last4").fill("1234")
    app.ui.locator("#cf-nick").fill("4111 1111 1111 1111")                    # a card number is refused
    app.ui.locator("#cf-save").click()
    assert "looks like a card number" in app.ui.locator("#cf-error").inner_text() and app.cards() == []
    app.ui.locator("#cf-nick").fill("Cobalt")
    app.ui.locator('#cf-colours .swatch:has(input[value="rose"])').click()
    app.ui.locator("#cf-save").click()
    assert app.toast().inner_text() == "Added American Express Cobalt Card" and app.sheet_hidden()
    cobalt = app.cards()[0]
    assert {k: cobalt[k] for k in ["catalogueId", "issuer", "name", "kind", "networks", "nickname", "last4", "colour", "archived"]} == {
        "catalogueId": "amex-cobalt", "issuer": "American Express", "name": "American Express Cobalt Card", "kind": "credit",
        "networks": ["American Express"], "nickname": "Cobalt", "last4": "1234", "colour": "rose", "archived": False}
    assert set(cobalt) == {"id", "catalogueId", "issuer", "name", "kind", "networks", "nickname", "last4", "colour", "archived", "createdAt"}
    tile = app.ui.locator("#card-list .card-tile")
    assert tile.locator(".row-title").inner_text() == "Cobalt"
    for part in ["American Express Cobalt Card", "American Express", "Credit", "•••• 1234"]:
        assert part in tile.locator(".row-sub").inner_text()
    assert tile.locator(".card-swatch.sw-rose").count() == 1

    # a second card, no nickname
    app.ui.locator("#btn-add-card").click()
    app.pick_card("Maple Bank", "Maple Everyday Debit", kind="debit")
    app.ui.locator("#cf-save").click()
    debit = [c for c in app.cards() if c["kind"] == "debit"][0]
    assert debit["colour"] != "rose" and debit["nickname"] == "" and debit["last4"] == ""

    # the picker: My cards first, then Other ways with "Other ..." labels
    app.tab("add")
    app.ui.locator("#details-row").click()
    assert app.ui.locator("#d-pay .group-label").all_inner_texts() == ["My cards", "Other ways"]
    labels = [t.strip() for t in app.ui.locator("#d-pay .option").all_inner_texts()]
    assert labels == ["Cobalt ••1234", "Maple Everyday Debit", "Cash", "e-Transfer (Interac)", "Pre-authorised debit",
                      "Other debit card", "Other credit card", "Other prepaid card", "Other"]
    assert app.ui.locator("#d-pay input:checked + span").inner_text().strip() == "Other credit card"
    app.ui.locator('#d-pay label:has-text("Cobalt")').click()
    app.ui.locator("#d-done").click()
    assert "Today · Cobalt ••1234" in app.ui.locator("#details-row").inner_text()
    app.add("20", "Groceries")
    e = app.expenses()[0]
    assert e["cardId"] == cobalt["id"] and e["paymentMethodId"] == "credit"
    assert app.state()["settings"]["lastPayment"] == {"methodId": "credit", "cardId": cobalt["id"]}
    assert "Today · Cobalt ••1234" in app.ui.locator("#details-row").inner_text()        # the choice sticks
    app.add("5", "Transit")
    pick_payment(app, "Maple Everyday Debit")
    app.add("30", "Restaurant / Take-Out")
    assert [x for x in app.expenses() if x["amountCents"] == 3000][0]["paymentMethodId"] == "debit"
    assert [x for x in app.expenses() if x["amountCents"] == 3000][0]["cardId"] == debit["id"]
    pick_payment(app, "Cash")
    app.add("10", "Groceries")
    assert [x for x in app.expenses() if x["amountCents"] == 1000][0]["cardId"] is None
    pick_payment(app, "Cobalt")
    app.reload()                                                                   # the default survives a restart
    assert "Today · Cash" in app.ui.locator("#details-row").inner_text()         # (it sticks on save, not on tap)
    pick_payment(app, "Cobalt")
    app.add("1", "Groceries")
    app.ui.locator("#details-row").click()                                         # most used card first
    assert app.ui.locator("#d-pay .option").first.inner_text().strip() == "Cobalt ••1234"
    app.page.keyboard.press("Escape")

    # History shows the card; Summary has By card with correct totals
    app.tab("history")
    assert app.ui.locator('.row[data-act="edit"]:has-text("Transit") .row-pay').inner_text() == "Cobalt"
    app.ui.locator('.row[data-act="edit"]:has-text("Transit")').click()
    assert app.ui.locator("#e-pay optgroup").evaluate_all("(g) => g.map((x) => x.label)") == ["My cards", "Other ways"]
    assert app.ui.locator("#e-pay option:checked").inner_text() == "Cobalt ••1234"
    app.ui.locator("#e-pay").select_option(label="Cash")                           # a card can be taken off an expense
    app.ui.locator("#e-save").click()
    t = [x for x in app.expenses() if x["amountCents"] == 500][0]
    assert t["cardId"] is None and t["paymentMethodId"] == "cash"
    app.ui.locator('.row[data-act="edit"]:has-text("Transit")').click()
    app.ui.locator("#e-pay").select_option(label="Cobalt ••1234")
    app.ui.locator("#e-save").click()
    t = [x for x in app.expenses() if x["amountCents"] == 500][0]
    assert t["cardId"] == cobalt["id"] and t["paymentMethodId"] == "credit"

    app.tab("summary")
    assert app.ui.locator("#view .section-head").all_inner_texts() == ["By group", "By card"]
    names = app.ui.locator("#by-card .name").all_inner_texts()
    amounts = [cents(x) for x in app.ui.locator("#by-card .amt").all_inner_texts()]
    assert dict(zip(names, amounts)) == {"Maple Everyday Debit": 3000, "Cobalt ••1234": 2600, "Cash & other": 1000}
    assert names[-1] == "Cash & other" and sum(amounts) == cents(app.ui.locator("#summary-total").inner_text()) == 6600
    assert sum(int(p.rstrip("%")) for p in app.ui.locator("#by-card .pct").all_inner_texts()) == 100
    # tapping a card opens History filtered to that card for the month
    app.ui.locator('#by-card .cat-row:has-text("Cobalt")').click()
    assert app.ui.locator('.tab[data-tab="history"]').get_attribute("aria-current") == "page"
    assert app.ui.locator("#f-card").inner_text() == "Cobalt" and app.ui.locator("#f-card").get_attribute("aria-pressed") == "true"
    assert "November 2026" in app.ui.locator("#f-month").inner_text()
    assert app.ui.locator("#results-total").inner_text() == "$26.00"
    assert app.ui.locator('.row[data-act="edit"]').count() == 3
    # the History card filter
    app.ui.locator("#f-clear").click()
    assert app.ui.locator("#month-total").inner_text() == "$66.00"
    app.ui.locator("#f-card").click()
    assert [t.strip().split("\n")[0] for t in app.ui.locator("#fk-list .row").all_inner_texts()] == [
        "All cards and other ways", "Cobalt ••1234", "Maple Everyday Debit", "Cash & other"]
    app.ui.locator('#fk-list .row:has-text("Cash & other")').click()
    assert app.ui.locator("#results-total").inner_text() == "$10.00" and app.ui.locator("#f-card").inner_text() == "Cash & other"
    app.ui.locator("#f-card").click()
    app.ui.locator('#fk-list .row:has-text("Maple Everyday Debit")').click()
    assert app.ui.locator("#results-total").inner_text() == "$30.00"
    app.ui.locator("#f-card").click()
    app.ui.locator('#fk-list .row:has-text("All cards")').click()
    assert app.ui.locator("#f-clear").count() == 0

    # editing a card
    app.tab("profile")
    assert app.ui.locator("#card-list .card-tile .row-title").all_inner_texts() == ["Cobalt", "Maple Everyday Debit"]   # most used first
    app.ui.locator('#card-list .card-tile:has-text("Maple Everyday Debit")').click()
    assert app.ui.locator("#cf-issuer").count() == 0 and app.ui.locator("#cf-name").count() == 0
    app.ui.locator("#cf-nick").fill("Chequing")
    app.ui.locator("#cf-last4").fill("0042")
    app.ui.locator("#cf-save").click()
    assert app.toast().inner_text() == "Card saved"
    assert app.ui.locator("#card-list .card-tile .row-title").all_inner_texts() == ["Cobalt", "Chequing"]

    # removing a used card archives it: hidden from pickers, kept on its expenses
    app.ui.locator('#card-list .card-tile:has-text("Cobalt")').click()
    app.ui.locator("#cf-remove").click()
    assert "stays on the 3 expenses" in app.ui.locator("#cf-confirm-text").inner_text()
    app.ui.locator("#cf-confirm-cancel").click()
    assert not app.cards()[0]["archived"]
    app.ui.locator("#cf-remove").click()
    app.ui.locator("#cf-confirm-remove").click()
    assert app.toast().inner_text() == "Card archived"
    assert [c for c in app.cards() if c["id"] == cobalt["id"]][0]["archived"] is True
    assert sum(1 for x in app.expenses() if x["cardId"] == cobalt["id"]) == 3
    assert "Archived" in app.ui.locator("#view .section-head").all_inner_texts()
    assert "Cobalt" in app.ui.locator("#archived-cards").inner_text()
    assert app.ui.locator("#card-list .card-tile .row-title").all_inner_texts() == ["Chequing"]
    app.tab("add")
    assert "Today · Other credit card" in app.ui.locator("#details-row").inner_text()      # falls back to the card's method
    app.ui.locator("#details-row").click()
    assert "Cobalt" not in app.ui.locator("#d-pay").inner_text()
    app.page.keyboard.press("Escape")
    app.tab("history")
    assert app.ui.locator('.row[data-act="edit"]:has-text("Transit") .row-pay').inner_text() == "Cobalt"
    app.ui.locator('.row[data-act="edit"]:has-text("Transit")').click()
    assert app.ui.locator("#e-pay option:checked").inner_text() == "Cobalt ••1234 (archived)"
    app.page.keyboard.press("Escape")
    app.tab("summary")
    assert "Cobalt ••1234" in app.ui.locator("#by-card .name").all_inner_texts()
    # restore brings it back
    app.tab("profile")
    app.ui.locator('#archived-cards [data-act="card-restore"]').click()
    assert app.ui.locator("#archived-cards").count() == 0
    assert [c for c in app.cards() if c["id"] == cobalt["id"]][0]["archived"] is False
    # removing an unused card deletes it
    app.ui.locator("#btn-add-card").click()
    app.pick_card("Prairie Credit Union", "Prairie Reloadable Prepaid", kind="prepaid")
    app.ui.locator("#cf-save").click()
    assert len(app.cards()) == 3
    app.ui.locator('#card-list .card-tile:has-text("Prairie Reloadable Prepaid")').click()
    app.ui.locator("#cf-remove").click()
    assert app.ui.locator("#cf-confirm-text").inner_text() == "Remove this card?"
    app.ui.locator("#cf-confirm-remove").click()
    assert app.toast().inner_text() == "Card removed" and len(app.cards()) == 2
    # nothing that looks like a card number, expiry or security code is ever stored
    raw = json.dumps(app.state())
    assert not re.search(r"\d{8,}", re.sub(r'"(createdAt|updatedAt|capturedAt|id|cardId)": "[^"]*"', "", raw))
    assert not re.search(r"expir|cvv|cvc|security", raw, re.I)
    assert app.card_requests == 2                                                  # fetched once per visit; this test reloaded once
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 7
def test_07_card_list_fails_add_by_hand(make_app):
    app = make_app(cards="fail")
    app.tab("profile")
    app.ui.locator("#btn-add-card").click()
    status = app.ui.locator("#card-list-status")
    status.filter(has_text="couldn't be loaded").wait_for()
    assert status.inner_text() == "The card list couldn't be loaded. You can still add your card yourself."
    manual = app.ui.locator("#ac-manual")
    assert manual.inner_text() == "My bank or card isn't listed"
    manual.click()
    assert app.ui.locator("#cf-note").inner_text() == "Only the card's name is stored. Never enter your full card number."
    app.ui.locator("#cf-save").click()
    assert app.ui.locator("#cf-error").inner_text() == "Enter the card's name."
    app.ui.locator("#cf-issuer").fill("My Credit Union")
    app.ui.locator("#cf-name").fill("Everyday Debit")
    app.ui.locator('#cf-kinds label:has-text("Debit")').click()
    assert app.ui.locator("#cf-network option").all_inner_texts() == [
        "Not sure", "Visa", "Mastercard", "American Express", "Interac", "Visa Debit", "Debit Mastercard"]
    app.ui.locator("#cf-network").select_option("Interac")
    app.ui.locator("#cf-nick").fill("Joint")
    app.ui.locator("#cf-last4").fill("0042")
    app.ui.locator("#cf-save").click()
    card = app.cards()[0]
    assert {k: card[k] for k in ["catalogueId", "issuer", "name", "kind", "networks", "nickname", "last4"]} == {
        "catalogueId": None, "issuer": "My Credit Union", "name": "Everyday Debit", "kind": "debit",
        "networks": ["Interac"], "nickname": "Joint", "last4": "0042"}
    assert "Joint" in app.ui.locator("#card-list .card-tile").inner_text()
    pick_payment(app, "Joint")
    app.add("8", "Groceries")
    e = app.expenses()[0]
    assert e["cardId"] == card["id"] and e["paymentMethodId"] == "debit"
    # Back from the form returns to the list sheet
    app.tab("profile")
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-manual").click()
    app.ui.locator("#cf-cancel").click()
    assert app.ui.locator("#ac-manual").is_visible()
    assert all("Failed to load resource" in m for m in app.console_errors)        # only the failed download itself
    assert app.dialogs == []


# ---------------------------------------------------------------- 8
def test_08_charts(app):
    app.seed(make_state(SAMPLE_ROWS))
    nov = [r for r in SAMPLE_ROWS if r[0].startswith("2026-11")]
    total = sum(r[1] for r in nov)
    app.tab("summary")
    assert app.ui.locator("#charts").get_attribute("class").split() == ["card", "charts", "draw"]
    assert app.page.evaluate("getComputedStyle(document.getElementById('donut')).animationDuration") == "0.3s"
    assert app.page.evaluate("getComputedStyle(document.querySelector('.dbar')).animationDuration") == "0.3s"
    slices = app.ui.locator("#donut .slice")
    data = slices.evaluate_all("(els) => els.map((e) => [e.getAttribute('aria-label'), Number(e.dataset.cents), e.dataset.group, e.getAttribute('tabindex'), e.getAttribute('role')])")
    # v2.2: one slice per group with spending, highest first
    assert [d[2] for d in data] == ["housing", "misc", "food", "transportation", "communications"]
    assert sum(d[1] for d in data) == total == cents(app.ui.locator("#summary-total").inner_text())
    assert cents(app.ui.locator("#donut-total").text_content()) == total
    for label, c, group, tabindex, role in data:
        assert re.match(r"^.+, \$[\d,]+\.\d\d, \d+%$", label), label
        assert tabindex == "0" and role == "button" and group
    assert data[0][0].startswith("Housing, $1,982.60, ") and data[2][0].startswith("Food, $223.61, ")
    assert sum(int(d[0].rsplit(", ", 1)[1].rstrip("%")) for d in data) == 100
    by_group = dict(zip(app.ui.locator("#by-group .grp-row .name").all_inner_texts(), app.ui.locator("#by-group .grp-row .amt").all_inner_texts()))
    assert len(by_group) == 5 and cents(by_group["Food"]) == 22361              # the list stays as the text equivalent

    # daily bars: one per day with spending, today marked
    bars = app.ui.locator("#daily-bars .daybar")
    days = sorted({r[0] for r in nov})
    bdata = bars.evaluate_all("(els) => els.map((e) => [e.dataset.day, Number(e.dataset.cents), e.getAttribute('aria-label'), e.getAttribute('tabindex'), e.getAttribute('class')])")
    assert [b[0] for b in bdata] == days and sum(b[1] for b in bdata) == total
    for day, c, label, tabindex, cls in bdata:
        assert c == sum(r[1] for r in nov if r[0] == day) and tabindex == "0"
        assert re.match(r"^.+, \$[\d,]+\.\d\d$", label), label
        assert ("today" in cls.split()) == (day == "2026-11-15")
    assert bdata[-1][2] == "Today, $88.87" and "Fri, Nov 13, $112.00" in [b[2] for b in bdata]
    assert app.ui.locator("#today-dot").count() == 1
    assert app.ui.locator("#daily-bars .dbar").count() + app.ui.locator("#daily-bars .bar-empty").count() == 30    # one per day

    # a slice opens that group inside Summary; an item there opens History for the month
    tap_inside(app, app.ui.locator('#donut .slice[data-group="food"]'))
    assert app.ui.locator('.tab[data-tab="summary"]').get_attribute("aria-current") == "page"
    assert app.ui.locator("#group-view").get_attribute("data-group") == "food" and app.ui.locator("#charts").count() == 0
    assert cents(app.ui.locator("#group-total").inner_text()) == 22361
    assert app.ui.locator("#group-items .name").all_inner_texts() == ["Groceries", "Restaurant / Take-Out"]
    app.ui.locator('#group-items .cat-row:has-text("Groceries")').click()
    assert app.ui.locator('.tab[data-tab="history"]').get_attribute("aria-current") == "page"
    assert app.ui.locator("#f-category").inner_text() == "Groceries"
    assert app.ui.locator("#f-month").inner_text() == "November 2026 ×"
    assert app.ui.locator("#month-label").count() == 0
    assert cents(app.ui.locator("#results-total").inner_text()) == 17987
    assert app.ui.locator('.row[data-act="edit"]').count() == 2
    app.ui.locator("#f-month").click()                                              # without the month: October too
    assert cents(app.ui.locator("#results-total").inner_text()) == 17987 + 7250
    assert app.ui.locator(".month-group").count() == 2
    app.ui.locator("#f-clear").click()

    # a bar opens History filtered to that day
    app.tab("summary")
    assert "draw" in app.ui.locator("#charts").get_attribute("class")
    app.ui.locator('#daily-bars .daybar[data-day="2026-11-14"]').click()
    assert app.ui.locator("#f-day").inner_text() == "Yesterday ×"
    assert cents(app.ui.locator("#results-total").inner_text()) == 6230 + 3899
    assert app.ui.locator("section.day").count() == 1 and app.ui.locator('.row[data-act="edit"]').count() == 2
    app.ui.locator("#f-day").click()
    assert app.ui.locator("#month-label").inner_text() == "November 2026"

    # keyboard: slices and bars take focus and answer Enter and Space
    app.tab("summary")
    app.ui.locator('#donut .slice[data-group="transportation"]').focus()
    app.page.keyboard.press("Enter")
    assert app.ui.locator("#group-view").get_attribute("data-group") == "transportation"
    app.ui.locator("#group-back").click()
    app.ui.locator('#daily-bars .daybar[data-day="2026-11-10"]').focus()
    app.page.keyboard.press("Space")
    assert app.ui.locator("#f-day").inner_text() == "Tue, Nov 10 ×"
    # the By group rows do the same job, in place
    app.tab("summary")
    app.ui.locator('#by-group .grp-row:has-text("Miscellaneous")').click()
    app.ui.locator('#by-group .item-row:has-text("Donations")').click()
    assert app.ui.locator("#f-category").inner_text() == "Donations" and cents(app.ui.locator("#results-total").inner_text()) == 2150
    app.ui.locator("#f-clear").click()

    # another month, a month with one group (a full ring), an empty month
    app.tab("summary")
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert "draw" not in app.ui.locator("#charts").get_attribute("class")           # drawn once, on arrival
    assert app.ui.locator("#donut .slice").count() == 2 and app.ui.locator("#today-dot").count() == 0
    for _ in range(7):
        app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert app.ui.locator("#month-label").inner_text() == "March 2026"
    assert app.ui.locator("#donut .slice").count() == 1
    assert app.ui.locator("#donut .slice").get_attribute("aria-label") == "Miscellaneous, $99.00, 100%"
    tap_inside(app, app.ui.locator("#donut .slice"))
    app.ui.locator('#group-items .cat-row:has-text("Medical")').click()
    assert app.ui.locator("#f-month").inner_text() == "March 2026 ×" and cents(app.ui.locator("#results-total").inner_text()) == 9900
    app.ui.locator("#f-clear").click()
    app.tab("summary")
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert app.ui.locator("#charts").count() == 0 and "No expenses in February 2026." in app.ui.locator(".empty").inner_text()
    assert app.console_errors == []


def test_08b_no_chart_animation_with_reduced_motion(make_app):
    app = make_app(reduced_motion="reduce")
    app.seed(make_state(SAMPLE_ROWS))
    app.tab("summary")
    assert app.page.evaluate("getComputedStyle(document.getElementById('donut')).animationName") == "none"
    assert app.page.evaluate("getComputedStyle(document.querySelector('.dbar')).animationName") == "none"
    app.tab("add")
    app.add("1", "Groceries")
    assert app.page.evaluate("getComputedStyle(document.querySelector('.toast-check path')).strokeDashoffset") == "0px"
    assert app.page.evaluate("getComputedStyle(document.querySelector('.toast')).animationName") == "none"


# ---------------------------------------------------------------- 9
def repeat_rows():
    card = make_card("card-a", "Maple Rewards Visa", nickname="Rewards", last4="4321")
    rows = [("2026-11-14", 6230, "gas", "credit", "Petro-Canada", "Fill up", "card-a", PIN),
            ("2026-11-13", 475, "dining", "debit", "Tim Hortons", "", None),
            ("2026-11-12", 475, "dining", "debit", "Tim Hortons", "", None),      # same again: listed once in Recent
            ("2026-11-11", 475, "dining", "debit", "tim hortons", "", "card-a")]  # same but another card: its own entry
    rows += [(f"2026-10-{d:02d}", 1000 + d, "groceries", "cash", f"Shop {d}", "") for d in range(1, 12)]
    return rows, card


def test_09_quick_repeat(make_app):
    rows, card = repeat_rows()
    app = make_app(geolocation=CALGARY)
    app.seed(make_state(rows, cards=[card]))
    n = len(rows)

    def newest():
        return sorted(app.expenses(), key=lambda e: e["createdAt"])[-1] if len(app.expenses()) > n else None

    def check_copy(src_id):
        assert app.toast().count() == 1 and app.ui.locator(".toast-undo").is_visible()
        src = [e for e in app.expenses() if e["id"] == src_id][0]
        new = [e for e in app.expenses() if not e["id"].startswith("seed-")]
        assert len(new) == 1
        new = new[0]
        for f in ["amountCents", "categoryId", "paymentMethodId", "cardId", "merchant", "note"]:
            assert new[f] == src[f], f
        assert new["date"] == "2026-11-15" and new["location"] is None and new["id"] != src["id"]
        app.ui.locator(".toast-undo").click()
        assert len(app.expenses()) == n and all(e["id"].startswith("seed-") for e in app.expenses())

    # 1. the Edit sheet
    app.tab("history")
    app.ui.locator('.row[data-id="seed-000"]').click()
    assert app.ui.locator("#e-again").inner_text() == "Log again today"
    app.ui.locator("#e-again").click()
    assert app.sheet_hidden()
    assert app.toast().inner_text() == "Saved $62.30 · Gas / Diesel"
    check_copy("seed-000")                                                           # the location is not copied

    # 2. a swipe right on a History row
    drag(app, app.ui.locator('.row[data-id="seed-001"]'), 130)
    assert app.toast().inner_text() == "Saved $4.75 · Restaurant / Take-Out"
    assert app.sheet_hidden()
    check_copy("seed-001")

    # 3. the Recent sheet on Add: ten most recent distinct expenses
    app.tab("add")
    assert app.ui.locator("#btn-recent").inner_text().strip() == "Recent"
    app.ui.locator("#btn-recent").click()
    titles = app.ui.locator("#recent-list .recent-row .row-title").all_inner_texts()
    assert len(titles) == 10
    assert titles[:3] == ["$62.30 · Gas / Diesel", "$4.75 · Restaurant / Take-Out", "$4.75 · Restaurant / Take-Out"]
    subs = app.ui.locator("#recent-list .recent-row .row-sub").all_inner_texts()
    assert subs[0] == "Petro-Canada · Rewards ••4321" and subs[1].startswith("Tim Hortons · ") and subs[2] == "tim hortons · Rewards ••4321"
    ids = app.ui.locator("#recent-list [data-again]").evaluate_all("(els) => els.map((e) => e.dataset.again)")
    assert ids[:3] == ["seed-000", "seed-001", "seed-003"] and len(set(ids)) == 10
    app.ui.locator('#recent-list [data-again="seed-003"]').click()
    assert app.sheet_hidden() and app.toast().inner_text() == "Saved $4.75 · Restaurant / Take-Out"
    check_copy("seed-003")
    assert app.state()["settings"]["lastPayment"] == {"methodId": "credit", "cardId": None}     # a repeat does not change the default

    # with automatic location on, a repeat gets a fresh location of its own
    app.tab("profile")
    app.ui.locator("#set-auto-loc").check()
    app.tab("add")
    app.ui.locator("#btn-recent").click()
    app.ui.locator('#recent-list [data-again="seed-000"]').click()
    wait_until(lambda: any(e["location"] for e in app.expenses() if not e["id"].startswith("seed-")))
    new = [e for e in app.expenses() if not e["id"].startswith("seed-")][0]
    assert new["location"]["lat"] == 51.04471 and new["location"]["capturedAt"] != PIN["capturedAt"]
    assert app.console_errors == []

    # a new user has nothing to repeat: no Recent button
    b = make_app()
    assert b.ui.locator("#btn-recent").count() == 0
    b.add("2", "Groceries")
    assert b.ui.locator("#btn-recent").count() == 1


# ---------------------------------------------------------------- 10
def test_10_merchant_remembers_category(app):
    def with_merchant(amount, merchant):
        app.type_amount(amount)
        app.ui.locator("#details-row").click()
        app.ui.locator("#d-merchant").fill(merchant)
        app.ui.locator("#d-done").click()

    assert app.ui.locator("#usual-pill").count() == 0
    with_merchant("2.25", "Tim Hortons")
    assert app.ui.locator("#usual-pill").count() == 0                              # never seen before
    app.chip("Restaurant / Take-Out").click()
    with_merchant("3.10", "Tim Hortons")
    app.chip("Restaurant / Take-Out").click()
    chips_before = app.ui.locator("#chips .chip-name").all_inner_texts()

    # typing the merchant (any case) shows the suggestion above the chips, live while the sheet is open
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-merchant").fill("tim hort")
    assert app.ui.locator("#usual-pill").count() == 0
    app.ui.locator("#d-merchant").fill("tim hortons")
    assert app.ui.locator("#usual-pill").count() == 1
    app.ui.locator("#d-done").click()
    pill = app.ui.locator("#usual-pill")
    assert pill.inner_text() == "Usual: 🍔 Restaurant / Take-Out"
    above = app.page.evaluate("document.getElementById('usual-pill').getBoundingClientRect().bottom <= document.getElementById('chips').getBoundingClientRect().top")
    assert above
    # with no amount it behaves like a chip: looks disabled, does not save
    assert pill.get_attribute("aria-disabled") == "true"
    pill.click(force=True)
    assert app.ui.locator("#amount-hint").inner_text() == "Enter an amount first" and len(app.expenses()) == 2
    app.type_amount("4.50")
    assert pill.get_attribute("aria-disabled") == "false"
    pill.click()
    assert app.toast().inner_text() == "Saved $4.50 · Restaurant / Take-Out"
    saved = [e for e in app.expenses() if e["amountCents"] == 450][0]
    assert saved["categoryId"] == "food.restaurant-take-out" and saved["merchant"] == "tim hortons"
    assert app.ui.locator("#usual-pill").count() == 0                              # gone with the cleared merchant
    assert app.ui.locator("#chips .chip-name").all_inner_texts() == chips_before   # chip order stays frozen

    # most used wins; a tie goes to the most recent; a hidden category is not suggested
    rows = [("2026-11-01", 100, "groceries", "credit", "Corner Shop", ""), ("2026-11-05", 100, "shopping", "credit", "Corner Shop", ""),
            ("2026-11-02", 100, "gas", "credit", "Depot", ""), ("2026-11-03", 100, "gas", "credit", "Depot", ""),
            ("2026-11-09", 100, "car", "credit", "Depot", ""),
            ("2026-11-02", 100, "gifts", "credit", "Café Olé", "")]
    st = make_state(rows)
    app.seed(st)
    for merchant, want in [("corner shop", "Usual: 🛍️ Shopping"), ("Depot", "Usual: ⛽ Gas / Diesel"), ("cafe ole", "Usual: 🎁 Gifts")]:
        with_merchant("1", merchant)
        assert app.ui.locator("#usual-pill").inner_text() == want
        app.ui.locator('[data-key="back"]').click()
    [c for c in st["categories"] if c["id"] == "misc.gifts"][0]["hidden"] = True
    app.seed(st)
    with_merchant("1", "Café Olé")
    assert app.ui.locator("#usual-pill").count() == 0
    assert app.console_errors == []


# ---------------------------------------------------------------- 11
def filter_rows():
    cards = [make_card("card-a", "Maple Rewards Visa", nickname="Rewards", last4="4321"),
             make_card("card-b", "Maple Everyday Debit", kind="debit", networks=("Interac",), colour="blue")]
    rows = [("2026-11-15", 475, "dining", "credit", "Café Olé", "latte", "card-a", PIN),
            ("2026-11-14", 3899, "dining", "credit", "Phil & Sebastian", "Brunch", "card-a"),
            ("2026-11-10", 8412, "groceries", "debit", "Co-op", "", "card-b", PIN),
            ("2026-10-28", 7250, "groceries", "credit", "Co-op", "cafe run", "card-a"),
            ("2026-10-20", 1500, "dining", "cash", "Cafe Rosso", "", None, PIN),
            ("2026-09-02", 9900, "medical", "credit", "Pharmacy", "", None),
            ("2025-12-20", 2000, "dining", "credit", "CAFÉ central", "", "card-a")]
    return rows, cards


def test_11_search_and_filters(app):
    rows, cards = filter_rows()
    app.seed(make_state(rows, cards=cards))
    app.tab("history")
    total = lambda: cents(app.ui.locator("#results-total").inner_text())
    shown = lambda: app.ui.locator('.row[data-act="edit"]').evaluate_all("(els) => els.map((e) => e.dataset.id)")
    assert app.ui.locator("#h-filters .fchip").all_inner_texts() == ["Category", "Card", "📍 Has location"]
    assert app.ui.locator("#month-label").inner_text() == "November 2026" and app.ui.locator("#f-clear").count() == 0

    # text: merchant and note, ignoring case and accents, across all months
    search = app.ui.locator("#h-search")
    search.click()
    app.page.keyboard.type("cafe")
    assert app.page.evaluate("document.activeElement.id") == "h-search"            # typing keeps the focus
    assert shown() == ["seed-000", "seed-003", "seed-004", "seed-006"]
    assert total() == 475 + 7250 + 1500 + 2000
    assert app.ui.locator("#results-count").inner_text() == "4 results across all months"
    assert app.ui.locator("#month-label").count() == 0 and app.ui.locator('[data-act="month"]').count() == 0
    groups = app.ui.locator(".month-group")
    assert groups.evaluate_all("(els) => els.map((e) => e.dataset.month)") == ["2026-11", "2026-10", "2025-12"]
    assert app.ui.locator(".month-name").all_inner_texts() == ["November 2026", "October 2026", "December 2025"]
    assert [cents(t) for t in app.ui.locator(".month-sum").all_inner_texts()] == [475, 8750, 2000]
    assert groups.nth(1).locator("section.day").count() == 2
    assert [cents(t) for t in groups.nth(1).locator(".day-total").all_inner_texts()] == [7250, 1500]
    search.fill("CAFÉ")
    assert len(shown()) == 4
    search.fill("cafe")

    # + category (multi-select sheet)
    app.ui.locator("#f-category").click()
    assert app.ui.locator("#fc-list input[data-item]").count() == 45 and app.ui.locator("#fc-list input[data-group]").count() == 8
    app.ui.locator('#fc-list label:has-text("Restaurant / Take-Out")').click()
    app.ui.locator("#fc-done").click()
    assert app.ui.locator("#f-category").inner_text() == "Restaurant / Take-Out"
    assert shown() == ["seed-000", "seed-004", "seed-006"] and total() == 3975
    # + card
    app.ui.locator("#f-card").click()
    app.ui.locator('#fk-list .row:has-text("Rewards")').click()
    assert shown() == ["seed-000", "seed-006"] and total() == 2475
    # + has location
    app.ui.locator("#f-loc").click()
    assert app.ui.locator("#f-loc").get_attribute("aria-pressed") == "true"
    assert shown() == ["seed-000"] and total() == 475
    assert app.ui.locator("#results-count").inner_text() == "1 result across all months"
    # nothing matches
    search.fill("cafe zzz")
    assert "No matching expenses." in app.ui.locator(".empty").inner_text() and total() == 0

    # Clear resets everything
    app.ui.locator("#f-clear").click()
    assert search.input_value() == "" and app.ui.locator("#f-clear").count() == 0
    assert app.ui.locator("#month-label").inner_text() == "November 2026"
    assert cents(app.ui.locator("#month-total").inner_text()) == 475 + 3899 + 8412
    assert app.ui.locator("#h-filters .fchip").all_inner_texts() == ["Category", "Card", "📍 Has location"]
    assert app.ui.locator('#h-filters [aria-pressed="true"]').count() == 0

    # filters on their own
    app.ui.locator("#f-loc").click()
    assert shown() == ["seed-000", "seed-002", "seed-004"] and total() == 475 + 8412 + 1500
    app.ui.locator("#f-loc").click()
    app.ui.locator("#f-card").click()
    app.ui.locator('#fk-list .row:has-text("Cash & other")').click()
    assert shown() == ["seed-004", "seed-005"] and total() == 11400
    app.ui.locator("#f-clear").click()
    app.ui.locator("#f-category").click()
    app.ui.locator('#fc-list label:has-text("Restaurant / Take-Out")').click()
    app.ui.locator('#fc-list label:has-text("Groceries")').click()
    assert app.ui.locator("#f-category").inner_text() == "Food"                    # applied while the sheet is open; both Food items = the group
    app.ui.locator("#fc-done").click()
    assert total() == 475 + 3899 + 8412 + 7250 + 1500 + 2000
    app.ui.locator("#f-category").click()
    assert app.ui.locator("#fc-list input[data-item]:checked").count() == 2
    app.ui.locator("#fc-none").click()
    app.ui.locator("#fc-done").click()
    assert app.ui.locator("#f-clear").count() == 0

    # editing from a filtered list keeps the filter
    search.fill("pharmacy")
    app.ui.locator('.row[data-id="seed-005"]').click()
    app.ui.locator("#e-amount").fill("100")
    app.ui.locator("#e-save").click()
    assert app.ui.locator("#h-search").input_value() == "pharmacy" and total() == 10000
    # filters are kept while moving between tabs, until cleared
    app.tab("add")
    app.tab("history")
    assert app.ui.locator("#h-search").input_value() == "pharmacy" and shown() == ["seed-005"]
    assert app.console_errors == []


# ---------------------------------------------------------------- 12
def touch_drag(app, x, y, dx, dy, steps=10):
    """A real touch gesture through the browser's input pipeline (so touch-action and scrolling apply)."""
    cdp = app.context.new_cdp_session(app.page)
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
    for i in range(1, steps + 1):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x + dx * i / steps, "y": y + dy * i / steps}]})
        app.page.wait_for_timeout(16)
    cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    cdp.detach()
    app.page.wait_for_timeout(800)           # let the scroll's momentum finish


def test_12_swipe_actions(app):
    app.seed(make_state(SAMPLE_ROWS))
    n = len(SAMPLE_ROWS)
    app.tab("history")
    row = lambda i: app.ui.locator(f'.row[data-id="seed-{i:03d}"]')
    wrap = lambda i: app.ui.locator(f'.swipe[data-id="seed-{i:03d}"]')
    shift = lambda i: row(i).evaluate("(e) => new DOMMatrix(getComputedStyle(e).transform).m41")
    assert app.page.evaluate("getComputedStyle(document.querySelector('.swipe .row')).touchAction") == "pan-y"

    # a short swipe left reveals Delete and deletes nothing
    drag(app, row(2), -70)
    app.page.wait_for_timeout(300)
    assert shift(2) == -88 and "show-delete" in wrap(2).get_attribute("class")
    assert len(app.expenses()) == n and app.toast().count() == 0 and app.sheet_hidden()
    # only one row is open at a time
    drag(app, row(4), -70)
    app.page.wait_for_timeout(300)
    assert shift(2) == 0 and shift(4) == -88
    # tapping elsewhere closes it and does nothing else
    row(6).click()
    app.page.wait_for_timeout(300)
    assert shift(4) == 0 and app.sheet_hidden()
    app.page.wait_for_timeout(200)
    # tapping the open row itself also just closes it
    drag(app, row(2), -70)
    app.page.wait_for_timeout(400)
    box = row(2).bounding_box()
    app.page.mouse.click(box["x"] + 60, box["y"] + box["height"] / 2)
    app.page.wait_for_timeout(300)
    assert shift(2) == 0 and app.sheet_hidden()
    # the revealed Delete button deletes, with Undo instead of a confirmation
    drag(app, row(2), -70)
    app.page.wait_for_timeout(400)
    box = wrap(2).bounding_box()
    app.page.mouse.click(box["x"] + box["width"] - 40, box["y"] + box["height"] / 2)
    assert app.toast().inner_text() == "Expense deleted" and app.ui.locator(".toast-undo").is_visible()
    assert len(app.expenses()) == n - 1 and row(2).count() == 0 and app.sheet_hidden()
    app.ui.locator(".toast-undo").click()
    assert len(app.expenses()) == n and row(2).count() == 1
    assert [e for e in app.expenses() if e["id"] == "seed-002"][0]["merchant"] == "Petro-Canada"

    # a full swipe left deletes straight away, with Undo
    app.page.wait_for_timeout(400)
    drag(app, row(3), -260)
    assert app.toast().inner_text() == "Expense deleted"
    assert len(app.expenses()) == n - 1 and row(3).count() == 0
    app.ui.locator(".toast-undo").click()
    assert len(app.expenses()) == n and row(3).count() == 1

    # a swipe right logs it again today
    app.page.wait_for_timeout(400)
    drag(app, row(3), 130)
    assert app.toast().inner_text() == "Saved $38.99 · Restaurant / Take-Out"
    new = [e for e in app.expenses() if not e["id"].startswith("seed-")]
    assert len(new) == 1 and new[0]["date"] == "2026-11-15" and new[0]["merchant"] == "Phil & Sebastian"
    app.ui.locator(".toast-undo").click()
    assert len(app.expenses()) == n
    # too short a swipe does nothing either way
    app.page.wait_for_timeout(2300)
    drag(app, row(3), 40)
    drag(app, row(3), -30)
    app.page.wait_for_timeout(300)
    assert shift(3) == 0 and len(app.expenses()) == n and app.toast().count() == 0

    # a vertical drag scrolls the list and triggers neither action (real touch input)
    view = app.ui.locator("#view")
    assert view.evaluate("(v) => v.scrollHeight > v.clientHeight + 200")
    box = row(4).bounding_box()
    touch_drag(app, box["x"] + 200, box["y"] + 20, 14, -260)
    down = view.evaluate("(v) => v.scrollTop")
    assert down > 150
    assert len(app.expenses()) == n and app.toast().count() == 0 and app.sheet_hidden()
    assert app.ui.locator(".swipe.show-delete, .swipe.show-again").count() == 0
    touch_drag(app, 200, 300, -14, 260)
    assert view.evaluate("(v) => v.scrollTop") < down - 150 and len(app.expenses()) == n
    view.evaluate("(v) => { v.scrollTop = 0; }")
    # a steep diagonal (more down than across) is still a scroll, not a swipe
    drag(app, row(4), -60, 120)
    drag(app, row(4), 90, 150)
    app.page.wait_for_timeout(300)
    assert len(app.expenses()) == n and app.toast().count() == 0 and shift(4) == 0
    # real touch swipes work too
    box = row(5).bounding_box()
    touch_drag(app, box["x"] + 300, box["y"] + 25, -80, 4)
    assert shift(5) == -88 and len(app.expenses()) == n
    row(7).scroll_into_view_if_needed()
    app.page.wait_for_timeout(300)
    box = row(7).bounding_box()
    touch_drag(app, box["x"] + 80, box["y"] + 25, 140, -5)
    assert app.toast().inner_text() == "Saved $95.75 · Groceries" and len(app.expenses()) == n + 1
    app.ui.locator(".toast-undo").click()

    # every action also works without swiping: a tap opens the Edit sheet with Delete and Log again today
    app.page.wait_for_timeout(400)
    row(3).click()
    assert app.ui.locator("#e-delete").is_visible() and app.ui.locator("#e-again").is_visible()
    app.ui.locator("#e-delete").click()
    assert app.ui.locator("#e-confirm-text").inner_text() == "Delete this expense?"
    app.page.keyboard.press("Escape")
    assert len(app.expenses()) == n
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 13
def test_13_first_run_setup(make_app):
    app = make_app(skip_welcome=False, geolocation=CALGARY)
    title = app.ui.locator("#sheet-title")
    assert title.inner_text() == "Track spending in seconds"
    assert app.ui.locator("#ob-step").inner_text() == "Step 1 of 2"
    assert app.ui.locator("#ob-privacy").inner_text() == PRIVACY
    assert app.state() is None or app.state()["settings"]["onboarded"] is False
    app.ui.locator("#ob-next").click()

    # step 2 (v2.1: the card step is gone): automatic location, off by default; turning it on asks for permission
    assert title.inner_text() == "Add location to expenses?" and app.ui.locator("#ob-step").inner_text() == "Step 2 of 2"
    toggle = app.ui.locator("#ob-auto")
    assert not toggle.is_checked() and (app.state() is None or app.state()["settings"]["autoLocation"] is False)
    toggle.check()
    assert app.state()["settings"]["autoLocation"] is True
    toggle.uncheck()
    assert app.state()["settings"]["autoLocation"] is False
    app.ui.locator("#ob-done").click()
    assert app.sheet_hidden() and app.ui.locator('.tab[data-tab="add"]').get_attribute("aria-current") == "page"
    assert app.state()["settings"]["onboarded"] is True and app.cards() == []

    # never again...
    app.page.reload()
    app.ui.locator("#amount").wait_for()
    app.page.wait_for_timeout(200)
    assert app.sheet_hidden() and app.ui.locator("#ob-skip").count() == 0
    # ...unless asked for from Profile → About
    app.tab("profile")
    again = app.ui.locator("#btn-setup-again")
    assert again.inner_text() == "Run setup again"
    again.click()
    assert title.inner_text() == "Track spending in seconds"
    app.ui.locator("#ob-next").click()
    app.ui.locator("#ob-skip").click()
    assert app.sheet_hidden()
    assert app.console_errors == [] and app.dialogs == []

    # it can be skipped at either step, and every way of closing it counts
    for step, closer in [(1, "skip"), (2, "skip"), (1, "escape"), (1, "backdrop"), (2, "x")]:
        b = make_app(skip_welcome=False)
        for _ in range(step - 1):
            b.ui.locator("#ob-next").click()
        if closer == "skip":
            b.ui.locator("#ob-skip").click()
        elif closer == "escape":
            b.page.keyboard.press("Escape")
        elif closer == "backdrop":
            b.page.mouse.click(195, 30)
        else:
            b.ui.locator("[data-sheet-close]").click()
        assert b.sheet_hidden()
        st = b.state()
        assert st["settings"]["onboarded"] is True and st["cards"] == [] and st["settings"]["autoLocation"] is False
        b.add("5", "Groceries")
        b.page.reload()
        b.ui.locator("#amount").wait_for()
        assert b.ui.locator("#ob-skip").count() == 0
        b.close()

    # permission refused: the switch goes back off, with the reason
    c = make_app(skip_welcome=False)
    c.ui.locator("#ob-next").click()
    c.ui.locator("#ob-auto").check()
    c.ui.locator("#ob-loc-error").filter(has_text="Location is off").wait_for()
    assert c.ui.locator("#ob-loc-error").inner_text() == DENIED
    assert not c.ui.locator("#ob-auto").is_checked() and c.state()["settings"]["autoLocation"] is False

    # not shown when there is already data
    e = make_app(skip_welcome=False, open_page=False)
    e.page.goto(e.base_url + "/")
    e.page.evaluate("s => localStorage.setItem('dailyspend.state', JSON.stringify(s))", make_state(SAMPLE_ROWS[:2], onboarded=False))
    e.page.reload()
    e.ui.locator("#amount").wait_for()
    assert e.ui.locator("#ob-skip").count() == 0 and e.sheet_hidden()


# ---------------------------------------------------------------- 14
V1_CSV = "\r\n".join([
    "id,date,amount,category,payment_method,merchant,note,tax_tag,created_at,updated_at",
    "v1-a,2026-11-02,1234.50,Groceries,Debit (Interac),\"Joe's \"\"Fresh\"\" Market, Inc.\",\"line one\nline two\",,2026-11-02T10:00:00.000Z,2026-11-02T10:00:00.000Z",
    "v1-b,2026-11-03,9.99,Dining & coffee,Credit card,'=SUM(A1:A9),'+1 403 555 0100,,2026-11-03T10:00:00.000Z,2026-11-03T11:00:00.000Z",
    "v1-c,2026-11-04,45.00,Vet,Pre-authorised debit,Clinic,,medical,2026-11-04T10:00:00.000Z,2026-11-04T10:00:00.000Z",
    "v1-d,2026-11-05,20.00,Transit,Cash,,,,2026-11-05T10:00:00.000Z,2026-11-05T10:00:00.000Z",
]) + "\r\n"


def test_14_csv_v2_round_trip_and_v1_restore(make_app):
    cards = [make_card("card-a", "American Express Cobalt Card", nickname="Cobalt", last4="1234", issuer="American Express",
                       networks=("American Express",), colour="rose", catalogue_id="amex-cobalt"),
             make_card("card-b", "Maple Everyday Debit", kind="debit", networks=("Interac",), colour="blue"),
             make_card("card-c", "=Odd card", kind="prepaid", networks=(), last4="0007", archived=True)]
    rows = [("2026-11-15", 475, "dining", "credit", "Café Olé", "latte, large", "card-a", PIN),
            ("2026-11-14", 3899, "groceries", "debit", "Co-op", "", "card-b"),
            ("2026-11-13", 1500, "transit", "prepaid", "", "", "card-c", {"lat": -33.86882, "lng": 151.20929, "accuracyM": None, "capturedAt": "2026-11-13T01:00:00.000Z"}),
            ("2026-11-12", 2000, "medical", "cash", "Pharmacy", "", None, {"lat": 0.0, "lng": -0.5, "accuracyM": 1200, "capturedAt": "2026-11-12T01:00:00.000Z"}),
            ("2026-11-11", 999, "gas", "credit", "Esso", "", None)]
    src = make_app(init_scripts=[CAPTURE_CLIPBOARD])
    src.seed(make_state(rows, cards=cards))
    text = copied_csv(src)
    assert text.split("\r\n")[0] == HEADER == ("id,date,amount,category_group,category,payment_method,card,card_last4,merchant,note,tax_tag,"
                                                "latitude,longitude,location_accuracy_m,created_at,updated_at")
    body = {r[0]: dict(zip(HEADER.split(","), r)) for r in parse_csv(text)[1:]}
    a = body["seed-000"]
    assert (a["payment_method"], a["card"], a["card_last4"]) == ("Credit card", "Cobalt", "1234")
    assert (a["latitude"], a["longitude"], a["location_accuracy_m"]) == ("51.04471", "-114.07188", "25")
    assert (body["seed-001"]["card"], body["seed-001"]["card_last4"], body["seed-001"]["latitude"]) == ("Maple Everyday Debit", "", "")
    c = body["seed-002"]
    assert (c["payment_method"], c["card"], c["card_last4"]) == ("Prepaid card", "'=Odd card", "0007")      # formula safety on card names
    assert (c["latitude"], c["longitude"], c["location_accuracy_m"]) == ("-33.86882", "151.20929", "")
    assert (body["seed-003"]["card"], body["seed-003"]["latitude"], body["seed-003"]["longitude"]) == ("", "0.00000", "-0.50000")
    assert (body["seed-004"]["card"], body["seed-004"]["card_last4"], body["seed-004"]["latitude"], body["seed-004"]["location_accuracy_m"]) == ("", "", "", "")

    # restore into an empty app: same expenses, cards and locations
    dst = make_app(init_scripts=[CAPTURE_CLIPBOARD])
    assert restore(dst, text) == "Restored 5 expenses. Skipped 0 already here and 0 invalid rows."
    got = {e["id"]: e for e in dst.expenses()}
    want = {e["id"]: e for e in src.expenses()}
    for i, e in want.items():
        for f in ["amountCents", "date", "categoryId", "paymentMethodId", "merchant", "note", "createdAt", "updatedAt"]:
            assert got[i][f] == e[f], (i, f)
        if e["location"]:
            assert {k: got[i]["location"][k] for k in ["lat", "lng", "accuracyM"]} == {k: e["location"][k] for k in ["lat", "lng", "accuracyM"]}
        else:
            assert got[i]["location"] is None
    by_id = {c["id"]: c for c in dst.cards()}
    made = sorted([(c["issuer"], c["name"], c["kind"], c["networks"], c["last4"], c["catalogueId"], c["archived"]) for c in dst.cards()], key=lambda x: x[1])
    assert made == [("", "=Odd card", "prepaid", [], "0007", None, False), ("", "Cobalt", "credit", [], "1234", None, False),
                    ("", "Maple Everyday Debit", "debit", [], "", None, False)]            # cards created by hand, as the brief says
    assert by_id[got["seed-000"]["cardId"]]["name"] == "Cobalt" and by_id[got["seed-001"]["cardId"]]["name"] == "Maple Everyday Debit"
    assert by_id[got["seed-002"]["cardId"]]["name"] == "=Odd card"
    assert got["seed-003"]["cardId"] is None and got["seed-004"]["cardId"] is None
    assert copied_csv(dst) == text                                                   # and it exports the same file again
    # a second restore skips everything and creates no cards
    assert restore(dst, text) == "Restored 0 expenses. Skipped 5 already here and 0 invalid rows."
    assert len(dst.cards()) == 3 and len(dst.expenses()) == 5
    # restoring where the cards already exist matches them by name plus last 4, archived ones included
    assert restore(src, text.replace("seed-", "copy-")) == "Restored 5 expenses. Skipped 0 already here and 0 invalid rows."
    assert len(src.cards()) == 3
    copies = {e["id"]: e for e in src.expenses()}
    assert copies["copy-000"]["cardId"] == "card-a" and copies["copy-001"]["cardId"] == "card-b" and copies["copy-002"]["cardId"] == "card-c"

    # an invalid location is ignored, the row is kept; a different last 4 is a different card
    odd = "\r\n".join([
        "date,amount,category,payment_method,card,card_last4,latitude,longitude,location_accuracy_m",
        "2026-11-01,1.00,Groceries,Credit card,Cobalt,1234,95.0,10.0,5",              # latitude out of range
        "2026-11-01,2.00,Groceries,Credit card,Cobalt,9999,10.0,-181,5",              # longitude out of range, other card
        "2026-11-01,3.00,Groceries,Credit card,cobalt,1234,abc,10,5",                 # not a number; name matches ignoring case
        "2026-11-01,4.00,Groceries,Debit card,Maple Everyday Debit,12,45.5,-73.5,x",  # bad last 4 and accuracy are dropped
        "2026-11-01,5.00,Groceries,Cash,New card,,,,",                                # method is not a card kind
        "2026-11-01,6.00,Groceries,Other debit card,,,-90,180,0",                     # edge values are valid
    ]) + "\r\n"
    assert restore(dst, odd) == "Restored 6 expenses. Skipped 0 already here and 0 invalid rows."
    new = {e["amountCents"]: e for e in dst.expenses() if not e["id"].startswith("seed-")}
    cards_now = {c["id"]: c for c in dst.cards()}
    assert new[100]["location"] is None and new[200]["location"] is None and new[300]["location"] is None
    assert cards_now[new[100]["cardId"]]["last4"] == "1234" and new[300]["cardId"] == new[100]["cardId"]
    assert cards_now[new[200]["cardId"]]["last4"] == "9999" and cards_now[new[200]["cardId"]]["name"] == "Cobalt"
    assert new[400]["location"] == {"lat": 45.5, "lng": -73.5, "accuracyM": None, "capturedAt": new[400]["createdAt"]}
    assert cards_now[new[400]["cardId"]]["name"] == "Maple Everyday Debit" and new[400]["paymentMethodId"] == "debit"
    assert cards_now[new[500]["cardId"]]["kind"] == "credit" and new[500]["paymentMethodId"] == "credit"
    assert new[600]["cardId"] is None and new[600]["paymentMethodId"] == "debit"
    assert (new[600]["location"]["lat"], new[600]["location"]["lng"], new[600]["location"]["accuracyM"]) == (-90, 180, 0)
    assert len(dst.cards()) == 5

    # a v1 backup still restores
    old = make_app()
    assert restore(old, V1_CSV) == "Restored 4 expenses. Skipped 0 already here and 0 invalid rows."
    ex = {e["id"]: e for e in old.expenses()}
    assert all(e["cardId"] is None and e["location"] is None for e in ex.values()) and old.cards() == []
    assert (ex["v1-a"]["amountCents"], ex["v1-a"]["paymentMethodId"], ex["v1-a"]["merchant"], ex["v1-a"]["note"]) == (
        123450, "debit", 'Joe\'s "Fresh" Market, Inc.', "line one\nline two")
    assert (ex["v1-b"]["paymentMethodId"], ex["v1-b"]["merchant"], ex["v1-b"]["note"], ex["v1-b"]["updatedAt"]) == (
        "credit", "=SUM(A1:A9)", "+1 403 555 0100", "2026-11-03T11:00:00.000Z")
    assert ex["v1-c"]["paymentMethodId"] == "pad" and ex["v1-d"]["paymentMethodId"] == "cash"
    vet = [c for c in old.state()["categories"] if c["name"] == "Vet"][0]
    assert vet["taxTag"] == "medical" and ex["v1-c"]["categoryId"] == vet["id"]
    assert restore(old, V1_CSV) == "Restored 0 expenses. Skipped 4 already here and 0 invalid rows."
    for a in (src, dst, old):
        assert a.console_errors == [] and a.dialogs == []


# ---------------------------------------------------------------- 15
def test_15_v1_state_migrates(make_app):
    v1 = make_v1_state(SAMPLE_ROWS, last_payment="cash")
    v1["categories"][0]["hidden"] = True
    v1["categories"][1]["name"] = "Coffee runs"
    v1["categories"].append({"id": "c_custom", "emoji": "🐶", "name": "Vet", "taxTag": "medical", "hidden": False, "builtIn": False, "order": 21})
    v1["expenses"][0]["categoryId"] = "c_custom"
    app = make_app(skip_welcome=False, open_page=False)
    app.page.goto(app.base_url + "/")
    app.page.evaluate("([k, s]) => { localStorage.clear(); localStorage.setItem(k, JSON.stringify(s)); }", [LEGACY_KEY, v1])
    raw_before = app.page.evaluate("k => localStorage.getItem(k)", LEGACY_KEY)
    app.page.reload()
    app.ui.locator("#amount").wait_for()
    assert app.ui.locator("#ob-skip").count() == 0                                 # existing users are not walked through setup
    assert "8 budget groups" in app.ui.locator("#mig-text").inner_text()           # v2.2: told once that categories moved
    app.ui.locator("#mig-ok").click()
    assert app.sheet_hidden() and app.ui.locator("#banner-corrupt").count() == 0

    st = app.state()
    assert st["schemaVersion"] == 3 and st["cards"] == []
    assert st["settings"] == {"lastPayment": {"methodId": "cash", "cardId": None}, "testNoticeDismissed": True,
                              "autoLocation": False, "mapsNoticeShown": False, "onboarded": True, "groupsNotice": False}
    assert len(st["expenses"]) == len(v1["expenses"]) == 18
    for old, new in zip(v1["expenses"], st["expenses"]):
        want = "c_custom" if old["categoryId"] == "c_custom" else CAT[old["categoryId"]]
        assert new == {**old, "categoryId": want, "cardId": None, "location": None}    # every field kept; category moved by the table
    cats = {c["id"]: c for c in st["categories"]}
    assert len(cats) == 46
    assert cats["food.groceries"]["hidden"] is True                                # hidden stays hidden
    assert cats["food.restaurant-take-out"]["name"] == "Coffee runs"               # a rename is kept
    assert (cats["c_custom"]["name"], cats["c_custom"]["groupId"], cats["c_custom"]["taxTag"], cats["c_custom"]["builtIn"]) == ("Vet", "misc", "medical", False)
    assert app.page.evaluate("k => localStorage.getItem(k)", LEGACY_KEY) == raw_before      # the old copy is left alone
    # and the app shows it
    assert "Today · Cash" in app.ui.locator("#details-row").inner_text()
    assert "Groceries" not in app.ui.locator("#chips .chip-name").all_inner_texts()
    app.tab("history")
    nov = [r for r in SAMPLE_ROWS if r[0].startswith("2026-11")]
    assert cents(app.ui.locator("#month-total").inner_text()) == sum(r[1] for r in nov)
    assert app.ui.locator('.row[data-id="seed-000"] .row-title').inner_text() == "Vet"
    assert app.ui.locator('.row[data-id="seed-000"] .row-pay').inner_text() == "Credit"
    assert app.ui.locator('.row[data-id="seed-001"] .row-pay').inner_text() == "Debit"
    app.tab("summary")
    assert cents(app.ui.locator('#tax-card [data-tax="medical"] .v').inner_text()) == 28400 + 8412
    # the migration runs once: later changes are not overwritten by the old key
    app.tab("add")
    app.add("1", "Transit")
    app.reload()
    assert len(app.expenses()) == 19
    assert app.console_errors == []

    # an empty v1 state migrates too, and that user does get the welcome
    b = make_app(skip_welcome=False, open_page=False)
    b.page.goto(b.base_url + "/")
    b.page.evaluate("([k, s]) => { localStorage.clear(); localStorage.setItem(k, JSON.stringify(s)); }", [LEGACY_KEY, make_v1_state([], "debit")])
    b.page.reload()
    b.ui.locator("#amount").wait_for()
    assert b.ui.locator("#ob-skip").is_visible()
    assert b.state()["settings"]["lastPayment"] == {"methodId": "debit", "cardId": None} and b.state()["settings"]["onboarded"] is False
    b.ui.locator("#ob-skip").click()
    assert "Today · Debit card" in b.ui.locator("#details-row").inner_text()

    # unreadable v1 data: a copy is kept, the app starts fresh and says so
    c = make_app(skip_welcome=True, open_page=False)
    c.page.goto(c.base_url + "/")
    c.page.evaluate("k => { localStorage.clear(); localStorage.setItem(k, '{broken'); }", LEGACY_KEY)
    c.reload()
    assert "could not be read" in c.ui.locator("#banner-corrupt").inner_text()
    keys = c.page.evaluate("Object.keys(localStorage)")
    assert LEGACY_KEY in keys and len([k for k in keys if k.startswith("dailyspend.state.corrupt.")]) == 1


# ---------------------------------------------------------------- 16
LONG_CARDS = [
    make_card("card-a", "American Express Cobalt Card", nickname="Cobalt", last4="1234", issuer="American Express",
              networks=("American Express",), colour="rose"),
    make_card("card-b", "A Card With A Remarkably Long Product Name Platinum Privilege World Elite", kind="debit",
              issuer="The Very Long Named Savings And Credit Union Of Southern Alberta", networks=("Interac", "Visa Debit"), last4="0042", colour="blue"),
    make_card("card-c", "Prairie Reloadable Prepaid", kind="prepaid", nickname="WWWWWWWWWWWWWWWWWWWWWWWW", colour="green"),
    make_card("card-d", "Old card", archived=True, colour="slate", last4="9999"),
]


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("size", SIZES, ids=lambda s: f"{s[0]}x{s[1]}")
def test_16_layout(make_app, size, scheme):
    app = make_app(width=size[0], height=size[1], scheme=scheme, reduced_motion="reduce", geolocation=CALGARY, skip_welcome=False)
    rows = [r + (None,) for r in SAMPLE_ROWS]
    rows[0] = SAMPLE_ROWS[0] + ("card-a", PIN)
    rows[1] = SAMPLE_ROWS[1] + ("card-b", PIN)
    rows[2] = SAMPLE_ROWS[2] + ("card-c",)
    rows[3] = SAMPLE_ROWS[3] + ("card-d",)
    rows.append(("2026-11-15", 9999999, "utilities", "pad", "A very long merchant name that keeps going and going on",
                 "And an equally long note that should be truncated rather than pushing the amount off the screen", "card-b", PIN))

    def check(label):
        bad = app.page.evaluate(LAYOUT_CHECK)
        assert bad == [], f"{label} at {size} {scheme}: {bad}"

    # first-run setup, both steps
    check("welcome 1")
    app.ui.locator("#ob-next").click()
    check("welcome 2")
    app.ui.locator("#ob-skip").click()

    app.seed(make_state(rows, cards=LONG_CARDS))
    # Add: Recent button, the Usual pill, the payment picker and the location row
    check("add")
    assert app.page.evaluate(ADD_FITS) == []
    app.type_amount("99999.99")
    app.ui.locator("#details-row").click()
    check("details sheet with cards")
    app.ui.locator('#d-pay label:has-text("A Card With")').click()
    app.ui.locator("#d-merchant").fill("Tim Hortons")
    app.ui.locator("#d-note").fill("A long note so that the second line of the details row is full of text")
    app.ui.locator("#d-loc-add").scroll_into_view_if_needed()
    app.ui.locator("#d-loc-add").click()
    app.ui.locator("#d-loc-remove").wait_for()
    check("details sheet with location")
    app.ui.locator("#d-done").click()
    assert app.ui.locator("#usual-pill").is_visible()
    check("add with usual pill")
    assert app.page.evaluate(ADD_FITS) == [], "Add must fit without scrolling, even with the Usual pill"
    app.ui.locator("#btn-recent").click()
    check("recent sheet")
    app.page.keyboard.press("Escape")

    # History: filters active, filter sheets, the Edit sheet with a location
    app.tab("history")
    check("history")
    app.ui.locator("#h-search").fill("o")
    app.ui.locator("#f-loc").click()
    app.ui.locator("#f-category").click()
    check("category filter sheet")
    for name in ["Groceries", "Restaurant / Take-Out", "Gas & Hydro"]:
        app.ui.locator(f'#fc-list label:has-text("{name}")').click()
    app.ui.locator("#fc-done").click()
    app.ui.locator("#f-card").click()
    check("card filter sheet")
    app.ui.locator('#fk-list .row:has-text("A Card With")').click()
    check("history with every filter")
    app.ui.locator("#f-clear").click()
    app.tab("summary")
    app.ui.locator('#daily-bars .daybar[data-day="2026-11-15"]').click()
    check("history with a day filter")
    drag(app, app.ui.locator('.row[data-act="edit"]').first, -70)
    app.page.wait_for_timeout(100)
    # the row itself is meant to slide off to the left; the page must not gain a sideways scroll
    assert app.page.evaluate("[document.documentElement.scrollWidth <= innerWidth, document.getElementById('view').scrollWidth <= document.getElementById('view').clientWidth]") == [True, True]
    box = app.ui.locator(".swipe.show-delete").bounding_box()
    assert box["x"] >= 0 and box["x"] + box["width"] <= size[0]
    app.ui.locator("#h-search").click()
    app.page.wait_for_timeout(400)
    app.ui.locator('.row[data-act="edit"]').first.click()
    check("edit sheet")
    app.ui.locator("#e-maps").scroll_into_view_if_needed()
    check("edit sheet at location")
    app.ui.locator("#e-maps").click()
    check("edit sheet with maps notice")
    app.ui.locator("#e-maps-cancel").click()
    app.ui.locator("#e-loc-remove").click()
    check("edit sheet without location")
    app.page.keyboard.press("Escape")

    # Summary: charts and By card
    app.tab("summary")
    check("summary")
    chart = app.page.evaluate("""() => {
      const card = document.getElementById('charts').getBoundingClientRect();
      return ['donut', 'daily-bars'].map((id) => { const r = document.getElementById(id).getBoundingClientRect();
        return r.left >= card.left && r.right <= card.right && r.width > 150; });
    }""")
    assert chart == [True, True]
    assert app.ui.locator("#by-card .cat-row").count() == 5

    # Profile: My cards, archived, add card, card forms
    app.tab("profile")
    check("profile")
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()
    check("picker: institutions")
    app.ui.locator("#ac-search").fill("ma")
    check("picker: search")
    app.ui.locator("#ac-search").fill("")
    app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    check("picker: types")
    app.ui.locator('#ac-types [data-kind="credit"]').click()
    check("picker: cards")
    app.ui.locator("#ac-cards .row").first.click()
    check("card confirmation")
    app.ui.locator("#cf-last4").fill("1")
    app.ui.locator("#cf-save").scroll_into_view_if_needed()
    app.ui.locator("#cf-save").click()
    check("card confirmation with error")
    app.ui.locator("#cf-cancel").click()
    app.ui.locator("#ac-manual-here").click()
    check("add card by hand")
    app.ui.locator("[data-sheet-close]").click()
    app.ui.locator('#card-list .card-tile:has-text("A Card With")').click()
    check("edit card")
    app.ui.locator("#cf-remove").scroll_into_view_if_needed()
    app.ui.locator("#cf-remove").click()
    check("remove card confirmation")
    app.page.keyboard.press("Escape")
    assert app.console_errors == []
