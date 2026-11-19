"""Acceptance tests from the v2.1 brief, section 6 (test numbers match the brief).

The fixture card list (conftest.FIXTURE_CARDS) has Maple Bank with credit, debit and prepaid cards,
American Express with credit cards only, and The Northern Trust with a single debit card.
"""
import re

from conftest import make_card, make_state
from test_v1 import cents, source
from test_v2 import wait_cached

PICKER_LEVEL = """() => ({
  title: document.getElementById('sheet-title').textContent,
  focus: document.activeElement && document.activeElement.id,
  back: !!document.querySelector('.sheet [data-sheet-back]'),
  anim: getComputedStyle(document.querySelector('.sheet-body')).animationDuration,
  name: getComputedStyle(document.querySelector('.sheet-body')).animationName,
})"""


def open_picker(app):
    app.tab("profile")
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()


def titles(app, scope):
    return app.ui.locator(f"{scope} .row-title").all_inner_texts()


def subs(app, scope):
    return app.ui.locator(f"{scope} .row-sub").all_inner_texts()


# ---------------------------------------------------------------- 1
def test_01_full_picker_path(app):
    app.tab("profile")
    assert app.ui.locator("#no-cards").inner_text() == "Add the cards you use to see spending by card."
    assert app.ui.locator("#btn-add-card").inner_text() == "Add a card"
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()

    # Level 1: institutions, alphabetical (a leading "The" is ignored), with counts, monograms and chevrons
    lvl = app.page.evaluate(PICKER_LEVEL)
    assert lvl["title"] == "Add a card" and lvl["focus"] == "sheet-title" and lvl["back"] is False
    assert app.ui.locator("#ac-search").get_attribute("placeholder") == "Search a bank or card"
    assert titles(app, "#ac-list [data-issuer]") == ["American Express", "Maple Bank", "The Northern Trust", "Prairie Credit Union"]
    assert subs(app, "#ac-list [data-issuer]") == ["2 cards", "4 cards", "1 card", "2 cards"]
    assert app.ui.locator("#ac-list .ibadge").evaluate_all("(els) => els.map((e) => e.dataset.t)") == ["Amex", "Maple", "NT", "PCU"]
    assert app.ui.locator("#ac-list .group-head").all_inner_texts() == ["Popular", "All institutions"]      # v2.2 sections
    assert app.ui.locator("#ac-list [data-issuer] .chev").count() == 4
    assert app.ui.locator("#ac-list [data-cat-id]").count() == 0                      # no cards until one is searched for
    assert app.ui.locator("#ac-manual").inner_text() == "My bank or card isn't listed"
    assert app.ui.locator(".sheet img, .sheet input[type=checkbox]").count() == 0     # no logos, no multi-select

    # Level 2: the types that institution has, with counts
    app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    lvl = app.page.evaluate(PICKER_LEVEL)
    assert lvl["title"] == "Maple Bank" and lvl["focus"] == "sheet-title" and lvl["back"] is True
    assert lvl["name"] == "slide-fwd" and float(lvl["anim"].rstrip("s")) <= 0.25
    assert titles(app, "#ac-types") == ["Credit cards", "Debit cards", "Other cards"]
    assert subs(app, "#ac-types") == ["2 cards", "1 card", "1 card"]
    assert app.ui.locator("#ac-types .chev").count() == 3
    assert app.ui.locator("#ac-manual-here").inner_text() == "Card not listed at Maple Bank"

    # Level 3: only that institution's credit cards, with networks in small text
    app.ui.locator('#ac-types [data-kind="credit"]').click()
    lvl = app.page.evaluate(PICKER_LEVEL)
    assert lvl["title"] == "Maple Bank · Credit cards" and lvl["focus"] == "sheet-title" and lvl["back"] is True
    assert titles(app, "#ac-cards") == ["Maple Rewards Visa", "Maple Travel World Mastercard"]
    assert subs(app, "#ac-cards") == ["Visa", "Mastercard"]
    assert app.ui.locator("#ac-cards .badge").count() == 0
    assert app.ui.locator(".sheet input[type=checkbox]").count() == 0

    # Level 4: the confirm step, then save
    app.ui.locator('#ac-cards .row:has-text("Maple Rewards Visa")').click()
    lvl = app.page.evaluate(PICKER_LEVEL)
    assert lvl["title"] == "Confirm card" and lvl["back"] is True and lvl["focus"] == "sheet-title"
    assert "Maple Rewards Visa" in app.ui.locator("#cf-summary").inner_text()
    assert app.ui.locator("#cf-nick").is_visible() and app.ui.locator("#cf-last4").is_visible()
    assert app.ui.locator("#cf-colours input").count() == 8
    assert app.cards() == []
    app.ui.locator("#cf-nick").fill("Everyday")
    app.ui.locator("#cf-last4").fill("4321")
    app.ui.locator("#cf-save").click()
    assert app.sheet_hidden()
    assert app.toast().inner_text() == "Added Maple Rewards Visa"
    assert app.ui.locator('.tab[data-tab="profile"]').get_attribute("aria-current") == "page"
    assert app.ui.locator("#card-list .card-tile .row-title").all_inner_texts() == ["Everyday"]
    card = app.cards()[0]
    assert (card["catalogueId"], card["issuer"], card["name"], card["kind"], card["networks"], card["nickname"], card["last4"]) == (
        "maple-rewards-visa", "Maple Bank", "Maple Rewards Visa", "credit", ["Visa"], "Everyday", "4321")
    assert app.ui.locator("#no-cards").count() == 0 and app.ui.locator("#btn-add-card").inner_text() == "Add a card"
    # the other types list only their own cards
    app.ui.locator("#btn-add-card").click()
    app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    app.ui.locator('#ac-types [data-kind="prepaid"]').click()
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "Maple Bank · Other cards"
    assert titles(app, "#ac-cards") == ["Maple Travel Prepaid"]
    app.page.keyboard.press("Escape")
    app.ui.locator('#ac-types [data-kind="debit"]').click()
    assert titles(app, "#ac-cards") == ["Maple Everyday Debit"] and subs(app, "#ac-cards") == ["Interac / Visa Debit"]
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 2
def test_02_single_type_institution_skips_level_2(app):
    open_picker(app)
    app.ui.locator('#ac-list [data-issuer="American Express"]').click()
    assert app.ui.locator("#ac-types").count() == 0
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "American Express · Credit cards"
    assert titles(app, "#ac-cards") == ["American Express Cobalt Card", "American Express Green Card"]      # the unknown kind is ignored
    app.ui.locator("[data-sheet-back]").click()                                       # back returns to Level 1
    lvl = app.page.evaluate(PICKER_LEVEL)
    assert lvl["title"] == "Add a card" and lvl["name"] == "slide-back" and app.ui.locator("#ac-search").is_visible()
    # a debit-only institution too, and Escape does the same as the arrow
    app.ui.locator('#ac-list [data-issuer="The Northern Trust"]').click()
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "The Northern Trust · Debit cards"
    app.page.keyboard.press("Escape")
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "Add a card"
    # back from the confirm step returns to that card list, then to Level 1
    app.ui.locator('#ac-list [data-issuer="American Express"]').click()
    app.ui.locator('#ac-cards .row:has-text("Green")').click()
    app.ui.locator("[data-sheet-back]").click()
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "American Express · Credit cards"
    app.ui.locator("[data-sheet-back]").click()
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "Add a card" and app.cards() == []


# ---------------------------------------------------------------- 3
def test_03_search(app):
    open_picker(app)
    search = app.ui.locator("#ac-search")
    search.click()
    app.page.keyboard.type("prairie")                                                 # a bank name filters the institutions
    assert app.page.evaluate("document.activeElement.id") == "ac-search"
    assert titles(app, "#ac-list [data-issuer]") == ["Prairie Credit Union"]
    assert app.ui.locator("#ac-cards-head").inner_text() == "Cards"
    assert titles(app, "#ac-list [data-cat-id]") == ["Prairie Cash Back Mastercard", "Prairie Reloadable Prepaid"]
    # institutions come first, the Cards group below them
    order = app.ui.locator("#ac-list > *").evaluate_all("(els) => els.map((e) => e.dataset.issuer ? 'institution' : e.dataset.catId ? 'card' : 'head')")
    assert order == ["institution", "head", "card", "card"]
    search.fill("NORTHERN trust")
    assert titles(app, "#ac-list [data-issuer]") == ["The Northern Trust"] and app.ui.locator("#ac-list [data-cat-id]").count() == 0

    # a card name shows the Cards group as "Card name · Institution · Credit"; case and accents are ignored
    for query in ["cobalt", "CÓBALT", "express cobalt"]:
        search.fill(query)
        assert app.ui.locator("#ac-list [data-issuer]").count() == 0
        assert app.ui.locator("#ac-cards-head").inner_text() == "Cards"
        row = app.ui.locator("#ac-list [data-cat-id]")
        assert row.count() == 1
        assert row.locator(".row-title").inner_text() == "American Express Cobalt Card"
        assert row.locator(".row-sub").inner_text() == "American Express · Credit"
    search.fill("prepaid")
    assert subs(app, "#ac-list [data-cat-id]") == ["Maple Bank · Prepaid", "Prairie Credit Union · Prepaid"]
    search.fill("zzz")
    assert "Nothing matches" in app.ui.locator("#card-no-match").inner_text() and app.ui.locator("#ac-manual").is_visible()

    # tapping a card result opens the confirm step directly
    search.fill("cobalt")
    app.ui.locator("#ac-list [data-cat-id]").click()
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "Confirm card"
    assert "American Express Cobalt Card" in app.ui.locator("#cf-summary").inner_text()
    app.ui.locator("[data-sheet-back]").click()                                       # back goes up to Level 1, search kept
    assert app.ui.locator("#ac-search").input_value() == "cobalt" and app.ui.locator("#ac-list [data-cat-id]").count() == 1
    app.ui.locator("#ac-list [data-cat-id]").click()
    app.ui.locator("#cf-save").click()
    assert app.toast().inner_text() == "Added American Express Cobalt Card"
    assert [c["catalogueId"] for c in app.cards()] == ["amex-cobalt"]
    assert app.console_errors == []


# ---------------------------------------------------------------- 4
def test_04_added_badge(app):
    app.seed(make_state([], cards=[make_card("card-a", "Maple Rewards Visa", catalogue_id="maple-rewards-visa")]))
    open_picker(app)
    app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    app.ui.locator('#ac-types [data-kind="credit"]').click()
    rows = app.ui.locator("#ac-cards .row")
    assert [r.locator(".badge").count() for r in rows.all()] == [1, 0]
    assert rows.first.locator(".badge").inner_text() == "Added"
    app.page.keyboard.press("Escape")
    app.page.keyboard.press("Escape")
    app.ui.locator("#ac-search").fill("maple")                                        # search results show it too
    assert "Added" in app.ui.locator('#ac-list [data-cat-id]:has-text("Maple Rewards Visa")').inner_text()
    assert app.ui.locator("#ac-list [data-cat-id] .badge").count() == 1
    # still selectable: someone can hold two of the same card
    app.ui.locator('#ac-list [data-cat-id]:has-text("Maple Rewards Visa")').click()
    app.ui.locator("#cf-nick").fill("Second one")
    app.ui.locator("#cf-save").click()
    assert [c["catalogueId"] for c in app.cards()] == ["maple-rewards-visa", "maple-rewards-visa"]
    assert len({c["id"] for c in app.cards()}) == 2


# ---------------------------------------------------------------- 5
def test_05_add_by_hand_from_the_footers(app):
    open_picker(app)
    # Level 1 footer: an empty form
    app.ui.locator("#ac-manual").click()
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "Add your own card"
    assert app.ui.locator("#cf-issuer").input_value() == ""
    app.ui.locator("#cf-issuer").fill("Corner Credit Union")
    app.ui.locator("#cf-name").fill("Member Card")
    app.ui.locator('#cf-kinds label:has-text("Debit")').click()
    app.ui.locator("#cf-save").click()
    assert app.toast().inner_text() == "Added Member Card" and app.sheet_hidden()
    card = app.cards()[0]
    assert (card["catalogueId"], card["issuer"], card["name"], card["kind"]) == (None, "Corner Credit Union", "Member Card", "debit")

    # Level 2 footer: the institution is already filled in
    app.ui.locator("#btn-add-card").click()
    app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    app.ui.locator("#ac-manual-here").click()
    assert app.ui.locator("#cf-issuer").input_value() == "Maple Bank"
    app.ui.locator("[data-sheet-back]").click()                                       # back returns to Level 2
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "Maple Bank" and len(app.cards()) == 1
    app.ui.locator("#ac-manual-here").click()
    app.ui.locator("#cf-save").click()
    assert app.ui.locator("#cf-error").inner_text() == "Enter the card's name."
    app.ui.locator("#cf-name").fill("Maple Student Visa")
    app.ui.locator("#cf-network").select_option("Visa")
    app.ui.locator("#cf-save").click()
    assert app.toast().inner_text() == "Added Maple Student Visa"
    new = [c for c in app.cards() if c["name"] == "Maple Student Visa"][0]
    assert (new["catalogueId"], new["issuer"], new["kind"], new["networks"]) == (None, "Maple Bank", "credit", ["Visa"])
    # the card list too has the footer (and the form's Back button works like the arrow)
    app.ui.locator("#btn-add-card").click()
    app.ui.locator('#ac-list [data-issuer="American Express"]').click()
    assert app.ui.locator("#ac-manual-here").inner_text() == "Card not listed at American Express"
    app.ui.locator("#ac-manual-here").click()
    assert app.ui.locator("#cf-issuer").input_value() == "American Express"
    app.ui.locator("#cf-cancel").click()
    assert app.page.evaluate(PICKER_LEVEL)["title"] == "American Express · Credit cards"
    assert app.console_errors == []


# ---------------------------------------------------------------- 6
def test_06_back_escape_and_reopen(make_app):
    app = make_app()
    open_picker(app)
    title = lambda: app.page.evaluate(PICKER_LEVEL)["title"]
    app.ui.locator("#ac-search").fill("maple")
    app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    app.ui.locator('#ac-types [data-kind="credit"]').click()
    app.ui.locator("#ac-cards .row").first.click()
    app.ui.locator("#cf-nick").fill("Half typed")
    assert title() == "Confirm card"
    # Escape goes up one level at a time, and finally closes
    for want in ["Maple Bank · Credit cards", "Maple Bank", "Add a card"]:
        app.page.keyboard.press("Escape")
        assert title() == want and not app.sheet_hidden()
        assert app.page.evaluate("document.activeElement.id") == "sheet-title"
    app.page.keyboard.press("Escape")
    assert app.sheet_hidden() and app.cards() == []
    # reopening starts at Level 1 with the search cleared
    app.ui.locator("#btn-add-card").click()
    assert title() == "Add a card" and app.ui.locator("#ac-search").input_value() == ""
    assert app.ui.locator("#ac-list [data-issuer]").count() == 4
    # the back arrow does the same
    app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    app.ui.locator('#ac-types [data-kind="debit"]').click()
    app.ui.locator("#ac-cards .row").first.click()
    for want in ["Maple Bank · Debit cards", "Maple Bank", "Add a card"]:
        app.ui.locator("[data-sheet-back]").click()
        assert title() == want
    assert app.ui.locator("[data-sheet-back]").count() == 0
    # closing from any level discards what was in progress
    for depth, closer in [(1, "x"), (2, "backdrop"), (3, "x"), (4, "x")]:
        if depth > 1:
            app.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
        if depth > 2:
            app.ui.locator('#ac-types [data-kind="credit"]').click()
        if depth > 3:
            app.ui.locator("#ac-cards .row").first.click()
            app.ui.locator("#cf-nick").fill("Not saved")
        if closer == "x":
            app.ui.locator("[data-sheet-close]").click()
        else:
            app.page.mouse.click(195, 20)
        assert app.sheet_hidden() and app.cards() == []
        app.ui.locator("#btn-add-card").click()
        assert title() == "Add a card" and app.ui.locator("#ac-search").input_value() == ""
    assert app.console_errors == []

    # no sliding with reduced motion
    b = make_app(reduced_motion="reduce")
    open_picker(b)
    b.ui.locator('#ac-list [data-issuer="Maple Bank"]').click()
    assert b.page.evaluate(PICKER_LEVEL)["name"] == "none"


# ---------------------------------------------------------------- 7
def test_07_first_run_has_two_steps_and_no_cards(make_app):
    app = make_app(skip_welcome=False)
    assert app.ui.locator("#ob-step").inner_text() == "Step 1 of 2"
    assert app.ui.locator("#sheet-title").inner_text() == "Track spending in seconds"
    assert "card" not in app.ui.locator(".sheet").inner_text().lower()
    app.ui.locator("#ob-next").click()
    assert app.ui.locator("#ob-step").inner_text() == "Step 2 of 2"
    assert app.ui.locator("#sheet-title").inner_text() == "Add location to expenses?"
    assert not app.ui.locator("#ob-auto").is_checked()                                # off by default
    assert "card" not in app.ui.locator(".sheet").inner_text().lower()
    assert app.ui.locator("#ob-next").count() == 0 and app.ui.locator("#ob-cards, #ob-search").count() == 0
    app.ui.locator("#ob-done").click()
    assert app.sheet_hidden() and app.ui.locator('.tab[data-tab="add"]').get_attribute("aria-current") == "page"
    assert app.cards() == [] and app.state()["settings"]["onboarded"] is True
    assert app.card_requests == 0                                                     # the card list is not even loaded at startup
    app.tab("profile")
    assert app.ui.locator("#btn-setup-again").inner_text() == "Run setup again"
    app.ui.locator("#btn-setup-again").click()
    assert app.ui.locator("#ob-step").inner_text() == "Step 1 of 2"
    assert app.console_errors == []


# ---------------------------------------------------------------- 8
def bars_of(app):
    app.page.wait_for_timeout(400)          # let the 300 ms draw animation finish before measuring
    return app.page.evaluate(BARS)


BARS = """() => {
  const svg = document.getElementById('daily-bars').getBoundingClientRect();
  return Array.from(document.querySelectorAll('#daily-bars .daybar')).map((g) => {
    const bar = g.querySelector('.dbar').getBoundingClientRect(), hit = g.querySelector('.hit').getBoundingClientRect();
    const label = g.querySelector('.over-label');
    const lb = label ? label.getBoundingClientRect() : null;
    return { day: g.dataset.day, h: bar.height, capped: g.classList.contains('capped'), marks: g.querySelectorAll('.break').length,
      label: label ? label.textContent : null, labelAbove: lb ? lb.bottom <= bar.top + 0.5 : null,
      labelInside: lb ? lb.left >= svg.left - 0.5 && lb.right <= svg.right + 0.5 : null,
      hitH: hit.height / svg.height, hitW: hit.width / svg.width, aria: g.getAttribute('aria-label') };
  });
}"""


def test_08_chart_cap(app):
    rows = [("2026-11-01", 200000, "housing", "etransfer", "", "Rent"), ("2026-11-03", 5000, "groceries", "credit", "", ""),
            ("2026-11-05", 2000, "dining", "credit", "", ""), ("2026-11-09", 500, "transit", "credit", "", ""),
            ("2026-11-15", 3500, "groceries", "credit", "", "")]
    app.seed(make_state(rows))
    app.tab("summary")
    assert app.ui.locator("#daily-bars").get_attribute("data-cap") == "6000"          # 1.2 x the second-highest day ($50)
    bars = {b["day"]: b for b in bars_of(app)}
    big, fifty, twenty, five = bars["2026-11-01"], bars["2026-11-03"], bars["2026-11-05"], bars["2026-11-09"]
    # the large bar: full height, break marker, amount labelled above it
    assert big["capped"] and big["marks"] == 1 and big["label"] == "$2,000"
    assert big["labelAbove"] and big["labelInside"]
    assert big["h"] == max(b["h"] for b in bars.values())
    assert app.ui.locator("#daily-bars .break").get_attribute("d").count("M") == 2    # two short lines
    # small bars are readable: $50 is most of the height, and they keep their proportions
    assert abs(fifty["h"] / big["h"] - 5000 / 6000) < 0.02
    assert abs(twenty["h"] / fifty["h"] - 0.4) < 0.02 and abs(bars["2026-11-15"]["h"] / fifty["h"] - 0.7) < 0.02
    assert fifty["h"] > 60 and twenty["h"] > 25 and five["h"] >= 6                     # pixels at 390 wide
    for day, b in bars.items():
        if day != "2026-11-01":
            assert not b["capped"] and b["marks"] == 0 and b["label"] is None
        assert abs(b["hitH"] - 1) < 0.01 and abs(b["hitW"] - 1 / 30) < 0.001         # full-height, full-column tap areas
    # labels unchanged, with the real amount
    assert big["aria"] == "Sun, Nov 1, $2,000.00" and fifty["aria"] == "Tue, Nov 3, $50.00"
    assert cents(app.ui.locator("#summary-total").inner_text()) == 211000
    # tapping the large bar still filters History to that day (also near its top, on the marker)
    app.ui.locator('#daily-bars .daybar[data-day="2026-11-01"] .hit').click()
    assert app.ui.locator("#f-day").inner_text() == "Sun, Nov 1 ×"
    assert cents(app.ui.locator("#results-total").inner_text()) == 200000 and app.ui.locator('.row[data-act="edit"]').count() == 1
    app.ui.locator("#f-clear").click()
    app.tab("summary")
    box = app.ui.locator('#daily-bars .daybar[data-day="2026-11-01"] .break').bounding_box()
    app.page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    assert app.ui.locator("#f-day").inner_text() == "Sun, Nov 1 ×"
    app.ui.locator("#f-clear").click()
    app.tab("summary")
    app.ui.locator('#daily-bars .daybar[data-day="2026-11-09"]').click()                # and a small one
    assert cents(app.ui.locator("#results-total").inner_text()) == 500
    app.ui.locator("#f-clear").click()

    # only one day with spending: that day sets the scale, nothing is capped
    app.seed(make_state(rows[:1]))
    app.tab("summary")
    assert app.ui.locator("#daily-bars").get_attribute("data-cap") == "200000"
    only = bars_of(app)
    assert len(only) == 1 and not only[0]["capped"] and only[0]["label"] is None and abs(only[0]["h"] - big["h"]) < 0.5
    # two equal top days: neither is capped
    app.seed(make_state([rows[0], ("2026-11-02", 200000, "housing", "etransfer", "", ""), rows[1]]))
    app.tab("summary")
    assert [b["capped"] for b in bars_of(app)] == [False, False, False]
    # a capped day at the end of the month keeps its label inside the chart; only the top day can ever be capped
    app.seed(make_state([("2026-11-30", 400000, "housing", "etransfer", "", ""), ("2026-11-29", 250000, "car", "credit", "", ""), rows[1]]))
    app.tab("summary")
    late = {b["day"]: b for b in bars_of(app)}
    assert late["2026-11-30"]["capped"] and not late["2026-11-29"]["capped"]
    assert late["2026-11-30"]["labelInside"] and late["2026-11-30"]["labelAbove"] and late["2026-11-30"]["label"] == "$4,000"
    assert app.console_errors == []


# ---------------------------------------------------------------- 9
def test_09_version(make_app):
    sw = source("sw.js")
    assert "const VERSION = '0.2.3';" in sw and "const CACHE = 'ds-' + VERSION;" in sw
    assert not re.search(r"0\.2\.[012]", sw + source("app.js"))
    app = make_app(service_workers="allow", cards=None)
    wait_cached(app.page, cache="ds-0.2.3")
    assert app.page.evaluate("caches.keys()") == ["ds-0.2.3"]
    app.tab("profile")
    assert app.ui.locator("#app-version").inner_text() == "Version 0.2.3"
    assert app.console_errors == []
