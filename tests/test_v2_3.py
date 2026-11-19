"""Acceptance tests from the v2.3 brief, section 7 (test numbers match the brief)."""
import re

from conftest import CAT, GROUPS, SAMPLE_ROWS, cents, make_card, make_state
from test_v1 import ADD_FITS, source
from test_v2 import CALGARY, STUB_GEO, drag, tap_inside, wait_cached

DEFAULT_CHIPS = ["Groceries", "Restaurant / Take-Out", "Gas / Diesel", "Shopping", "Transit", "Personal Care", "Medical"]
RED = {"light": "rgb(239, 68, 68)", "dark": "rgb(255, 107, 97)"}       # --missing (v2.4 light theme)
GREEN = "rgb(187, 247, 208)"                                           # Save, ready (light): pastel green...
GREEN_TEXT = "rgb(20, 83, 45)"                                         # ...with dark green text
CLEAR = "rgba(0, 0, 0, 0)"
ADD_STATE = """() => {
  const cs = (id) => getComputedStyle(document.getElementById(id));
  const save = document.getElementById('btn-save');
  return {
    amountOutline: [cs('amount').outlineColor, cs('amount').outlineStyle, cs('amount').outlineWidth],
    chipsOutline: [cs('chips').outlineColor, cs('chips').outlineStyle, cs('chips').outlineWidth],
    disabled: save.getAttribute('aria-disabled'), saveBg: cs('btn-save').backgroundColor, saveFg: cs('btn-save').color,
    saveText: save.textContent, hint: document.getElementById('save-hint').textContent,
    selected: Array.from(document.querySelectorAll('#chips .chip[aria-pressed="true"] .chip-name')).map((n) => n.textContent),
    chips: Array.from(document.querySelectorAll('#chips .chip-name')).map((n) => n.textContent),
    bg: getComputedStyle(document.body).backgroundColor,
  };
}"""


def luminance(rgb):
    r, g, b = [int(v) / 255 for v in re.findall(r"\d+", rgb)[:3]]
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def add_state(app):
    return app.page.evaluate(ADD_STATE)


# ---------------------------------------------------------------- 1
def test_01_fresh_add_screen(make_app):
    for scheme in ["light", "dark"]:
        app = make_app(scheme=scheme)
        st = add_state(app)
        assert st["amountOutline"] == [RED[scheme], "solid", "2px"]            # amount is missing
        assert st["chipsOutline"] == [RED[scheme], "solid", "2px"]             # category is missing
        assert contrast(RED[scheme], st["bg"]) >= 3                          # a non-text indicator
        assert st["disabled"] == "true" and st["saveText"] == "Save expense"
        assert st["hint"] == "Enter an amount and choose a category"
        r, g, b = [int(v) for v in re.findall(r"\d+", st["saveBg"])[:3]]
        assert max(r, g, b) - min(r, g, b) < 20                                # grey
        assert st["selected"] == [] and st["chips"] == DEFAULT_CHIPS + ["More"]
        # full width, at the bottom of the screen, just above the tab bar
        box = app.ui.locator("#btn-save").bounding_box()
        pad = app.ui.locator("#keypad").bounding_box()
        tab = app.ui.locator(".tabbar").bounding_box()
        assert box["width"] >= 390 - 24 - 1 and box["height"] >= 44
        assert pad["y"] + pad["height"] <= box["y"] and box["y"] + box["height"] <= tab["y"] and tab["y"] - (box["y"] + box["height"]) < 16
        hint = app.ui.locator("#save-hint").bounding_box()
        assert hint["y"] + hint["height"] <= box["y"] + 0.5                    # the hint is one line above it
        assert app.console_errors == []


def test_01b_fits_at_375x667(make_app):
    app = make_app(width=375, height=667)
    assert app.page.evaluate(ADD_FITS) == []
    app.type_amount("99999.99")
    app.chip("Restaurant / Take-Out").click()
    assert app.page.evaluate(ADD_FITS) == []
    sizes = app.page.evaluate("Array.from(document.querySelectorAll('.key, #chips .chip, #btn-save, #details-row')).map((n) => n.getBoundingClientRect().height)")
    assert min(sizes) >= 44


# ---------------------------------------------------------------- 2
def test_02_step_by_step(app):
    app.ui.locator("#details-row").click()
    app.ui.locator('#d-pay label:has-text("Cash")').click()
    app.ui.locator("#d-merchant").fill("Co-op")
    app.ui.locator("#d-done").click()
    # an amount removes its outline; the hint names what is left
    app.type_amount("12.34")
    st = add_state(app)
    assert st["amountOutline"][0] == CLEAR and st["chipsOutline"][0] == RED["light"]
    assert st["hint"] == "Choose a category" and st["disabled"] == "true"
    # tapping Save while it is disabled shakes only what is missing, and saves nothing
    app.ui.locator("#btn-save").click(force=True)
    assert app.page.evaluate("[document.getElementById('amount').classList.contains('shake'), document.getElementById('chips').classList.contains('shake')]") == [False, True]
    assert app.expenses() == [] and app.toast().count() == 0 and app.dialogs == []
    # selecting a chip removes the chip-area outline and turns Save green and enabled
    app.chip("Groceries").click()
    assert app.ui.locator("#btn-save").get_attribute("aria-disabled") == "false"     # enabled at once...
    app.page.wait_for_timeout(300)                                                   # ...the colour cross-fades (v2.4)
    st = add_state(app)
    assert st["chipsOutline"][0] == CLEAR and st["amountOutline"][0] == CLEAR
    assert st["disabled"] == "false" and st["saveBg"] == GREEN and st["saveFg"] == GREEN_TEXT and st["hint"] == ""
    assert contrast(GREEN, GREEN_TEXT) >= 4.5
    assert st["selected"] == ["Groceries"]
    chip = app.chip("Groceries")
    assert chip.get_attribute("aria-pressed") == "true" and chip.locator(".chip-check").inner_text() == "✓"
    accent = app.page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()")
    assert accent == "#0F766E" and chip.evaluate("(e) => [getComputedStyle(e).backgroundColor, getComputedStyle(e).color]") == [
        "rgb(204, 251, 241)", "rgb(17, 94, 89)"]
    assert app.expenses() == [] and app.toast().count() == 0                   # selecting does not save
    # the outline comes back if the amount is cleared, and goes again when refilled
    for _ in range(5):
        app.ui.locator('[data-key="back"]').click()
    st = add_state(app)
    assert st["amountOutline"][0] == RED["light"] and st["hint"] == "Enter an amount" and st["disabled"] == "true"
    assert st["selected"] == ["Groceries"]
    app.ui.locator("#btn-save").click(force=True)
    assert app.page.evaluate("[document.getElementById('amount').classList.contains('shake'), document.getElementById('chips').classList.contains('shake')]") == [True, False]
    app.type_amount("12.34")
    # Save: saved, toast with Undo, form reset with both outlines back
    app.save()
    assert app.toast().inner_text() == "Saved $12.34 · Groceries" and app.ui.locator(".toast-undo").is_visible()
    e = app.expenses()[0]
    assert (e["amountCents"], e["categoryId"], e["paymentMethodId"], e["merchant"], e["date"]) == (1234, "food.groceries", "cash", "Co-op", "2026-11-15")
    st = add_state(app)
    assert app.amount() == "$0" and st["selected"] == [] and st["disabled"] == "true"
    assert st["amountOutline"][0] == RED["light"] and st["chipsOutline"][0] == RED["light"]
    assert st["hint"] == "Enter an amount and choose a category"
    row = app.ui.locator("#details-row").inner_text()
    assert "Today · Cash" in row and "Add merchant or note" in row              # payment stays; merchant cleared
    app.ui.locator(".toast-undo").click()
    assert app.expenses() == []
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 3
def test_03_more_and_usual_select_without_saving(app):
    rows = [("2026-11-01", 500, "dining", "credit", "Tim Hortons", ""), ("2026-11-02", 500, "dining", "credit", "Tim Hortons", "")]
    app.seed(make_state(rows))
    chips = lambda: add_state(app)["chips"]
    start = chips()
    assert start == DEFAULT_CHIPS[1:2] + DEFAULT_CHIPS[0:1] + DEFAULT_CHIPS[2:] + ["More"]      # most used first, frozen for the session
    # More works with no amount yet; choosing closes the sheet and selects, nothing is saved
    app.ui.locator(".chip-more").click()
    app.ui.locator('#all-categories [data-pick="insurance.life-insurance"]').click()
    assert app.sheet_hidden() and len(app.expenses()) == 2 and app.toast().count() == 0
    st = add_state(app)
    # ...and it takes the seventh chip slot for this entry
    assert st["chips"] == start[:6] + ["Life Insurance", "More"] and st["selected"] == ["Life Insurance"]
    assert st["hint"] == "Enter an amount" and st["chipsOutline"][0] == CLEAR
    app.ui.locator(".chip-more").click()
    assert app.ui.locator('#all-categories [data-pick="insurance.life-insurance"]').get_attribute("aria-pressed") == "true"
    app.ui.locator('#all-categories [data-pick="recreation.club-memberships"]').click()        # only one category at a time
    assert chips() == start[:6] + ["Club Memberships", "More"] and add_state(app)["selected"] == ["Club Memberships"]
    app.type_amount("45")
    assert add_state(app)["disabled"] == "false" and len(app.expenses()) == 2
    app.save()
    assert app.toast().inner_text() == "Saved $45.00 · Club Memberships"
    assert [e for e in app.expenses() if e["amountCents"] == 4500][0]["categoryId"] == "recreation.club-memberships"
    assert chips() == start and add_state(app)["selected"] == []               # saved: the frozen chip order is back
    # a More pick that is already a chip just selects that chip
    app.ui.locator(".chip-more").click()
    app.ui.locator('#all-categories [data-pick="misc.shopping"]').click()
    assert chips() == start and add_state(app)["selected"] == ["Shopping"]
    # clearing a borrowed slot brings the seventh chip back
    app.ui.locator(".chip-more").click()
    app.ui.locator('#all-categories [data-pick="misc.pets"]').click()
    assert chips()[6] == "Pets"
    app.chip("Pets").click()
    assert chips() == start and add_state(app)["selected"] == []

    # the Usual pill selects too
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-merchant").fill("tim hortons")
    app.ui.locator("#d-done").click()
    pill = app.ui.locator("#usual-pill")
    assert pill.inner_text() == "Usual: 🍔 Restaurant / Take-Out" and pill.get_attribute("aria-pressed") == "false"
    pill.click()
    assert app.ui.locator("#usual-pill").get_attribute("aria-pressed") == "true"
    assert add_state(app)["selected"] == ["Restaurant / Take-Out"] and len(app.expenses()) == 3          # selected, not saved
    app.type_amount("3.50")
    app.save()
    assert app.toast().inner_text() == "Saved $3.50 · Restaurant / Take-Out" and len(app.expenses()) == 4
    assert app.ui.locator("#usual-pill").count() == 0 and add_state(app)["selected"] == []
    assert app.console_errors == []


# ---------------------------------------------------------------- 4
def test_04_deselect(app):
    app.type_amount("8")
    app.chip("Transit").click()
    assert add_state(app)["disabled"] == "false"
    app.chip("Transit").click()                                                 # again: deselected
    st = add_state(app)
    assert st["selected"] == [] and st["disabled"] == "true" and st["hint"] == "Choose a category"
    assert st["chipsOutline"][0] == RED["light"] and app.chip("Transit").get_attribute("aria-pressed") == "false"
    app.ui.locator("#btn-save").click(force=True)
    assert app.expenses() == []
    # only one category can be selected
    app.chip("Transit").click()
    app.chip("Shopping").click()
    assert add_state(app)["selected"] == ["Shopping"]
    app.save()
    assert app.expenses()[0]["categoryId"] == "misc.shopping"
    # a hardware Enter key saves too, when the entry is ready
    app.page.keyboard.type("6.5")
    app.chip("Transit").click()
    app.page.evaluate("document.activeElement.blur()")
    app.page.keyboard.press("Enter")
    assert sorted(e["amountCents"] for e in app.expenses()) == [650, 800]


# ---------------------------------------------------------------- 5
def test_05_automatic_location_with_save_button(make_app):
    # the fix arrives while the form is being filled: saved with the expense
    a = make_app(geolocation=CALGARY)
    a.seed(make_state([], auto_location=True))
    a.type_amount("5")
    a.ui.locator('#details-row:has-text("📍")').wait_for()
    a.chip("Transit").click()
    assert a.expenses() == []
    a.page.wait_for_timeout(300)
    a.save()
    e = a.expenses()[0]
    assert e["location"]["lat"] == 51.04471 and e["location"]["accuracyM"] == 25
    # the fix arrives after Save: the save did not wait, and the fix is attached to it
    app = make_app(init_scripts=[STUB_GEO])
    app.seed(make_state([], auto_location=True))
    app.type_amount("7")
    assert app.page.evaluate("window.__geo.length") == 1
    app.chip("Groceries").click()
    assert app.page.evaluate("window.__geo.length") == 1 and app.expenses() == []          # selecting neither saves nor asks again
    app.save()
    assert app.toast().inner_text() == "Saved $7.00 · Groceries" and app.expenses()[0]["location"] is None
    app.page.evaluate("window.__geo[0].ok({ coords: { latitude: 53.5461234, longitude: -113.4937012, accuracy: 12.4 } })")
    loc = app.expenses()[0]["location"]
    assert (loc["lat"], loc["lng"], loc["accuracyM"]) == (53.54612, -113.4937, 12)
    assert "📍" not in app.ui.locator("#details-row").inner_text()
    assert app.console_errors == [] and a.console_errors == []


# ---------------------------------------------------------------- 6
def test_06_quick_repeat_stays_one_tap(app):
    rows = [("2026-11-14", 6230, "gas", "credit", "Petro-Canada", "Fill up"), ("2026-11-13", 475, "dining", "debit", "Tim Hortons", "")]
    app.seed(make_state(rows))
    # Recent → Again: saved at once, no Save button involved
    app.ui.locator("#btn-recent").click()
    app.ui.locator('#recent-list [data-again="seed-000"]').click()
    assert app.sheet_hidden() and app.toast().inner_text() == "Saved $62.30 · Gas / Diesel" and len(app.expenses()) == 3
    assert add_state(app)["disabled"] == "true" and add_state(app)["selected"] == []
    app.ui.locator(".toast-undo").click()
    assert len(app.expenses()) == 2
    # a half-filled form is left alone by a repeat
    app.type_amount("9")
    app.chip("Shopping").click()
    app.ui.locator("#btn-recent").click()
    app.ui.locator('#recent-list [data-again="seed-001"]').click()
    assert len(app.expenses()) == 3 and app.amount() == "$9" and add_state(app)["selected"] == ["Shopping"]
    app.ui.locator(".toast-undo").click()
    # History swipe right → Again
    app.tab("history")
    drag(app, app.ui.locator('.row[data-id="seed-001"]'), 130)
    assert app.toast().inner_text() == "Saved $4.75 · Restaurant / Take-Out" and len(app.expenses()) == 3
    new = [e for e in app.expenses() if not e["id"].startswith("seed-")][0]
    assert new["date"] == "2026-11-15" and new["merchant"] == "Tim Hortons"
    app.ui.locator(".toast-undo").click()
    # Log again today in the Edit sheet
    app.page.wait_for_timeout(400)
    app.ui.locator('.row[data-id="seed-000"]').click()
    app.ui.locator("#e-again").click()
    assert app.toast().inner_text() == "Saved $62.30 · Gas / Diesel" and len(app.expenses()) == 3
    assert app.console_errors == []


# ---------------------------------------------------------------- 7
def bank_state():
    cards = [make_card("td-1", "TD Cash Back Visa", issuer="TD", catalogue_id=None),
             make_card("td-2", "TD Access Card", kind="debit", issuer="TD", networks=("Interac",), colour="green", archived=True),
             make_card("amex-1", "American Express Cobalt Card", issuer="American Express", nickname="Cobalt", colour="rose")]
    rows = [("2026-11-10", 1000, "groceries", "credit", "Co-op", "", "td-1"), ("2026-10-05", 2000, "dining", "credit", "Cafe", "", "td-1"),
            ("2026-11-11", 4000, "groceries", "debit", "Superstore", "", "td-2"), ("2026-11-12", 8000, "dining", "credit", "Bistro", "", "amex-1"),
            ("2026-11-13", 16000, "groceries", "cash", "Market", "", None), ("2026-09-01", 32000, "housing", "etransfer", "", "Rent", None)]
    return make_state(rows, cards=cards)


def test_07_filter_by_institution(app):
    app.seed(bank_state())
    app.tab("history")
    total = lambda: cents(app.ui.locator("#results-total").inner_text())
    shown = lambda: sorted(app.ui.locator('.row[data-act="edit"]').evaluate_all("(els) => els.map((e) => e.dataset.id)"))
    label = lambda: app.ui.locator("#f-card").inner_text()
    assert label() == "Card"
    app.ui.locator("#f-card").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Card or institution"
    # institutions with their badge and name, their cards beneath (archived ones too), Cash & other last
    assert [t.strip().split("\n")[0] for t in app.ui.locator("#fk-list .row").all_inner_texts()] == [
        "American Express", "Cobalt", "TD", "TD Cash Back Visa", "TD Access Card", "Cash & other"]
    assert app.ui.locator("#fk-list .group-check .ibadge").count() == 2
    assert "Archived" in app.ui.locator('#fk-list .item-check:has-text("TD Access Card")').inner_text()
    td = app.ui.locator('#fk-list input[data-inst="td"]')
    # TD: the entries on both TD cards
    td.check()
    assert app.ui.locator('#fk-list input[data-card="td"]:checked').count() == 2
    assert label() == "TD" and app.ui.locator("#f-card").get_attribute("aria-pressed") == "true"
    assert total() == 7000 and shown() == ["seed-000", "seed-001", "seed-002"]
    assert app.ui.locator("#results-count").inner_text() == "3 results across all months"
    # one TD card narrows it
    app.ui.locator('#fk-list .item-check:has-text("TD Access Card")').click()
    assert td.evaluate("(e) => [e.checked, e.indeterminate]") == [False, True]
    assert label() == "TD Cash Back Visa" and total() == 3000 and shown() == ["seed-000", "seed-001"]
    # Cash & other alone: only entries without a card
    app.ui.locator("#fk-none").click()
    assert label() == "Card" and app.ui.locator("#f-clear").count() == 0
    app.ui.locator("#fk-list .cash-check").click()
    assert label() == "Cash & other" and total() == 48000 and shown() == ["seed-004", "seed-005"]
    # combinations across institutions, and the chip labels
    td.check()
    assert label() == "3 selected" and total() == 55000
    app.ui.locator("#fk-list .cash-check").click()
    app.ui.locator('#fk-list input[data-inst="american express"]').check()
    assert label() == "3 selected" and total() == 15000 and shown() == ["seed-000", "seed-001", "seed-002", "seed-003"]
    td.uncheck()
    assert label() == "Cobalt" and total() == 8000                             # one card: its display name
    td.check()
    app.ui.locator('#fk-list .item-check:has-text("Cobalt")').click()
    app.ui.locator("#fk-done").click()
    assert app.sheet_hidden() and label() == "TD" and total() == 7000
    # it combines with search, category and the other filters
    app.ui.locator("#h-search").fill("co")
    assert shown() == ["seed-000"] and total() == 1000
    app.ui.locator("#h-search").fill("")
    app.ui.locator("#f-category").click()
    app.ui.locator('#fc-list label:has-text("Groceries")').click()
    app.ui.locator("#fc-done").click()
    assert shown() == ["seed-000", "seed-002"] and total() == 5000
    app.ui.locator("#f-card").click()
    assert app.ui.locator('#fk-list input[data-card="td"]:checked').count() == 2            # the sheet reopens with the selection
    app.ui.locator("#fk-list .cash-check").click()
    app.ui.locator("#fk-done").click()
    assert shown() == ["seed-000", "seed-002", "seed-004"] and total() == 21000 and label() == "3 selected"
    app.ui.locator("#f-clear").click()
    assert label() == "Card" and app.ui.locator("#month-label").inner_text() == "November 2026"
    # Summary → By card still lands on one card for the month
    app.tab("summary")
    app.ui.locator('#by-card .cat-row:has-text("TD Cash Back Visa")').click()
    assert label() == "TD Cash Back Visa" and total() == 1000 and "November 2026" in app.ui.locator("#f-month").inner_text()
    assert app.console_errors == []


def test_07b_cards_added_by_hand_group_by_typed_issuer(app):
    cards = [make_card("h-1", "Member Card", issuer="Corner CU"), make_card("h-2", "Savings Card", kind="debit", issuer="corner cu "),
             make_card("h-3", "Mystery Card", issuer=""), make_card("m-1", "Maple Rewards Visa", catalogue_id="maple-rewards-visa")]
    rows = [("2026-11-10", 100, "groceries", "credit", "", "", "h-1"), ("2026-11-10", 200, "groceries", "debit", "", "", "h-2"),
            ("2026-11-10", 400, "groceries", "credit", "", "", "h-3"), ("2026-11-10", 800, "groceries", "credit", "", "", "m-1")]
    app.seed(make_state(rows, cards=cards))
    app.tab("history")
    app.ui.locator("#f-card").click()
    assert [t.strip().split("\n")[0] for t in app.ui.locator("#fk-list .group-check").all_inner_texts()] == ["Corner CU", "Maple Bank", "Other cards"]
    app.ui.locator('#fk-list input[data-inst="corner cu"]').check()
    assert app.ui.locator("#f-card").inner_text() == "Corner CU" and cents(app.ui.locator("#results-total").inner_text()) == 300
    app.ui.locator("#fk-none").click()
    app.ui.locator('#fk-list input[data-inst=""]').check()
    assert app.ui.locator("#f-card").inner_text() == "Mystery Card" and cents(app.ui.locator("#results-total").inner_text()) == 400


# ---------------------------------------------------------------- 8
def colour_rows():
    one = ["housing", "debt.student-loan", "phone", "groceries", "gas", "travel", "shopping", "insurance.life-insurance"]   # one per group, in group order
    nov = [("2026-11-05", (8 - i) * 1000, c, "credit", "", "") for i, c in enumerate(one)]      # Housing largest
    octo = [("2026-10-05", (i + 1) * 1000, c, "credit", "", "") for i, c in enumerate(one)]     # Insurance largest: ranks reversed
    return nov + octo


GROUP_COLOURS = """() => {
  const card = getComputedStyle(document.getElementById('by-group')).backgroundColor;
  const out = {};
  document.querySelectorAll('#donut .slice').forEach((s) => {
    const bar = document.querySelector('#by-group .grp[data-group="' + s.dataset.group + '"] .grp-row .bar i');
    const rgb = (text) => (text.match(/rgba?[(][^)]*[)]/) || [''])[0];
    out[s.dataset.group] = { slice: getComputedStyle(s).fill, bar: getComputedStyle(bar).backgroundColor,
      sliceEdge: getComputedStyle(s).stroke, barEdge: rgb(getComputedStyle(bar).boxShadow) };
  });
  return { card, groups: out, order: Array.from(document.querySelectorAll('#donut .slice')).map((s) => s.dataset.group),
    cardBar: document.querySelector('#by-card .bar i') ? getComputedStyle(document.querySelector('#by-card .bar i')).backgroundColor : null };
}"""


def test_08_group_colours_match(make_app):
    seen = {}
    for scheme in ["light", "dark"]:
        app = make_app(scheme=scheme)
        app.seed(make_state(colour_rows(), cards=[make_card("card-a", "Maple Rewards Visa")]))
        app.tab("summary")
        nov = app.page.evaluate(GROUP_COLOURS)
        assert nov["order"] == [g[0] for g in GROUPS] and len(nov["groups"]) == 8
        for group, c in nov["groups"].items():
            assert c["slice"] == c["bar"], (scheme, group)                      # the bar has the fill of its slice
            if scheme == "light":                                               # ...and, in the pastel theme, its edge
                assert c["sliceEdge"] == c["barEdge"] != c["bar"], (group, c)
                assert contrast(c["barEdge"], nov["card"]) >= 3, (group, c["barEdge"])
            else:                                                               # dark, as in 0.2.3: the fill itself carries it
                assert c["barEdge"] == c["bar"] and contrast(c["bar"], nov["card"]) >= 3, (group, c)
        assert len({c["bar"] for c in nov["groups"].values()}) == 8             # eight distinct colours
        # another month, where the ranks are reversed: every group keeps its colour
        app.ui.locator('[data-act="month"][data-delta="-1"]').click()
        octo = app.page.evaluate(GROUP_COLOURS)
        assert octo["order"] == [g[0] for g in reversed(GROUPS)]
        assert octo["groups"] == nov["groups"]
        # and in a range view
        app.ui.locator('#range-seg [data-range="3"]').click()
        assert app.page.evaluate(GROUP_COLOURS)["groups"] == nov["groups"]
        # the group view: header accent and item bars in the group's colour; opened items in By group too
        tap_inside(app, app.ui.locator('#donut .slice[data-group="food"]'))
        view = app.page.evaluate("[getComputedStyle(document.getElementById('group-view')).borderTopColor, getComputedStyle(document.querySelector('#group-items .bar i')).backgroundColor]")
        food = nov["groups"]["food"]
        assert view == [food["barEdge"] if scheme == "light" else food["bar"], food["bar"]]
        app.ui.locator("#group-back").click()
        app.ui.locator('#by-group .grp-row:has-text("Recreation")').click()
        assert app.ui.locator("#by-group .item-row .bar i").evaluate("(e) => getComputedStyle(e).backgroundColor") == nov["groups"]["recreation"]["bar"]
        seen[scheme] = nov["groups"]
        app.close()
    assert all(seen["light"][g] != seen["dark"][g] for g in seen["light"])    # a distinct pair for each theme


def test_08b_other_bars_unchanged(app):
    rows = [("2026-11-05", 1000, "groceries", "credit", "", "", "card-a")]
    app.seed(make_state(rows, cards=[make_card("card-a", "Maple Rewards Visa")]))
    app.tab("summary")
    app.page.wait_for_timeout(400)
    got = app.page.evaluate("[getComputedStyle(document.querySelector('#by-card .bar i')).backgroundColor, getComputedStyle(document.querySelector('#daily-bars .dbar')).fill]")
    assert got == ["rgb(15, 118, 110)", "rgb(153, 246, 228)"]                  # By card: accent. Day bars: pastel teal


# ---------------------------------------------------------------- 9
def month_total(prefix):
    return sum(r[1] for r in SAMPLE_ROWS if r[0].startswith(prefix))


MONTH_BARS = """() => Array.from(document.querySelectorAll('#monthly-bars .monthbar')).map((g) => ({
  month: g.dataset.month, cents: Number(g.dataset.cents), aria: g.getAttribute('aria-label'), tab: g.getAttribute('tabindex'), role: g.getAttribute('role'),
  h: g.querySelector('.mbar').getBoundingClientRect().height, texts: Array.from(g.querySelectorAll('text')).map((t) => t.textContent),
  current: g.classList.contains('current') }))"""


def by_group(app):
    return dict(zip(app.ui.locator("#by-group .grp-row .name").all_inner_texts(),
                    [cents(t) for t in app.ui.locator("#by-group .grp-row .amt").all_inner_texts()]))


def test_09_time_ranges(app):
    cards = [make_card("card-a", "Maple Rewards Visa")]
    st = make_state(SAMPLE_ROWS, cards=cards)
    for e in st["expenses"]:
        if e["date"] in ("2026-11-14", "2026-10-28"):
            e["cardId"] = "card-a"
    app.seed(st)
    app.tab("summary")
    seg = lambda: app.ui.locator("#range-seg .seg-btn").evaluate_all("(els) => els.map((e) => [e.textContent, e.getAttribute('aria-pressed')])")
    assert seg() == [["Month", "true"], ["3 months", "false"], ["12 months", "false"]]        # Month is the default
    assert app.ui.locator("#daily-bars").count() == 1 and app.ui.locator("#tax-card").count() == 1 and app.ui.locator("#month-label").count() == 1
    nov, octo = month_total("2026-11"), month_total("2026-10")
    # the By group totals of each month, to add up later
    per_month = []
    for _ in range(3):
        per_month.append(by_group(app) if app.ui.locator("#by-group").count() else {})
        app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    for _ in range(3):
        app.ui.locator('[data-act="month"][data-delta="1"]').click()

    # ---- 3 months
    app.ui.locator('#range-seg [data-range="3"]').click()
    assert seg()[1] == ["3 months", "true"]
    assert app.ui.locator("#range-label").inner_text() == "Sep – Nov 2026"
    total3 = nov + octo
    assert cents(app.ui.locator("#summary-total").inner_text()) == total3
    avg = app.ui.locator("#range-avg").inner_text()
    assert avg.endswith("a month on average · includes this month so far") and cents(avg.split(" ")[0]) == round(total3 / 3)
    app.page.wait_for_timeout(400)
    bars = app.page.evaluate(MONTH_BARS)
    assert [(b["month"], b["cents"]) for b in bars] == [("2026-09", 0), ("2026-10", octo), ("2026-11", nov)]      # 3 bars, correct totals
    assert [b["aria"] for b in bars] == ["September 2026, $0.00", "October 2026, $542.50", f"November 2026, ${nov / 100:,.2f}"]
    assert all(b["tab"] == "0" and b["role"] == "button" for b in bars)
    assert [b["texts"] for b in bars] == [["Sep"], ["Oct"], ["Nov", "so far"]] and [b["current"] for b in bars] == [False, False, True]
    assert bars[0]["h"] == 0 and 0 < bars[1]["h"] < bars[2]["h"]                 # an empty month: zero height, still labelled
    # donut, By group and By card cover the whole range
    assert sum(int(c) for c in app.ui.locator("#donut .slice").evaluate_all("(els) => els.map((e) => e.dataset.cents)")) == total3
    assert cents(app.ui.locator("#donut-total").text_content()) == total3
    want = {}
    for month in per_month:
        for name, amount in month.items():
            want[name] = want.get(name, 0) + amount
    assert by_group(app) == want and sum(want.values()) == total3                 # equals the sum over its months
    by_card = dict(zip(app.ui.locator("#by-card .name").all_inner_texts(), [cents(t) for t in app.ui.locator("#by-card .amt").all_inner_texts()]))
    assert by_card == {"Maple Rewards Visa": 6230 + 3899 + 7250, "Cash & other": total3 - (6230 + 3899 + 7250)}
    # the day chart, Tax time and the month switcher are hidden in range views
    assert app.ui.locator("#daily-bars").count() == 0 and app.ui.locator("#tax-card").count() == 0
    assert app.ui.locator("#month-label").count() == 0 and app.ui.locator('[data-act="month"]').count() == 0
    # the choice lasts for the session
    app.tab("add")
    app.tab("summary")
    assert seg()[1] == ["3 months", "true"] and app.ui.locator("#range-label").inner_text() == "Sep – Nov 2026"
    # a By card row filters History over the range
    app.ui.locator('#by-card .cat-row:has-text("Maple Rewards Visa")').click()
    assert app.ui.locator("#f-range").inner_text() == "Sep – Nov 2026 ×" and cents(app.ui.locator("#results-total").inner_text()) == 6230 + 3899 + 7250
    app.ui.locator("#f-clear").click()

    # ---- 12 months
    app.tab("summary")
    app.ui.locator('#range-seg [data-range="12"]').click()
    assert app.ui.locator("#range-label").inner_text() == "Dec 2025 – Nov 2026"
    app.page.wait_for_timeout(400)
    bars = app.page.evaluate(MONTH_BARS)
    months = ["2025-12"] + [f"2026-{m:02d}" for m in range(1, 12)]
    assert [b["month"] for b in bars] == months and len(bars) == 12
    assert [b["cents"] for b in bars] == [month_total(m) for m in months]
    assert bars[0]["cents"] == 12000 and bars[3]["cents"] == 9900 and bars[0]["aria"] == "December 2025, $120.00"
    assert [b["texts"][0] for b in bars] == ["Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
    total12 = sum(month_total(m) for m in months)
    assert cents(app.ui.locator("#summary-total").inner_text()) == total12
    assert cents(app.ui.locator("#range-avg").inner_text().split(" ")[0]) == round(total12 / 12)
    assert sum(by_group(app).values()) == total12
    # the group view works over the range; an item opens History for that item over the range
    tap_inside(app, app.ui.locator('#donut .slice[data-group="misc"]'))
    medical = 18500 + 9900 + 12000
    assert "of Dec 2025 – Nov 2026" in app.ui.locator("#group-share").inner_text()
    items = dict(zip(app.ui.locator("#group-items .name").all_inner_texts(), [cents(t) for t in app.ui.locator("#group-items .amt").all_inner_texts()]))
    assert items["Medical"] == medical and items["Childcare"] == 42000
    assert app.ui.locator("#monthly-bars").count() == 0 and app.ui.locator("#tax-card").count() == 0
    app.ui.locator('#group-items .cat-row:has-text("Medical")').click()
    assert app.ui.locator('.tab[data-tab="history"]').get_attribute("aria-current") == "page"
    assert app.ui.locator("#f-category").inner_text() == "Medical" and app.ui.locator("#f-range").inner_text() == "Dec 2025 – Nov 2026 ×"
    assert app.ui.locator("#f-month").count() == 0 and cents(app.ui.locator("#results-total").inner_text()) == medical
    assert app.ui.locator(".month-group").evaluate_all("(els) => els.map((e) => e.dataset.month)") == ["2026-11", "2026-03", "2025-12"]
    app.ui.locator("#f-range").click()                                            # the range chip can be removed
    assert app.ui.locator("#f-range").count() == 0 and app.ui.locator("#f-category").inner_text() == "Medical"
    app.ui.locator("#f-clear").click()
    # in the 3-month view the same item covers only those months
    app.tab("summary")
    app.ui.locator('#range-seg [data-range="3"]').click()
    app.ui.locator('#by-group .grp-row:has-text("Miscellaneous")').click()
    app.ui.locator('#by-group .item-row:has-text("Medical")').click()
    assert app.ui.locator("#f-range").inner_text() == "Sep – Nov 2026 ×" and cents(app.ui.locator("#results-total").inner_text()) == 18500
    app.ui.locator("#f-clear").click()

    # ---- tapping a bar opens that month, in Month view
    app.tab("summary")
    app.ui.locator('#monthly-bars .monthbar[data-month="2026-10"] .hit').click()
    assert seg()[0] == ["Month", "true"] and app.ui.locator("#month-label").inner_text() == "October 2026"
    assert cents(app.ui.locator("#summary-total").inner_text()) == octo
    assert app.ui.locator("#daily-bars").count() == 1 and app.ui.locator("#tax-card").count() == 1
    # by keyboard too, including an empty month
    app.ui.locator('#range-seg [data-range="12"]').click()
    app.ui.locator('#monthly-bars .monthbar[data-month="2026-03"]').focus()
    app.page.keyboard.press("Enter")
    assert app.ui.locator("#month-label").inner_text() == "March 2026" and cents(app.ui.locator("#summary-total").inner_text()) == 9900
    app.ui.locator('#range-seg [data-range="12"]').click()
    app.ui.locator('#monthly-bars .monthbar[data-month="2026-01"] .hit').click()
    assert app.ui.locator("#month-label").inner_text() == "January 2026" and "No expenses in January 2026." in app.ui.locator(".empty").inner_text()
    assert app.console_errors == []


def test_09b_range_with_no_spending(app):
    app.tab("summary")
    app.ui.locator('#range-seg [data-range="12"]').click()
    assert app.ui.locator("#range-label").inner_text() == "Dec 2025 – Nov 2026"
    assert "No expenses in Dec 2025 – Nov 2026." in app.ui.locator(".empty").inner_text()
    assert cents(app.ui.locator("#summary-total").inner_text()) == 0 and app.console_errors == []


# ---------------------------------------------------------------- 10
def test_10_version(make_app):
    sw = source("sw.js")
    assert "const VERSION = '0.2.4';" in sw and "const CACHE = 'ds-' + VERSION;" in sw
    assert "version: '0.2.4'," in source("app.js") and not re.search(r"0\.2\.[0123]\b", sw + source("app.js"))
    app = make_app(service_workers="allow", cards=None, tax=None)
    wait_cached(app.page, cache="ds-0.2.4")
    assert app.page.evaluate("caches.keys()") == ["ds-0.2.4"]
    app.tab("profile")
    assert app.ui.locator("#app-version").inner_text() == "Version 0.2.4"
    assert app.console_errors == []
