"""Acceptance tests from the v2.4 brief, section 7 (test numbers match the brief)."""
import json
import os
import re

import pytest

from conftest import FIXTURE_TAX, ROOT, cents, make_state, names_the_template
from test_v1 import CAPTURE_CLIPBOARD, copied_csv, source
from test_v2 import tap_inside, wait_cached

TEAL_OLD = "#5AD1C6"
PAY_4000 = {"earners": [], "province": None, "takeHomeOverrideCents": 400000, "taxYear": 2026, "updatedAt": "2026-11-01T12:00:00.000Z"}
# Test 6 data: October 2026
OCTOBER = [("2026-10-01", 150000, "housing", "etransfer", "", "Rent"), ("2026-10-05", 60000, "groceries", "credit", "", ""),
           ("2026-10-09", 30000, "dining", "credit", "", ""), ("2026-10-12", 30000, "gas", "credit", "", ""),
           ("2026-10-20", 60000, "travel", "credit", "", "")]
NOVEMBER = [("2026-11-03", 5000, "groceries", "credit", "", "")]


def state_with(rows, pay=None, skipped=False):
    st = make_state(rows)
    st["settings"]["pay"] = pay
    st["settings"]["paySkipped"] = skipped
    return st


def luminance(colour):
    if colour.startswith("#"):
        rgb = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    else:
        rgb = [int(v) / 255 for v in re.findall(r"\d+", colour)[:3]]
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(rgb[0]) + 0.7152 * lin(rgb[1]) + 0.0722 * lin(rgb[2])


def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def css_var(app, name):
    return app.page.evaluate("(n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim()", name)


def open_october(app):
    app.tab("summary")
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert app.ui.locator("#month-label").inner_text() == "October 2026"


def open_report(app):
    app.ui.locator("#btn-compare").click()
    app.ui.locator("#report").wait_for()


def card_kinds(app):
    return app.ui.locator("#report .rp-card").evaluate_all("(els) => els.map((e) => e.dataset.kind + (e.dataset.group ? ':' + e.dataset.group : ''))")


def card(app, kind, group=None):
    return app.ui.locator(f'#report .rp-card[data-kind="{kind}"]' + (f'[data-group="{group}"]' if group else ""))


def current_card(app):
    return app.page.evaluate("""() => { const cards = Array.from(document.querySelectorAll('#report .rp-card'));
      const on = cards.filter((c) => !c.inert); return on.length === 1 ? cards.indexOf(on[0]) : -1; }""")


# ---------------------------------------------------------------- 1
def test_01_motion_does_not_block(make_app):
    app = make_app()
    assert app.page.evaluate("[document.getElementById('fx-layer').getAttribute('aria-hidden'), document.getElementById('fx-layer').inert, getComputedStyle(document.getElementById('fx-layer')).pointerEvents]") == ["true", True, "none"]
    z = app.page.evaluate("['sheet-root', 'fx-layer', 'toast-region'].map((id) => Number(getComputedStyle(document.getElementById(id)).zIndex))")
    assert z[0] < z[1] < z[2]                                   # above the app and sheets, below the toast
    # a sheet opens with an overshoot of about 260 ms
    app.ui.locator("#details-row").click()
    assert app.page.evaluate("[getComputedStyle(document.querySelector('.sheet')).animationName, getComputedStyle(document.querySelector('.sheet')).animationDuration]") == ["rise", "0.26s"]
    # close it and tap a chip in the same instant: closing is synchronous and the copy is not in the way
    got = app.page.evaluate("""() => {
      const t0 = performance.now();
      document.getElementById('d-done').click();
      const ghost = document.querySelector('#fx-layer .fx-ghost');
      const out = { ghost: !!ghost, pointer: ghost ? getComputedStyle(ghost).pointerEvents : null,
        sheetHidden: document.getElementById('sheet-root').hidden, appInert: document.getElementById('app').inert,
        idsInGhost: ghost ? ghost.querySelectorAll('[id]').length : -1 };
      document.querySelector('.chip[data-cat="food.groceries"]').click();
      out.selected = document.querySelector('.chip[data-cat="food.groceries"]').getAttribute('aria-pressed');
      out.ms = performance.now() - t0;
      return out;
    }""")
    assert got["ghost"] and got["pointer"] == "none" and got["sheetHidden"] and got["appInert"] is False
    assert got["selected"] == "true" and got["ms"] < 50 and got["idsInGhost"] == 0
    app.page.wait_for_timeout(400)
    assert app.ui.locator("#fx-layer .fx-ghost").count() == 0           # gone within 400 ms
    # the same with real taps, one straight after the other
    app.chip("Groceries").click()                                       # deselect
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-done").click()
    app.chip("Transit").click()
    assert app.chip("Transit").get_attribute("aria-pressed") == "true"
    assert app.chip("Transit").evaluate("(e) => getComputedStyle(e).animationName") == "chip-pop"
    # opening another sheet removes a copy that is still sliding away
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-done").click()
    app.ui.locator(".chip-more").click()
    assert app.ui.locator("#fx-layer .fx-ghost").count() == 0 and app.ui.locator("#cp-tiles").is_visible()
    app.page.keyboard.press("Escape")

    # select a chip and press Save at once: the expense saves; a burst is drawn in the layer
    app.type_amount("12")
    saved = app.page.evaluate("""() => {
      document.querySelector('.chip[data-cat="food.groceries"]').click();
      document.getElementById('btn-save').click();
      return { burst: document.querySelectorAll('#fx-layer .fx-burst').length, amount: document.getElementById('amount').textContent,
        toast: document.querySelector('#toast-region .toast-text').textContent };
    }""")
    assert saved == {"burst": 1, "amount": "$0", "toast": "Saved $12.00 · Groceries"}
    assert len(app.expenses()) == 1
    assert app.ui.locator(".toast").evaluate("(e) => getComputedStyle(e).animationName") == "drop"
    app.page.wait_for_timeout(600)
    assert app.ui.locator("#fx-layer .fx-burst").count() == 0
    # the toast slides out over its last moments and is gone on time
    app.page.wait_for_timeout(4300)
    assert "out" in app.ui.locator(".toast").get_attribute("class")
    app.page.wait_for_timeout(250)
    assert app.ui.locator(".toast").count() == 0

    # right after Summary renders, the total already holds the final value (the count-up is a separate layer)
    total = app.page.evaluate("""() => {
      document.querySelector('.tab[data-tab="summary"]').click();
      const t = document.getElementById('summary-total'), layer = document.querySelector('.count-layer');
      return { text: t.textContent, counting: t.classList.contains('counting'), colour: getComputedStyle(t).color,
        layer: !!layer, layerHidden: layer && layer.getAttribute('aria-hidden'), view: document.getElementById('view').classList.contains('view-in'),
        page: document.querySelector('#view .page').classList.contains('summary-in') };
    }""")
    assert total == {"text": "$12.00", "counting": True, "colour": "rgba(0, 0, 0, 0)", "layer": True, "layerHidden": "true", "view": True, "page": True}
    assert app.ui.locator("#summary-total").inner_text() == "$12.00"
    app.page.wait_for_timeout(700)
    assert app.ui.locator(".count-layer").count() == 0 and "counting" not in app.ui.locator("#summary-total").get_attribute("class")
    # a re-render that is not an arrival does not replay it
    app.ui.locator('#by-group .grp-row').first.click()
    assert app.ui.locator(".count-layer").count() == 0 and app.ui.locator(".page.summary-in").count() == 0
    # History: rows slide in when a filter chip changes, not while typing
    app.tab("history")
    app.ui.locator("#h-search").fill("zz")
    app.ui.locator("#h-search").fill("")
    assert app.ui.locator(".swipe.row-in").count() == 0
    app.ui.locator("#f-loc").click()
    app.ui.locator("#f-loc").click()
    assert app.ui.locator(".swipe.row-in").count() == 1
    assert app.console_errors == []


def test_01b_reduced_motion(make_app):
    app = make_app(reduced_motion="reduce")
    app.seed(state_with(OCTOBER, pay=PAY_4000))
    app.ui.locator("#details-row").click()
    assert app.page.evaluate("getComputedStyle(document.querySelector('.sheet')).animationName") == "none"
    app.ui.locator("#d-done").click()
    assert app.ui.locator("#fx-layer > *").count() == 0                 # no exit copy
    app.type_amount("5")
    app.chip("Groceries").click()
    assert app.chip("Groceries").evaluate("(e) => getComputedStyle(e).animationName") == "none"
    app.save()
    assert app.ui.locator("#fx-layer > *").count() == 0                 # no burst
    assert app.ui.locator(".toast").evaluate("(e) => getComputedStyle(e).animationName") == "none"
    app.ui.locator(".toast-undo").click()
    open_october(app)
    assert app.ui.locator(".count-layer").count() == 0 and "counting" not in (app.ui.locator("#summary-total").get_attribute("class") or "")
    assert app.page.evaluate("getComputedStyle(document.querySelector('#charts')).animationName") == "none"
    open_report(app)
    assert app.page.evaluate("getComputedStyle(document.getElementById('report')).animationName") == "none"
    app.ui.locator("#rp-next").click()                                  # a win card
    assert current_card(app) == 1 and card_kinds(app)[1] == "win:transportation"
    app.page.wait_for_timeout(150)
    assert app.ui.locator("#fx-layer > *").count() == 0                 # no confetti
    assert app.console_errors == []


# ---------------------------------------------------------------- 2
BADGE_COLOURS = """() => { const out = {}; ['0','1','2','3','4','5','6','7','8','9','10','11','n'].forEach((k) => {
  const b = document.createElement('span'); b.className = 'ibadge ib-' + k; document.body.appendChild(b);
  out['ib-' + k] = [getComputedStyle(b).backgroundColor, getComputedStyle(b).color]; b.remove(); }); return out; }"""
HUES = ["teal", "blue", "orange", "purple", "green", "rose", "indigo", "slate"]


def test_02_contrast(make_app):
    app = make_app()
    v = lambda name: css_var(app, name)
    assert (v("--bg"), v("--surface"), v("--surface-line"), v("--surface-2"), v("--text"), v("--text-2"), v("--accent"), v("--missing")) == (
        "#FAFDFC", "#F6FAF9", "#D7EBE7", "#EAF3F1", "#1F2933", "#5B6472", "#0F766E", "#EF4444")
    assert contrast(v("--text"), v("--bg")) >= 4.5                       # body text on the page
    assert contrast(v("--text-2"), v("--surface")) >= 4.5
    assert contrast(v("--accent"), v("--surface")) >= 4.5                # accent text
    assert contrast(v("--danger"), v("--surface")) >= 4.5
    # controls, as drawn
    app.type_amount("9")
    app.chip("Groceries").click()
    app.page.wait_for_timeout(300)
    chip = app.chip("Groceries").evaluate("(e) => [getComputedStyle(e).backgroundColor, getComputedStyle(e).color, getComputedStyle(e).borderTopColor]")
    assert chip == ["rgb(204, 251, 241)", "rgb(17, 94, 89)", "rgb(94, 234, 212)"] and contrast(chip[0], chip[1]) >= 4.5
    save = app.ui.locator("#btn-save").evaluate("(e) => [getComputedStyle(e).backgroundColor, getComputedStyle(e).color, getComputedStyle(e).borderTopColor]")
    assert save == ["rgb(187, 247, 208)", "rgb(20, 83, 45)", "rgb(134, 239, 172)"] and contrast(save[0], save[1]) >= 4.5
    app.save()
    toast = app.page.evaluate("[getComputedStyle(document.querySelector('.toast')).backgroundColor, getComputedStyle(document.querySelector('.toast-text')).color, getComputedStyle(document.querySelector('.toast-undo')).color]")
    assert toast == ["rgb(236, 253, 245)", "rgb(20, 83, 45)", "rgb(15, 118, 110)"]
    assert contrast(toast[0], toast[1]) >= 4.5 and contrast(toast[0], toast[2]) >= 4.5
    app.tab("profile")
    primary = app.ui.locator("#btn-add-card").evaluate("(e) => [getComputedStyle(e).backgroundColor, getComputedStyle(e).color]")
    assert primary == ["rgb(153, 246, 228)", "rgb(19, 78, 74)"] and contrast(primary[0], primary[1]) >= 4.5
    disabled = app.page.evaluate("(() => { document.querySelector('.tab[data-tab=add]').click(); const b = document.getElementById('btn-save'); return [getComputedStyle(b).backgroundColor, getComputedStyle(b).color]; })()")
    assert contrast(disabled[0], disabled[1]) >= 4.5
    # every badge: dark text of its hue on a pastel background
    badges = app.page.evaluate(BADGE_COLOURS)
    assert len(badges) == 13 and len({b[0] for b in badges.values()}) == 13
    for cls, (bg, fg) in badges.items():
        assert contrast(bg, fg) >= 4.5, (cls, bg, fg)
        assert luminance(bg) > 0.7, cls                                  # pastel
    # non-text indicators: 3:1 against the surface and the page
    assert contrast(v("--missing"), v("--surface")) >= 3 and contrast(v("--missing"), v("--bg")) >= 3
    assert contrast(v("--accent"), v("--bg")) >= 3                       # focus ring
    assert contrast("#5EEAD4", v("--surface")) < 3 <= contrast(v("--c-teal-edge"), v("--surface"))   # why fills need their edge
    for hue in HUES:
        fill, edge = v(f"--c-{hue}"), v(f"--c-{hue}-edge")
        assert contrast(edge, v("--surface")) >= 3, hue
        assert contrast(edge, fill) >= 3 or contrast(edge, v("--surface")) >= 4.5, hue
        assert luminance(fill) > 0.45, hue
    assert contrast(v("--databar-edge"), v("--surface")) >= 3

    # dark theme: unchanged from 0.2.3
    dark = make_app(scheme="dark")
    d = lambda name: css_var(dark, name)
    assert (d("--bg"), d("--surface"), d("--accent"), d("--c-teal"), d("--text"), d("--text-2")) == (
        "#000000", "#1C1C1E", "#5AD1C6", TEAL_OLD, "#F2F2F7", "#A9A9B0")
    assert d("--c-teal-edge") == TEAL_OLD and d("--missing") == "#FF6B61" and d("--surface-line") == "transparent"
    dark_badges = dark.page.evaluate(BADGE_COLOURS)
    assert dark_badges["ib-0"] == ["rgb(11, 110, 105)", "rgb(255, 255, 255)"] and dark_badges["ib-n"] == ["rgb(107, 114, 128)", "rgb(255, 255, 255)"]
    dark.type_amount("9")
    dark.chip("Groceries").click()
    dark.page.wait_for_timeout(300)
    assert dark.chip("Groceries").evaluate("(e) => [getComputedStyle(e).backgroundColor, getComputedStyle(e).color]") == ["rgb(90, 209, 198)", "rgb(0, 43, 40)"]
    assert dark.ui.locator("#btn-save").evaluate("(e) => [getComputedStyle(e).backgroundColor, getComputedStyle(e).color]") == ["rgb(27, 127, 59)", "rgb(255, 255, 255)"]
    assert dark.page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(0, 0, 0)"


# ---------------------------------------------------------------- 3
def test_03_pay_sheet(make_app):
    app = make_app()
    app.seed(state_with(NOVEMBER))
    app.tab("summary")
    assert app.ui.locator("#btn-compare").inner_text() == "📊 How do you compare?"
    app.ui.locator("#btn-compare").click()
    # no pay yet: the Pay sheet
    assert app.ui.locator("#sheet-title").inner_text() == "Your pay" and app.ui.locator("#report").count() == 0
    assert app.ui.locator("#pay-intro").inner_text() == "Compare your spending with a typical Canadian budget. Your pay stays on this phone."
    assert app.ui.locator('label[for="pay-1"]').inner_text() == "Your annual pay before tax"
    assert app.ui.locator("#pay-1").get_attribute("inputmode") == "decimal"
    assert app.ui.locator("#pay-footnote").inner_text() == (
        "Estimate for salary at 2026 rates, as on a pay cheque. Ignores RRSP, pension plans, benefits, other income and credits claimed at tax time. Not included in backups.")
    options = app.ui.locator("#pay-province option").all_inner_texts()
    assert len(options) == 14 and options[1:] == sorted(options[1:]) and options[1] == "Alberta" and options[-1] == "Yukon"
    assert app.ui.locator("#pay-province").input_value() == ""                      # no default
    save = app.ui.locator("#pay-save")
    assert save.inner_text() == "See my report" and save.is_disabled()
    assert app.ui.locator("#pay-skip").inner_text() == "Skip, compare spending split"
    # an amount alone is not enough; with a province the estimate appears live
    app.ui.locator("#pay-1").fill("40,000")
    assert save.is_disabled() and app.ui.locator("#pay-estimate").inner_text() == "Enter your pay and province for an estimate."
    app.ui.locator("#pay-province").select_option("AB")
    assert app.ui.locator("#pay-estimate").inner_text() == "Estimated take-home: $2,732 a month"        # 32,780 a year on the fixture
    assert save.is_enabled()
    # amounts: commas and cents are fine; over $2,000,000, zero or text are not
    for bad in ["2,000,001", "0", "abc", "12.345"]:
        app.ui.locator("#pay-1").fill(bad)
        assert app.ui.locator("#pay-error").inner_text() == "Enter an amount up to $2,000,000" and save.is_disabled(), bad
    for good in ["2,000,000", "$40,000.50", "1"]:
        app.ui.locator("#pay-1").fill(good)
        assert app.ui.locator("#pay-error").inner_text() == "" and save.is_enabled(), good
    app.ui.locator("#pay-1").fill("40000")
    # a second earner: add, and remove
    assert app.ui.locator("#pay-second").is_hidden()
    app.ui.locator("#pay-add-earner").click()
    assert app.ui.locator('label[for="pay-2"]').inner_text() == "Second earner's annual pay before tax"
    assert app.ui.locator("#pay-add-earner").is_hidden() and save.is_disabled()     # the second amount is needed now
    app.ui.locator("#pay-2").fill("120000")
    assert app.ui.locator("#pay-estimate").inner_text() == "Estimated take-home: $9,855 a month" and save.is_enabled()
    app.ui.locator("#pay-remove-2").click()
    assert app.ui.locator("#pay-second").is_hidden() and app.ui.locator("#pay-add-earner").is_visible()
    assert app.ui.locator("#pay-estimate").inner_text() == "Estimated take-home: $2,732 a month"
    app.ui.locator("#pay-add-earner").click()
    assert app.ui.locator("#pay-2").input_value() == "" and app.ui.locator("#pay-add-earner").count() == 1    # at most two
    app.ui.locator("#pay-2").fill("120,000")
    # Edit: the field is prefilled with the estimate; changing it makes it the user's own figure
    app.ui.locator("#pay-edit").click()
    assert app.ui.locator("#pay-takehome").input_value() == "9,855"
    assert app.ui.locator("#pay-estimate").inner_text() == "Estimated take-home: $9,855 a month"
    app.ui.locator("#pay-takehome").fill("9000")
    assert app.ui.locator("#pay-estimate").inner_text() == "Using your take-home: $9,000 a month"
    app.ui.locator("#pay-use-estimate").click()                                     # clears the override
    assert app.ui.locator("#pay-takehome-field").is_hidden() and app.ui.locator("#pay-estimate").inner_text() == "Estimated take-home: $9,855 a month"
    save.click()
    # saved, and the report opens in pay mode
    app.ui.locator("#report").wait_for()
    pay = app.state()["settings"]["pay"]
    assert (pay["earners"], pay["province"], pay["takeHomeOverrideCents"], pay["taxYear"]) == ([4000000, 12000000], "AB", None, 2026)
    assert app.state()["settings"]["paySkipped"] is False and app.sheet_hidden()
    assert app.ui.locator("#report").get_attribute("data-mode") == "pay"
    assert app.ui.locator("#rp-edit-pay").inner_text() == "Take-home about $9,855 a month · Alberta"
    # tapping the pay line edits pay; the next tap on the button goes straight to the report
    app.ui.locator("#rp-edit-pay").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Your pay" and app.ui.locator("#report").count() == 0
    assert (app.ui.locator("#pay-1").input_value(), app.ui.locator("#pay-2").input_value(), app.ui.locator("#pay-province").input_value()) == ("40,000", "120,000", "AB")
    app.page.keyboard.press("Escape")
    app.ui.locator("#btn-compare").click()
    app.ui.locator("#report").wait_for()
    assert app.sheet_hidden()
    app.page.keyboard.press("Escape")
    assert app.ui.locator("#report").count() == 0

    # Profile: the Pay row, edit, and Remove pay
    app.tab("profile")
    assert app.ui.locator("#pay-settings .row-title").inner_text() == "Pay for comparison"
    assert app.ui.locator("#pay-summary").inner_text() == "2 earners · Alberta · about $9,855 a month"
    app.ui.locator("#btn-pay").click()
    assert app.ui.locator("#pay-save").inner_text() == "Save" and app.ui.locator("#pay-skip").count() == 0
    assert app.ui.locator("#pay-remove").inner_text() == "Remove pay"
    app.ui.locator("#pay-remove-2").click()
    app.ui.locator("#pay-save").click()
    assert app.toast().inner_text() == "Pay saved" and app.ui.locator("#report").count() == 0
    assert app.ui.locator("#pay-summary").inner_text() == "Alberta · about $2,732 a month"
    assert app.state()["settings"]["pay"]["earners"] == [4000000]
    app.ui.locator("#btn-pay").click()
    app.ui.locator("#pay-edit").click()
    app.ui.locator("#pay-takehome").fill("4,000")
    app.ui.locator("#pay-save").click()
    assert app.ui.locator("#pay-summary").inner_text() == "Your take-home: $4,000 a month"
    assert app.state()["settings"]["pay"]["takeHomeOverrideCents"] == 400000
    # pay never goes into the backup
    assert "pay" not in copied_csv_text(app).lower().replace("payment_method", "")
    app.ui.locator("#btn-pay").click()
    app.ui.locator("#pay-remove").click()
    assert app.toast().inner_text() == "Pay removed"
    assert app.state()["settings"]["pay"] is None and app.state()["settings"]["paySkipped"] is False
    assert app.ui.locator("#pay-summary").inner_text() == "Not set"
    assert app.console_errors == [] and app.dialogs == []


def copied_csv_text(app):
    app.page.evaluate("""() => { window.__copied = null; Object.defineProperty(navigator, 'clipboard', { configurable: true,
      value: { writeText: (t) => { window.__copied = t; return Promise.resolve(); } } }); }""")
    return copied_csv(app)


def test_03b_override_skip_and_no_tax_data(make_app):
    # the override path: a monthly take-home on its own is enough
    app = make_app()
    app.seed(state_with(OCTOBER))
    open_october(app)
    app.ui.locator("#btn-compare").click()
    app.ui.locator("#pay-edit").click()
    assert app.ui.locator("#pay-takehome").input_value() == ""                      # nothing to prefill yet
    assert app.ui.locator('label[for="pay-takehome"]').inner_text() == "Monthly take-home"
    app.ui.locator("#pay-takehome").fill("4000")
    assert app.ui.locator("#pay-estimate").inner_text() == "Using your take-home: $4,000 a month"
    assert app.ui.locator("#pay-save").is_enabled() and app.ui.locator("#pay-1").input_value() == ""
    app.ui.locator("#pay-use-estimate").click()
    assert app.ui.locator("#pay-save").is_disabled()
    app.ui.locator("#pay-edit").click()
    app.ui.locator("#pay-takehome").fill("4000")
    app.ui.locator("#pay-save").click()
    app.ui.locator("#report").wait_for()
    pay = app.state()["settings"]["pay"]
    assert (pay["earners"], pay["province"], pay["takeHomeOverrideCents"]) == ([], None, 400000)
    assert app.ui.locator("#rp-edit-pay").inner_text() == "Take-home about $4,000 a month"
    assert app.tax_requests == 1

    # Skip: stored, split mode opens, and the next tap goes straight to the report
    b = make_app()
    b.seed(state_with(OCTOBER))
    open_october(b)
    b.ui.locator("#btn-compare").click()
    b.ui.locator("#pay-skip").click()
    b.ui.locator("#report").wait_for()
    assert b.state()["settings"]["paySkipped"] is True and b.state()["settings"]["pay"] is None
    assert b.ui.locator("#report").get_attribute("data-mode") == "split"
    b.ui.locator("#rp-close").click()
    b.ui.locator("#btn-compare").click()
    b.ui.locator("#report").wait_for()
    assert b.sheet_hidden()
    b.ui.locator("#rp-add-pay").click()                                             # pay can still be added later
    assert b.ui.locator("#sheet-title").inner_text() == "Your pay"
    b.ui.locator("#pay-1").fill("40000")
    b.ui.locator("#pay-province").select_option("AB")
    b.ui.locator("#pay-save").click()
    b.ui.locator("#report").wait_for()
    assert b.state()["settings"]["paySkipped"] is False and b.ui.locator("#report").get_attribute("data-mode") == "pay"

    # the tax figures cannot be loaded: the take-home field is asked for instead
    c = make_app(tax="fail")
    c.seed(state_with(OCTOBER))
    open_october(c)
    c.ui.locator("#btn-compare").click()
    c.ui.locator("#pay-takehome").wait_for()
    assert c.ui.locator("#pay-estimate").inner_text() == "Couldn't estimate here. Enter your monthly take-home instead."
    c.ui.locator("#pay-1").fill("40000")
    c.ui.locator("#pay-province").select_option("AB")                               # the list still has all 13
    assert c.ui.locator("#pay-save").is_disabled()
    c.ui.locator("#pay-takehome").fill("3,000")
    assert c.ui.locator("#pay-save").is_enabled()
    c.ui.locator("#pay-save").click()
    c.ui.locator("#report").wait_for()
    assert c.ui.locator("#report").get_attribute("data-mode") == "pay"

    # stored settings: invalid values are dropped on load; Delete all data clears pay and skip
    d = make_app()
    d.seed(state_with(NOVEMBER, pay={"earners": [5, 4000000, "x"], "province": "ZZ", "takeHomeOverrideCents": -1}, skipped=True))
    d.add("1", "Groceries")
    assert d.state()["settings"]["pay"] is None and d.state()["settings"]["paySkipped"] is True
    d.seed(state_with(NOVEMBER, pay={"earners": [4000000, 99], "province": "ON", "takeHomeOverrideCents": None}))
    d.add("1", "Groceries")
    assert d.state()["settings"]["pay"]["earners"] == [4000000] and d.state()["settings"]["pay"]["province"] == "ON"
    assert d.state()["schemaVersion"] == 3
    d.tab("profile")
    d.ui.locator("#btn-delete-all").click()
    d.ui.locator("#da-input").fill("DELETE")
    d.ui.locator("#da-go").click()
    assert d.state()["settings"]["pay"] is None and d.state()["settings"]["paySkipped"] is False


def test_03c_placeholder_tax_file_gives_no_estimate(make_app):
    data = json.load(open(os.path.join(ROOT, "data", "tax-ca-2026.json"), encoding="utf-8"))
    assert data["year"] == 2026 and len(data["provinces"]) == 13 and "referenceCases" in data
    if not data.get("placeholder"):
        pytest.skip("the real tax figures are in place")
    app = make_app(tax="real")
    app.seed(state_with(NOVEMBER))
    app.tab("summary")
    app.ui.locator("#btn-compare").click()
    app.ui.locator("#pay-takehome").wait_for()
    assert app.ui.locator("#pay-estimate").inner_text() == "Couldn't estimate here. Enter your monthly take-home instead."


# ---------------------------------------------------------------- 4
# Hand-worked on the synthetic figures in conftest.FIXTURE_TAX (not real rates):
#   federal  10% to 50,000, 20% to 100,000, 30% above; credits at 10%; BPA 10,000 falling to 5,000
#            between 100,000 and 200,000; employment amount 1,000; Quebec abatement 20%
#   CPP      YMPE 60,000, YAMPE 70,000, exemption 5,000; base 5% (QPP 6%), first additional 1%, second 4%
#   EI       2% (Quebec 1%) to 50,000;  QPIP 0.5% to 80,000
ESTIMATES = [
    # --- income below every maximum (AB: 10% to 100,000, credits at 10%, BPA 20,000)
    # pensionable 40,000 - 5,000 = 35,000: base 1,750, first 350; cpp2 0; EI 40,000 x 2% = 800
    # NI = 40,000 - 350 = 39,650
    # federal: 3,965 - 10% x (10,000 + 1,000 + 1,750 + 800 = 13,550) = 3,965 - 1,355 = 2,610
    # AB: 3,965 - 10% x (20,000 + 1,750 + 800 = 22,550) = 3,965 - 2,255 = 1,710
    # take-home = 40,000 - 2,100 - 800 - 2,610 - 1,710 = 32,780
    ("AB", 40000, {"cppBase": 1750, "cppFirst": 350, "cpp2": 0, "ei": 800, "qpip": 0, "federalTax": 2610, "provincialTax": 1710, "takeHome": 32780}),
    # --- above YMPE, YAMPE and the EI maximum; federal BPA part-way through its phase-out
    # pensionable 60,000 - 5,000 = 55,000: base 2,750, first 550; cpp2 (70,000 - 60,000) x 4% = 400; EI 50,000 x 2% = 1,000
    # NI = 120,000 - 550 - 400 = 119,050
    # federal brackets: 5,000 + 10,000 + 19,050 x 30% = 20,715
    # federal BPA: 10,000 - 5,000 x (19,050 / 100,000) = 9,047.50
    # federal: 20,715 - 10% x (9,047.50 + 1,000 + 2,750 + 1,000 = 13,797.50) = 20,715 - 1,379.75 = 19,335.25
    # AB: 10,000 + 19,050 x 15% = 12,857.50; - 10% x (20,000 + 2,750 + 1,000) = 2,375 -> 10,482.50
    # take-home = 120,000 - 3,700 - 1,000 - 19,335.25 - 10,482.50 = 85,482.25
    ("AB", 120000, {"cppBase": 2750, "cppFirst": 550, "cpp2": 400, "ei": 1000, "qpip": 0, "federalTax": 19335.25, "provincialTax": 10482.50, "takeHome": 85482.25}),
    # --- Quebec: QPP base 6%, EI 1%, QPIP, the abatement, the employment deduction, no CPP/EI/QPIP provincial credits
    # pensionable 55,000: base 3,300, first 550; cpp2 0; EI 50,000 x 1% = 500; QPIP 60,000 x 0.5% = 300
    # NI = 60,000 - 550 = 59,450
    # federal: 5,000 + 9,450 x 20% = 6,890; - 10% x (10,000 + 1,000 + 3,300 + 500 + 300 = 15,100) = 5,380; x (1 - 20%) = 4,304
    # QC: TI = 59,450 - min(1,400, 6% x 60,000 = 3,600) = 58,050; 14% x 50,000 + 19% x 8,050 = 8,529.50
    #     credits: BPA 18,000 only -> 14% x 18,000 = 2,520; tax 6,009.50
    # take-home = 60,000 - 3,850 - 500 - 300 - 4,304 - 6,009.50 = 45,036.50
    ("QC", 60000, {"cppBase": 3300, "cppFirst": 550, "cpp2": 0, "ei": 500, "qpip": 300, "federalTax": 4304, "provincialTax": 6009.50, "takeHome": 45036.50}),
    # --- Ontario-style: surtax (20% over 3,000, 36% over 5,000), reduction (basic 300), health premium (two tiers)
    # CPP as above with cpp2 400; EI 1,000; NI = 90,000 - 950 = 89,050
    # federal: 5,000 + 39,050 x 20% = 12,810; - 10% x (10,000 + 1,000 + 2,750 + 1,000) = 1,475 -> 11,335
    # ON: 2,000 + 4,000 + 9,050 x 15% = 7,357.50; - 5% x (10,000 + 2,750 + 1,000 = 13,750) = 687.50 -> basic 6,670
    #     surtax 20% x 3,670 + 36% x 1,670 = 734 + 601.20 = 1,335.20; reduction max(0, 600 - 8,005.20) = 0
    #     premium min(300, 69,050 x 6%) + min(150, 53,050 x 6%) = 450; tax 6,670 + 1,335.20 + 450 = 8,455.20
    # take-home = 90,000 - 3,700 - 1,000 - 11,335 - 8,455.20 = 65,509.80
    ("ON", 90000, {"cppBase": 2750, "cppFirst": 550, "cpp2": 400, "ei": 1000, "qpip": 0, "federalTax": 11335, "provincialTax": 8455.20, "takeHome": 65509.80}),
    # --- Ontario-style, low income: the reduction applies, no surtax, no premium
    # pensionable 15,000: base 750, first 150; EI 400; NI = 19,850
    # federal: 1,985 - 10% x (10,000 + 1,000 + 750 + 400 = 12,150) = 770
    # ON: 5% x 19,850 = 992.50; - 5% x (10,000 + 750 + 400 = 11,150) = 557.50 -> basic 435
    #     reduction min(435, max(0, 2 x 300 - 435 = 165)) = 165; premium 0 (19,850 < 20,000); tax 270
    # take-home = 20,000 - 900 - 400 - 770 - 270 = 17,660
    ("ON", 20000, {"cppBase": 750, "cppFirst": 150, "cpp2": 0, "ei": 400, "qpip": 0, "federalTax": 770, "provincialTax": 270, "takeHome": 17660}),
    # --- a linear reduction (BC-style: 500, less 4% of net income over 25,000)
    # pensionable 25,000: base 1,250, first 250; EI 600; NI = 29,750
    # federal: 2,975 - 10% x (10,000 + 1,000 + 1,250 + 600 = 12,850) = 1,690
    # BC: 5% x 29,750 = 1,487.50; - 5% x (12,000 + 1,250 + 600 = 13,850) = 692.50 -> 795
    #     reduction min(795, 500 - 4% x 4,750 = 310) = 310; tax 485
    # take-home = 30,000 - 1,500 - 600 - 1,690 - 485 = 25,725
    ("BC", 30000, {"cppBase": 1250, "cppFirst": 250, "cpp2": 0, "ei": 600, "qpip": 0, "federalTax": 1690, "provincialTax": 485, "takeHome": 25725}),
    # --- BPA phase-out: federal at its minimum, provincial part-way (MB-style: 15,000 falling to 0 between 200,000 and 400,000)
    # CPP 2,750 + 550 + 400; EI 1,000; NI = 300,000 - 950 = 299,050
    # federal: 5,000 + 10,000 + 199,050 x 30% = 74,715; BPA 5,000 (NI past 200,000)
    #          - 10% x (5,000 + 1,000 + 2,750 + 1,000 = 9,750) = 975 -> 73,740
    # MB: 10% x 299,050 = 29,905; BPA 15,000 - 15,000 x (99,050 / 200,000) = 7,571.25
    #     - 8% x (7,571.25 + 2,750 + 1,000 = 11,321.25) = 905.70 -> 28,999.30
    # take-home = 300,000 - 3,700 - 1,000 - 73,740 - 28,999.30 = 192,560.70
    ("MB", 300000, {"cppBase": 2750, "cppFirst": 550, "cpp2": 400, "ei": 1000, "qpip": 0, "federalTax": 73740, "provincialTax": 28999.30, "takeHome": 192560.70}),
    # --- a provincial employment amount (YT-style: as AB plus 1,000): credits 23,550 -> 2,355; tax 3,965 - 2,355 = 1,610
    ("YT", 40000, {"cppBase": 1750, "cppFirst": 350, "cpp2": 0, "ei": 800, "qpip": 0, "federalTax": 2610, "provincialTax": 1610, "takeHome": 32880}),
    # --- nothing owed at a very low income: below the CPP exemption, tax floors at zero; EI 3,000 x 2% = 60
    ("AB", 3000, {"cppBase": 0, "cppFirst": 0, "cpp2": 0, "ei": 60, "qpip": 0, "federalTax": 0, "provincialTax": 0, "takeHome": 2940}),
]


def test_04_estimator_on_synthetic_figures(app):
    assert app.page.evaluate("typeof window.DSTax.estimate + typeof window.DSTax.household") == "functionfunction"
    for province, gross, want in ESTIMATES:
        got = app.page.evaluate("([d, g, p]) => window.DSTax.estimate(d, g, p)", [FIXTURE_TAX, gross, province])
        assert got["gross"] == gross
        for key, value in want.items():
            assert abs(got[key] - value) < 0.005, (province, gross, key, got[key], value)
        parts = got["cppBase"] + got["cppFirst"] + got["cpp2"] + got["ei"] + got["qpip"] + got["federalTax"] + got["provincialTax"]
        assert abs(got["gross"] - parts - got["takeHome"]) < 0.005
    # household: 32,780 + 85,482.25 = 118,262.25 a year; / 12 = 9,855.1875 a month
    house = app.page.evaluate("(d) => window.DSTax.household(d, [40000, 120000], 'AB')", FIXTURE_TAX)
    assert house["takeHomeAnnual"] == 118262.25 and abs(house["takeHomeMonthly"] - 9855.1875) < 1e-9
    assert [e["takeHome"] for e in house["perEarner"]] == [32780, 85482.25]
    # pure: the data object is not changed, and no request was made for it
    assert app.page.evaluate("(d) => { const before = JSON.stringify(d); window.DSTax.estimate(d, 90000, 'ON'); return JSON.stringify(d) === before; }", FIXTURE_TAX)
    assert app.tax_requests == 0


# ---------------------------------------------------------------- 5
def test_05_reference_cases_real_file(make_app):
    data = json.load(open(os.path.join(ROOT, "data", "tax-ca-2026.json"), encoding="utf-8"))
    cases = data.get("referenceCases") or []
    if not cases:
        pytest.skip("data/tax-ca-2026.json has no referenceCases yet (placeholder file)")
    app = make_app(tax="real")
    for case in cases:
        got = app.page.evaluate("([d, g, p]) => window.DSTax.estimate(d, g, p)", [data, case["gross"], case["province"]])
        for key, value in case["expected"].items():
            assert abs(got[key] - value) <= 1, (case["id"], key, got[key], value)


# ---------------------------------------------------------------- 6
def test_06_report_pay_mode(app):
    app.seed(state_with(OCTOBER, pay=PAY_4000))
    open_october(app)
    open_report(app)
    dialog = app.ui.locator("#report")
    assert (dialog.get_attribute("role"), dialog.get_attribute("aria-modal"), dialog.get_attribute("data-mode")) == ("dialog", "true", "pay")
    assert app.ui.locator("#" + dialog.get_attribute("aria-labelledby")).inner_text() == "How do you compare?"
    assert app.ui.locator("#rp-close").get_attribute("aria-label") == "Close"
    assert app.page.evaluate("[document.getElementById('app').inert, getComputedStyle(document.getElementById('report')).animationName]") == [True, "report-in"]
    app.page.wait_for_timeout(450)                                       # measured once the entry animation has ended
    box = dialog.bounding_box()
    assert (box["x"], box["y"], box["width"], box["height"]) == (0, 0, 390, 844)                    # full screen
    # card order: score, wins, overs (largest first), savings, not logged, wrap-up
    assert card_kinds(app) == ["score", "win:transportation", "over:food", "over:housing", "over:recreation", "savings", "notlogged", "wrap"]
    cards = app.ui.locator("#report .rp-card")
    assert cards.evaluate_all("(els) => els.map((e) => [e.tagName, e.getAttribute('aria-roledescription'), e.getAttribute('aria-label')])") == [
        ["SECTION", "slide", f"{i} of 8"] for i in range(1, 9)]
    assert app.ui.locator(".rp-dots i").count() == 8
    # score
    assert app.ui.locator("#rp-headline").inner_text() == "Room to grow"
    assert app.ui.locator("#rp-score").inner_text() == "At or under typical in 1 of 4 groups"
    assert app.ui.locator("#rp-period").inner_text() == "October 2026"
    assert app.ui.locator("#rp-edit-pay").inner_text() == "Take-home about $4,000 a month"
    assert app.ui.locator("#rp-so-far, #rp-not-over").count() == 0                                   # October is over
    # the win: Transportation, typical 15% x 4,000 = 600, spent 300
    win = card(app, "win", "transportation")
    assert win.locator("h3").inner_text() == "Transportation"
    assert win.locator(".rp-you").inner_text() == "You: $300 a month (7.5% of take-home)"
    assert win.locator(".rp-typical").inner_text() == "Typical: $600 (15%)"
    assert win.locator(".rp-diff").inner_text() == "🎉 $300 less than typical"
    assert win.locator(".rp-year").inner_text() == "That's about $3,600 a year in your pocket."
    widths = win.locator(".rp-bar i").evaluate_all("(els) => els.map((e) => parseFloat(e.style.width))")
    assert widths == [50.0, 100.0]                                                                   # same scale: 300 against 600
    colours = win.evaluate("""(c) => { const you = getComputedStyle(c.querySelector('.rp-bar.you i')), typ = getComputedStyle(c.querySelector('.rp-bar.typical i'));
      const root = getComputedStyle(document.documentElement);
      return [you.backgroundColor, typ.backgroundColor, typ.boxShadow.includes('2px'), root.getPropertyValue('--c-green').trim()]; }""")
    assert colours[0] == "rgb(134, 239, 172)" and colours[1] == "rgba(0, 0, 0, 0)" and colours[2] and colours[3] == "#86EFAC"   # the group's colour; typical is an outline
    # the overs, largest first: Food 900 - 480, Housing 1,500 - 1,200, Recreation 600 - 400
    food = card(app, "over", "food")
    assert food.locator(".rp-you").inner_text() == "You: $900 a month (22.5% of take-home)"
    assert food.locator(".rp-typical").inner_text() == "Typical: $480 (12%)"
    assert food.locator(".rp-diff").inner_text() == "$420 over typical"
    assert food.locator(".rp-trim").inner_text() == "Trim it by 10% and keep about $90 a month ($1,080 a year)"
    assert food.locator(".rp-tip").inner_text() == "Plan meals around grocery flyers, and swap one takeout meal a week for cooking at home."
    assert card(app, "over", "housing").locator(".rp-diff").inner_text() == "$300 over typical"
    assert card(app, "over", "housing").locator(".rp-trim").inner_text() == "Trim it by 10% and keep about $150 a month ($1,800 a year)"
    assert card(app, "over", "housing").locator(".rp-tip").inner_text().startswith("Housing is hard to change quickly.")
    assert card(app, "over", "recreation").locator(".rp-diff").inner_text() == "$200 over typical"
    assert card(app, "over", "recreation").locator(".rp-tip").inner_text() == "Set a monthly fun budget, and look for free local events and library passes."
    # savings: 4,000 - 3,300 = 700 = 17.5%, at or above 8%
    assert app.ui.locator("#rp-savings-line").inner_text() == "Left after logged spending: $700 a month (17.5%)"
    assert app.ui.locator("#rp-savings-typical").inner_text() == "A typical budget saves 8%"
    assert card(app, "savings").get_attribute("data-confetti") == "1"                                # a win
    assert "Only counts spending you've logged." in card(app, "savings").inner_text()
    # not logged yet
    assert app.ui.locator("#rp-not-logged li").all_inner_texts() == ["Debt Payments", "Communications", "Miscellaneous", "Insurance"]
    assert "If you pay for these, log them to see the full picture." in card(app, "notlogged").inner_text()
    # wrap-up
    assert app.ui.locator("#rp-best").inner_text() == "Biggest win: Transportation, $300 less than typical"
    assert app.ui.locator("#rp-opp").inner_text() == "Biggest opportunity: Food, $420 over typical"
    assert app.ui.locator("#rp-opp-trim").inner_text() == "Trim it by 10% and keep about $90 a month ($1,080 a year)"
    assert app.ui.locator("#rp-done").inner_text() == "Done" and app.ui.locator("#rp-pay").inner_text() == "Edit pay"
    assert app.ui.locator("#rp-footnote").inner_text() == (
        "Typical shares come from a popular Canadian budgeting template. They're a rough guide, not official statistics.")
    # tone, and at most one emoji per card besides the group's own
    text = dialog.inner_text().lower()
    assert not re.search(r"\b(bad|fail\w*|overspen\w*|shame\w*)\b", text)

    # moving between cards: Next and Back (44 px), arrow keys, focus on the card's heading, Escape
    assert current_card(app) == 0 and app.ui.locator("#rp-back").is_disabled()
    assert app.page.evaluate("document.activeElement.id") == "rp-headline"
    sizes = app.ui.locator("#rp-back, #rp-next, #rp-close").evaluate_all("(els) => els.map((e) => Math.min(e.getBoundingClientRect().width, e.getBoundingClientRect().height))")
    assert min(sizes) >= 44
    assert app.ui.locator("#fx-layer .fx-confetti").count() == 0                                     # the score card is not a win card
    app.ui.locator("#rp-next").click()
    assert current_card(app) == 1 and app.page.evaluate("document.activeElement.textContent") == "Transportation"
    assert app.ui.locator("#fx-layer .fx-confetti i").count() == 24                                  # confetti on a win card...
    assert app.page.evaluate("[getComputedStyle(document.querySelector('.fx-confetti')).pointerEvents, document.getElementById('fx-layer').getAttribute('aria-hidden')]") == ["none", "true"]
    app.page.wait_for_timeout(1000)
    assert app.ui.locator("#fx-layer .fx-confetti").count() == 0                                     # ...gone within 900 ms
    snap = app.page.evaluate("(() => { const t = document.getElementById('rp-track'); return [getComputedStyle(t).scrollSnapType, Math.round(t.scrollLeft / t.clientWidth)]; })()")
    assert snap == ["x mandatory", 1]
    app.page.keyboard.press("ArrowRight")
    assert current_card(app) == 2 and app.page.evaluate("document.activeElement.textContent") == "Food"
    assert app.ui.locator("#fx-layer .fx-confetti").count() == 0                                     # an over card: none
    app.page.keyboard.press("ArrowLeft")
    assert current_card(app) == 1 and app.ui.locator("#fx-layer .fx-confetti").count() == 0          # once per card per opening
    app.ui.locator("#rp-back").click()
    assert current_card(app) == 0
    for _ in range(7):
        app.page.keyboard.press("ArrowRight")
    assert current_card(app) == 7 and app.ui.locator("#rp-next").is_disabled()
    assert app.ui.locator(".rp-dots i.on").count() == 1
    assert app.ui.locator("#fx-layer .fx-confetti").count() == 1                                     # wrap-up with at least one win
    # a swipe (the track scrolls) moves the card too
    app.page.evaluate("(() => { const t = document.getElementById('rp-track'); t.scrollTo({ left: 5 * t.clientWidth, behavior: 'auto' }); })()")
    app.page.wait_for_timeout(700)
    app.page.evaluate("(() => { const t = document.getElementById('rp-track'); t.scrollTo({ left: 4 * t.clientWidth, behavior: 'auto' }); })()")
    app.page.wait_for_timeout(300)
    assert current_card(app) == 4
    # Tab stays inside the dialog
    for _ in range(8):
        app.page.keyboard.press("Tab")
        assert app.page.evaluate("document.getElementById('report').contains(document.activeElement)")
    app.page.keyboard.press("Escape")
    assert app.ui.locator("#report").count() == 0 and app.page.evaluate("document.getElementById('app').inert") is False
    assert app.page.evaluate("document.activeElement.id") == "btn-compare"                           # focus returns
    # Done closes; Edit pay opens the Pay sheet
    open_report(app)
    app.ui.locator("#rp-done").evaluate("(e) => e.click()")
    assert app.ui.locator("#report").count() == 0
    open_report(app)
    app.ui.locator("#rp-pay").evaluate("(e) => e.click()")
    assert app.ui.locator("#sheet-title").inner_text() == "Your pay" and app.ui.locator("#pay-takehome").input_value() == "4,000"
    assert app.console_errors == [] and app.dialogs == []


def test_06b_report_other_outcomes(app):
    # all wins: "Budget boss!"; a group right at typical counts as a win; under 8% left
    rows = [("2026-10-01", 120000, "housing", "etransfer", "", ""), ("2026-10-02", 200000, "groceries", "credit", "", "")]
    app.seed(state_with(rows, pay={"earners": [], "province": None, "takeHomeOverrideCents": 400000}))
    open_october(app)
    open_report(app)
    assert card_kinds(app)[:3] == ["score", "win:housing", "over:food"]
    assert card(app, "win", "housing").locator(".rp-diff").inner_text() == "🎉 Right at typical"
    assert card(app, "win", "housing").locator(".rp-year").count() == 0
    assert app.ui.locator("#rp-headline").inner_text() == "Nicely balanced"                          # 1 of 2
    # left 4,000 - 3,200 = 800 = 20%: a win. Now make it tight.
    app.page.keyboard.press("Escape")
    rows.append(("2026-10-03", 60000, "gas", "credit", "", ""))                                      # 600: at typical; left 200 = 5%
    app.seed(state_with(rows, pay={"earners": [], "province": None, "takeHomeOverrideCents": 400000}))
    open_october(app)
    open_report(app)
    assert app.ui.locator("#rp-score").inner_text() == "At or under typical in 2 of 3 groups"
    assert app.ui.locator("#rp-savings-line").inner_text() == "Left after logged spending: $200 a month (5%)"
    assert app.ui.locator("#rp-savings-next").inner_text() == "Saving 8% would mean $320 a month"
    assert card(app, "savings").get_attribute("data-confetti") is None
    app.page.keyboard.press("Escape")
    # spending above take-home, and "just over" (within 5% of typical)
    rows = [("2026-10-01", 125000, "housing", "etransfer", "", ""), ("2026-10-02", 300000, "groceries", "credit", "", "")]
    app.seed(state_with(rows, pay={"earners": [], "province": None, "takeHomeOverrideCents": 400000}))
    open_october(app)
    open_report(app)
    assert card(app, "over", "housing").locator(".rp-diff").inner_text() == "Just over typical, by $50"   # 50 <= 5% of 1,200
    assert app.ui.locator("#rp-headline").inner_text() == "Room to grow" and app.ui.locator("#rp-best").count() == 0
    assert app.ui.locator("#rp-savings-line").inner_text() == "You spent $250 more than your take-home"
    assert app.ui.locator("#rp-savings-next").inner_text() == "Start with your biggest group over typical"
    assert card(app, "wrap").get_attribute("data-confetti") is None
    app.page.keyboard.press("Escape")
    # every group under: all wins
    app.seed(state_with([("2026-10-01", 10000, "housing", "etransfer", "", ""), ("2026-10-02", 10000, "groceries", "credit", "", "")],
                        pay={"earners": [], "province": None, "takeHomeOverrideCents": 400000}))
    open_october(app)
    open_report(app)
    assert app.ui.locator("#rp-headline").inner_text() == "Budget boss!" and app.ui.locator("#rp-opp").count() == 0
    assert card_kinds(app) == ["score", "win:housing", "win:food", "savings", "notlogged", "wrap"]     # 1,190 under, then 470 under


def test_06c_figures_foot(app):
    # Take-home 3,877.40; Housing 1,982.60 and Food 465.40 in October (a complete month).
    # Shown: You 1,983; typical round(0.30 x 3,877.40 = 1,163.22) = 1,163; over by 1,983 - 1,163 = 820 (unrounded: 819.38).
    rows = [("2026-10-01", 198260, "housing", "etransfer", "", "Rent"), ("2026-10-05", 46540, "groceries", "credit", "", "")]
    app.seed(state_with(rows, pay={"earners": [], "province": None, "takeHomeOverrideCents": 387740}))
    open_october(app)
    open_report(app)
    housing = card(app, "over", "housing")
    assert housing.locator(".rp-you").inner_text().startswith("You: $1,983 a month")
    assert housing.locator(".rp-typical").inner_text() == "Typical: $1,163 (30%)"
    assert housing.locator(".rp-diff").inner_text() == "$820 over typical"
    assert housing.locator(".rp-trim").inner_text() == "Trim it by 10% and keep about $198 a month ($2,376 a year)"     # round(198.3), x 12
    # Food: 465 against round(465.288) = 465: right at typical on the shown figures (unrounded it is 11 cents over)
    food = card(app, "win", "food")
    assert food.locator(".rp-you").inner_text().startswith("You: $465 a month") and food.locator(".rp-typical").inner_text() == "Typical: $465 (12%)"
    assert food.locator(".rp-diff").inner_text() == "🎉 Right at typical" and food.locator(".rp-year").count() == 0
    assert app.ui.locator("#rp-score").inner_text() == "At or under typical in 1 of 2 groups"
    # savings: round(3,877.40) - round(2,448.00) = 3,877 - 2,448 = 1,429; 1,429 / 3,877 = 36.9%
    assert app.ui.locator("#rp-savings-line").inner_text() == "Left after logged spending: $1,429 a month (36.9%)"
    assert app.ui.locator("#rp-best").inner_text() == "Biggest win: Food, Right at typical"
    assert app.ui.locator("#rp-opp").inner_text() == "Biggest opportunity: Housing, $820 over typical"
    app.page.keyboard.press("Escape")
    # a win: the year line is 12 x the shown difference. Take-home 3,877.40, Transportation 271.60: 272 against round(581.61) = 582
    app.seed(state_with([("2026-10-03", 27160, "gas", "credit", "", "")], pay={"earners": [], "province": None, "takeHomeOverrideCents": 387740}))
    open_october(app)
    open_report(app)
    win = card(app, "win", "transportation")
    assert win.locator(".rp-diff").inner_text() == "🎉 $310 less than typical"                       # 582 - 272
    assert win.locator(".rp-year").inner_text() == "That's about $3,720 a year in your pocket."      # 12 x 310
    assert app.console_errors == []


# ---------------------------------------------------------------- 7
def test_07_report_split_mode(app):
    app.seed(state_with(OCTOBER, skipped=True))
    open_october(app)
    open_report(app)
    assert app.ui.locator("#report").get_attribute("data-mode") == "split"
    assert app.ui.locator("#rp-mode").inner_text() == "Comparing how your spending splits"
    assert app.ui.locator("#rp-add-pay").inner_text() == "Add your pay"
    assert app.ui.locator("#rp-score").inner_text() == "At or under typical in 1 of 4 groups"
    # typical shares over the groups with spending: 30, 12, 15, 10 out of 67; yours out of 3,300
    shares = {}
    for group in ["housing", "food", "transportation", "recreation"]:
        c = app.ui.locator(f'#report .rp-card[data-group="{group}"]')
        shares[group] = (c.locator(".rp-typical").inner_text(), c.locator(".rp-you").inner_text())
    assert shares == {
        "housing": ("Typical: 44.8%", "You: 45.5% of your spending ($1,500 a month)"),
        "food": ("Typical: 17.9%", "You: 27.3% of your spending ($900 a month)"),
        "transportation": ("Typical: 22.4%", "You: 9.1% of your spending ($300 a month)"),
        "recreation": ("Typical: 14.9%", "You: 18.2% of your spending ($600 a month)")}
    # one win; overs by points, largest first; no savings card without pay
    assert card_kinds(app) == ["score", "win:transportation", "over:food", "over:recreation", "over:housing", "notlogged", "wrap"]
    assert card(app, "win", "transportation").locator(".rp-diff").inner_text() == "🎉 13.3 points under the typical share"
    assert card(app, "over", "food").locator(".rp-diff").inner_text() == "9.4 points over the typical share"
    assert card(app, "over", "recreation").locator(".rp-diff").inner_text() == "3.3 points over the typical share"
    assert card(app, "over", "housing").locator(".rp-diff").inner_text() == "0.7 points over the typical share"
    assert card(app, "over", "food").locator(".rp-trim").inner_text() == "Trim it by 10% and keep about $90 a month ($1,080 a year)"
    assert app.ui.locator("#rp-best").inner_text() == "Biggest win: Transportation, 13.3 points under the typical share"
    assert app.ui.locator("#rp-opp").inner_text() == "Biggest opportunity: Food, 9.4 points over the typical share"
    assert app.ui.locator("#rp-pay").inner_text() == "Add your pay" and app.ui.locator("#rp-edit-pay").count() == 0
    assert "$" not in card(app, "win", "transportation").locator(".rp-diff").inner_text()
    app.page.keyboard.press("Escape")

    # shares that display equal: Housing 30 and Food 12 of 42 are 71.4% and 28.6%.
    # Spending 2,499.70 and 1,000.30 of 3,500: 71.42% and 28.58%, shown as 71.4% and 28.6%. 0.0 points: at the typical share, a win.
    app.seed(state_with([("2026-10-01", 249970, "housing", "etransfer", "", ""), ("2026-10-05", 100030, "groceries", "credit", "", "")], skipped=True))
    open_october(app)
    open_report(app)
    assert card_kinds(app) == ["score", "win:housing", "win:food", "notlogged", "wrap"]
    assert card(app, "win", "housing").locator(".rp-you").inner_text() == "You: 71.4% of your spending ($2,500 a month)"
    assert card(app, "win", "housing").locator(".rp-typical").inner_text() == "Typical: 71.4%"
    assert card(app, "win", "housing").locator(".rp-diff").inner_text() == "🎉 Right at the typical share"
    assert card(app, "win", "food").locator(".rp-diff").inner_text() == "🎉 Right at the typical share"   # unrounded it is a hair over
    assert app.ui.locator("#rp-score").inner_text() == "At or under typical in 2 of 2 groups"
    assert app.ui.locator("#rp-headline").inner_text() == "Budget boss!" and app.ui.locator("#rp-opp").count() == 0
    assert app.ui.locator("#rp-best").inner_text() == "Biggest win: Housing, Right at the typical share"
    app.page.keyboard.press("Escape")

    # fewer than two groups with spending: one card
    app.seed(state_with(OCTOBER[:1], skipped=True))
    open_october(app)
    open_report(app)
    assert card_kinds(app) == ["few"] and app.ui.locator("#rp-few").inner_text() == "Log spending in a few more groups to compare."
    assert app.ui.locator("#rp-next").is_disabled() and app.ui.locator("#rp-back").is_disabled()
    app.ui.locator("#rp-add-pay").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Your pay"
    assert app.console_errors == []


# ---------------------------------------------------------------- 8
def test_08_three_month_average(app):
    rows = [("2026-09-10", 30000, "groceries", "credit", "", ""), ("2026-10-10", 60000, "groceries", "credit", "", ""),
            ("2026-11-10", 30000, "groceries", "credit", "", "")]
    app.seed(state_with(rows, pay=PAY_4000))
    app.tab("summary")
    app.ui.locator('#range-seg [data-range="3"]').click()
    assert app.ui.locator("#btn-compare").is_visible()
    open_report(app)
    assert app.ui.locator("#rp-period").inner_text() == "Sep – Nov 2026 · monthly average"
    food = card(app, "win", "food")
    assert food.locator(".rp-you").inner_text() == "You: $400 a month (10% of take-home)"            # 1,200 over 3 months
    assert food.locator(".rp-typical").inner_text() == "Typical: $480 (12%)"
    assert food.locator(".rp-diff").inner_text() == "🎉 $80 less than typical"
    assert food.locator(".rp-year").inner_text() == "That's about $960 a year in your pocket."
    assert app.ui.locator("#rp-so-far").inner_text() == "Includes this month so far."
    assert app.ui.locator("#rp-not-over").count() == 0                                               # not the current month alone
    assert app.ui.locator("#rp-savings-line").inner_text() == "Left after logged spending: $3,600 a month (90%)"
    app.page.keyboard.press("Escape")
    # 12 months: 1,200 / 12 = 100 a month
    app.ui.locator('#range-seg [data-range="12"]').click()
    open_report(app)
    assert app.ui.locator("#rp-period").inner_text() == "Dec 2025 – Nov 2026 · monthly average"
    assert card(app, "win", "food").locator(".rp-you").inner_text() == "You: $100 a month (2.5% of take-home)"
    app.page.keyboard.press("Escape")
    # the current month on its own: both notes
    app.ui.locator('#range-seg [data-range="month"]').click()
    open_report(app)
    assert app.ui.locator("#rp-period").inner_text() == "November 2026"
    assert app.ui.locator("#rp-so-far").inner_text() == "Includes this month so far."
    assert app.ui.locator("#rp-not-over").inner_text() == "The month isn't over yet, so some groups may look low."


# ---------------------------------------------------------------- 9
def test_09_button_visibility(app):
    app.seed(state_with(OCTOBER, pay=PAY_4000))
    app.tab("summary")                                                   # November: nothing logged
    assert app.ui.locator("#btn-compare").count() == 0
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    btn = app.ui.locator("#btn-compare")
    assert btn.count() == 1
    # between the total and the charts card, full width
    order = app.page.evaluate("['summary-total', 'btn-compare', 'charts'].map((id) => document.getElementById(id).getBoundingClientRect().top)")
    assert order == sorted(order) and btn.bounding_box()["width"] >= 390 - 24 - 1 and btn.bounding_box()["height"] >= 44
    tap_inside(app, app.ui.locator('#donut .slice[data-group="food"]'))
    assert app.ui.locator("#group-view").count() == 1 and app.ui.locator("#btn-compare").count() == 0      # hidden in group view
    app.ui.locator("#group-back").click()
    assert app.ui.locator("#btn-compare").count() == 1
    for choice in ["3", "12"]:
        app.ui.locator(f'#range-seg [data-range="{choice}"]').click()
        assert app.ui.locator("#btn-compare").count() == 1
    app.seed(state_with([], pay=PAY_4000))
    app.tab("summary")
    for choice in ["3", "12", "month"]:
        app.ui.locator(f'#range-seg [data-range="{choice}"]').click()
        assert app.ui.locator("#btn-compare").count() == 0                                           # an empty period


# ---------------------------------------------------------------- 10
def test_10_no_external_requests_and_no_template_name(app):
    app.seed(state_with(OCTOBER))
    open_october(app)
    app.ui.locator("#btn-compare").click()
    app.ui.locator("#pay-1").fill("85,000")
    app.ui.locator("#pay-add-earner").click()
    app.ui.locator("#pay-2").fill("62,500")
    app.ui.locator("#pay-province").select_option("ON")
    assert app.ui.locator("#pay-estimate").inner_text().startswith("Estimated take-home: $")
    seen = app.ui.locator("#sheet-root").inner_text()
    app.ui.locator("#pay-save").click()
    app.ui.locator("#report").wait_for()
    for _ in range(8):
        app.page.keyboard.press("ArrowRight")
    seen += "\n" + app.page.evaluate("document.body.textContent")
    app.page.keyboard.press("Escape")
    app.tab("profile")
    seen += "\n" + app.page.evaluate("document.body.textContent")
    # every request went to the site itself (the pay figures were never sent anywhere)
    prefix = app.base_url + "/"
    assert [u for u in app.requests if not u.startswith(prefix) and not u.startswith("data:")] == []
    assert not any("85" in u and "000" in u for u in app.requests) and app.tax_requests == 1
    assert "typical Canadian budget" in seen and "popular Canadian budgeting template" in seen
    # the template and its publisher are never named: not on screen, not in any file of the repository
    assert not names_the_template(seen)
    checked = 0
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".pytest_cache", ".git")]
        for name in files:
            if name.endswith((".js", ".html", ".css", ".json", ".md", ".py", ".webmanifest")):
                path = os.path.join(folder, name)
                assert not names_the_template(name + " " + open(path, encoding="utf-8").read()), path
                checked += 1
    assert checked >= 15
    assert names_the_template("xx " + "".join(chr(c) for c in [112, 97, 114, 97, 108, 108, 101, 108]) + " " + "".join(chr(c) for c in [119, 101, 97, 108, 116, 104]))   # the check does bite
    assert app.console_errors == []


# ---------------------------------------------------------------- 11
def test_11_version_and_assets(make_app):
    sw = source("sw.js")
    assert "const VERSION = '0.2.5';" in sw and "const CACHE = 'ds-' + VERSION;" in sw
    assets = re.findall(r"'([^']+)'", sw[sw.index("const ASSETS"):sw.index("];", sw.index("const ASSETS"))])
    assert "tax.js" in assets and "data/tax-ca-2026.json" in assets and len(assets) == 12
    assert "version: '0.2.5'," in source("app.js") and not re.search(r"0\.2\.[01234]\b", sw + source("app.js"))
    app = make_app(service_workers="allow", cards=None, tax=None)
    wait_cached(app.page, cache="ds-0.2.5")
    assert app.page.evaluate("caches.keys()") == ["ds-0.2.5"]
    cached = app.page.evaluate("caches.open('ds-0.2.5').then((c) => c.keys()).then((ks) => ks.map((k) => new URL(k.url).pathname.split('/').slice(-2).join('/')))")
    assert any(k.endswith("/tax.js") for k in cached) and "data/tax-ca-2026.json" in cached
    app.tab("profile")
    assert app.ui.locator("#app-version").inner_text() == "Version 0.2.5"
    assert app.console_errors == []
