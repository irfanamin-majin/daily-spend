"""The v1 acceptance tests (v1 brief, section 8), kept for v2.

Adapted to the multi-file site, the Profile tab (was More), the new payment picker,
the v2 CSV header and the schema 2 state. Test numbers match the v1 brief.
"""
import datetime
import re

import pytest

from conftest import App, SAMPLE_ROWS, cents, make_state

SITE_FILES = ["/", "/styles.css", "/app.js", "/manifest.webmanifest", "/icons/icon-192.png",
              "/icons/apple-touch-icon.png", "/data/cards-ca.json", "/sw.js", "/tax.js", "/data/tax-ca-2026.json"]


def source(name):
    import os
    return open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), name), encoding="utf-8").read()


def site_only(app, urls):
    """Every request is one of the site's own files, and the three core files were loaded."""
    allowed = {app.base_url + p for p in SITE_FILES}
    core = {app.base_url + p for p in SITE_FILES[:3]}
    return set(urls) <= allowed and (core <= set(urls) or len(urls) == 1)


HEADER = ("id,date,amount,category_group,category,payment_method,card,card_last4,merchant,note,tax_tag,"
          "latitude,longitude,location_accuracy_m,created_at,updated_at")
COL = {name: i for i, name in enumerate(HEADER.split(","))}
CAPTURE_CLIPBOARD = """
  window.__copied = null;
  try {
    Object.defineProperty(navigator, 'clipboard', { configurable: true,
      value: { writeText: (t) => { window.__copied = t; return Promise.resolve(); } } });
  } catch (e) {}
"""
THROWING_STORAGE = """
  Object.defineProperty(window, 'localStorage', { configurable: true,
    get() { throw new DOMException('The operation is insecure.', 'SecurityError'); } });
"""
FAKE_CLAUDE = """
  if (window.self !== window.top) {
    window.__saves = []; window.__rejectCode = null; window.__useCalls = [];
    window.claude = { use: async (name) => {
      window.__useCalls.push(name);
      if (name !== 'downloads') return null;
      return { save: async (o) => { window.__saves.push(o); if (window.__rejectCode) throw { code: window.__rejectCode }; } };
    } };
  }
"""


def copied_csv(app):
    app.tab("profile")
    app.ui.locator("#btn-copy").click()
    app.page.wait_for_function("window.__copied !== null")
    text = app.page.evaluate("window.__copied")
    app.page.evaluate("window.__copied = null")
    return text


# ---------------------------------------------------------------- 1
def test_01_first_load(app):
    assert app.ui.locator('.tab[data-tab="add"]').get_attribute("aria-current") == "page"
    assert app.amount() == "$0"
    chips = app.ui.locator("#chips .chip")
    assert chips.count() == 8
    names = app.ui.locator("#chips .chip-name").all_inner_texts()
    assert names == ["Groceries", "Restaurant / Take-Out", "Gas / Diesel", "Shopping", "Transit",
                     "Personal Care", "Medical", "More"]
    for i in range(8):
        assert chips.nth(i).is_visible()
    assert app.ui.locator("#keypad .key").count() == 12
    app.page.wait_for_timeout(600)
    assert app.console_errors == []
    network = [u for u in app.requests if not u.startswith("data:")]
    assert site_only(app, network), network
    assert app.dialogs == []


# ---------------------------------------------------------------- 2
def test_02_add_expense(app):
    app.type_amount("12.34")
    assert app.amount() == "$12.34"
    app.chip("Groceries").click()
    app.save()
    assert app.toast().inner_text() == "Saved $12.34 · Groceries"
    assert app.ui.locator(".toast-undo").is_visible()
    assert app.ui.locator("#toast-region").get_attribute("aria-live") == "polite"
    ex = app.expenses()
    assert len(ex) == 1
    e = ex[0]
    assert e["amountCents"] == 1234 and isinstance(e["amountCents"], int)
    assert e["categoryId"] == "food.groceries" and e["date"] == "2026-11-15"
    assert e["paymentMethodId"] == "credit" and e["merchant"] == "" and e["note"] == ""
    assert app.amount() == "$0"


def test_02b_toast_lasts_five_seconds(app):
    app.add("3", "Transit")
    app.page.wait_for_timeout(4300)
    assert app.toast().count() == 1
    app.page.wait_for_timeout(1200)
    assert app.toast().count() == 0


# ---------------------------------------------------------------- 3
def test_03_undo(app):
    app.add("12.34", "Groceries")
    assert len(app.expenses()) == 1
    app.ui.locator(".toast-undo").click()
    assert app.expenses() == []
    app.tab("history")
    assert "No expenses in November 2026." in app.ui.locator(".empty").inner_text()


# ---------------------------------------------------------------- 4
def test_04_survives_reload(app):
    app.add("12.34", "Groceries")
    app.add("5", "Transit")
    app.reload()
    assert sorted(e["amountCents"] for e in app.expenses()) == [500, 1234]
    app.tab("history")
    assert app.ui.locator('.row[data-act="edit"]').count() == 2
    assert app.ui.locator("#month-total").inner_text() == "$17.34"


# ---------------------------------------------------------------- 5
def test_05_keypad_rules(app):
    app.type_amount("05")
    assert app.amount() == "$5"
    app.ui.locator('[data-key="back"]').click()
    assert app.amount() == "$0"

    app.type_amount(".")
    assert app.amount() == "$0."
    app.type_amount("5")
    assert app.amount() == "$0.5"
    app.type_amount(".")  # second decimal point ignored
    assert app.amount() == "$0.5"
    app.type_amount("67")  # third decimal ignored
    assert app.amount() == "$0.56"
    for _ in range(4):
        app.ui.locator('[data-key="back"]').click()
    assert app.amount() == "$0"

    app.type_amount("1234.5")
    assert app.amount() == "$1,234.5"
    for _ in range(6):
        app.ui.locator('[data-key="back"]').click()

    app.type_amount("999999")  # sixth integer digit ignored
    assert app.amount() == "$99,999"
    app.type_amount(".999")
    assert app.amount() == "$99,999.99"

    # long-press on backspace clears
    back = app.ui.locator('[data-key="back"]')
    box = back.bounding_box()
    app.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    app.page.mouse.down()
    app.page.wait_for_timeout(700)
    app.page.mouse.up()
    assert app.amount() == "$0"

    # zero amount cannot be saved (v2.3: a chip only selects; the Save button stays disabled.
    # force: Playwright refuses to click aria-disabled elements; a finger does not)
    app.chip("Groceries").click()
    save = app.ui.locator("#btn-save")
    assert save.get_attribute("aria-disabled") == "true"
    assert app.ui.locator("#save-hint").inner_text() == "Enter an amount"
    save.click(force=True)
    app.type_amount("0.00")
    assert save.get_attribute("aria-disabled") == "true"
    save.click(force=True)
    assert app.expenses() == []
    assert app.toast().count() == 0


def test_05b_local_date_late_evening(make_app):
    # Late evening in Calgary on Nov 15 is already Nov 16 in UTC.
    a = make_app(now=datetime.datetime(2026, 11, 16, 5, 30, 0, tzinfo=datetime.timezone.utc))
    assert a.page.evaluate("[new Date().getUTCDate(), new Date().getDate()]") == [16, 15]
    a.add("7", "Groceries")
    assert a.expenses()[0]["date"] == "2026-11-15"
    assert "Today" in a.ui.locator("#details-row").inner_text()
    assert "toISOString().slice" not in source("app.js")


# ---------------------------------------------------------------- 6
def test_06_details_sheet(app):
    row = app.ui.locator("#details-row")
    assert "Today · Credit card" in row.inner_text()
    assert "Add merchant or note" in row.inner_text()

    row.click()
    assert app.ui.locator("#d-date").input_value() == "2026-11-15"
    app.ui.locator("#d-date").fill("2026-11-14")
    app.ui.locator('#d-pay label:has-text("Cash")').click()
    app.ui.locator("#d-merchant").fill("Tim Hortons")
    app.ui.locator("#d-note").fill("Double double")
    app.ui.locator("#d-done").click()
    assert app.ui.locator("#sheet-root").is_hidden()
    assert "Yesterday · Cash" in row.inner_text()
    assert "Tim Hortons · Double double" in row.inner_text()

    app.add("2.25", "Restaurant / Take-Out")
    assert app.toast().inner_text() == "Saved $2.25 · Restaurant / Take-Out · Yesterday"
    e = app.expenses()[0]
    assert e["date"] == "2026-11-14" and e["paymentMethodId"] == "cash"
    assert e["merchant"] == "Tim Hortons" and e["note"] == "Double double"

    # reset to today, merchant and note cleared, payment method sticks
    assert "Today · Cash" in row.inner_text()
    assert "Add merchant or note" in row.inner_text()
    assert app.state()["settings"]["lastPayment"] == {"methodId": "cash", "cardId": None}
    app.add("4", "Groceries")
    assert [x for x in app.expenses() if x["amountCents"] == 400][0]["paymentMethodId"] == "cash"
    assert [x for x in app.expenses() if x["amountCents"] == 400][0]["date"] == "2026-11-15"

    # merchant suggestions after one earlier entry
    row.click()
    assert app.ui.locator("#d-date").input_value() == "2026-11-15"
    app.ui.locator("#d-merchant").fill("ti")
    sug = app.ui.locator("#d-suggest button")
    assert sug.all_inner_texts() == ["Tim Hortons"]
    sug.first.click()
    assert app.ui.locator("#d-merchant").input_value() == "Tim Hortons"
    # Escape closes the sheet
    app.page.keyboard.press("Escape")
    assert app.ui.locator("#sheet-root").is_hidden()
    assert "Tim Hortons" in row.inner_text()


def test_06b_suggestion_ranking(app):
    rows = [("2026-11-10", 100, "dining", "credit", m, "") for m in
            ["Costco", "Costco", "Costco", "Co-op", "Co-op", "Tesco", "Tesco", "Tesco", "Tesco",
             "Cobs", "Coles", "Cora", "Conoco"]]
    app.seed(make_state(rows))
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-merchant").fill("CO")
    got = app.ui.locator("#d-suggest button").all_inner_texts()
    assert len(got) == 5
    assert got[:2] == ["Costco", "Co-op"]          # prefix matches by use count
    assert "Tesco" not in got                        # contains match loses to five prefix matches
    app.ui.locator("#d-merchant").fill("s")            # contains matches only, by use count
    assert app.ui.locator("#d-suggest button").all_inner_texts()[:2] == ["Tesco", "Costco"]


# ---------------------------------------------------------------- 7
def test_07_history(app):
    app.seed(make_state(SAMPLE_ROWS))
    app.tab("history")
    assert app.ui.locator("#month-label").inner_text() == "November 2026"
    nov = [r for r in SAMPLE_ROWS if r[0].startswith("2026-11")]
    assert cents(app.ui.locator("#month-total").inner_text()) == sum(r[1] for r in nov)

    days = app.ui.locator("section.day")
    dates = [days.nth(i).get_attribute("data-date") for i in range(days.count())]
    assert dates == sorted({r[0] for r in nov}, reverse=True)
    labels = app.ui.locator(".day-label").all_inner_texts()
    assert labels[:3] == ["Today", "Yesterday", "Fri, Nov 13"]
    for i, d in enumerate(dates):
        want = sum(r[1] for r in nov if r[0] == d)
        assert cents(days.nth(i).locator(".day-total").inner_text()) == want
        row_sum = sum(cents(t) for t in days.nth(i).locator(".row-amount").all_inner_texts())
        assert row_sum == want
    first = days.nth(0).locator(".row").first
    assert "Tim Hortons" in first.inner_text() or "Co-op" in first.inner_text()
    assert app.ui.locator(".row-pay").first.is_visible()

    # other months, and the year in old day headers
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert app.ui.locator("#month-label").inner_text() == "October 2026"
    assert cents(app.ui.locator("#month-total").inner_text()) == 7250 + 5000 + 42000
    for _ in range(10):
        app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert app.ui.locator("#month-label").inner_text() == "December 2025"
    assert app.ui.locator(".day-label").all_inner_texts() == ["Sat, Dec 20, 2025"]
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert "No expenses in November 2025." in app.ui.locator(".empty").inner_text()
    app.ui.locator('.empty [data-tab="add"]').click()
    assert app.ui.locator("#keypad").is_visible()
    app.tab("history")
    for _ in range(12):
        app.ui.locator('[data-act="month"][data-delta="1"]').click()
    assert app.ui.locator("#month-label").inner_text() == "November 2026"

    # edit an amount: totals update, updatedAt is set
    total_before = cents(app.ui.locator("#month-total").inner_text())
    before = [e for e in app.expenses() if e["id"] == "seed-002"][0]
    app.ui.locator('.row[data-id="seed-002"]').click()
    assert app.ui.locator("#e-amount").get_attribute("inputmode") == "decimal"
    assert app.ui.locator("#e-amount").input_value() == "62.30"
    assert app.ui.locator("#e-category option").count() == 45 and app.ui.locator("#e-category optgroup").count() == 8
    app.ui.locator("#e-amount").fill("70.129")       # third decimal dropped by the keypad rules
    assert app.ui.locator("#e-amount").input_value() == "70.12"
    app.ui.locator("#e-amount").fill("0")
    app.ui.locator("#e-save").click()
    assert app.ui.locator("#e-error").inner_text() == "Enter an amount above $0."
    app.ui.locator("#e-amount").fill("70.00")
    app.ui.locator("#e-save").click()
    assert app.ui.locator("#sheet-root").is_hidden()
    after = [e for e in app.expenses() if e["id"] == "seed-002"][0]
    assert after["amountCents"] == 7000 and after["updatedAt"] != before["updatedAt"]
    assert after["createdAt"] == before["createdAt"]
    assert cents(app.ui.locator("#month-total").inner_text()) == total_before - 6230 + 7000
    day = app.ui.locator('section.day[data-date="2026-11-14"]')
    assert cents(day.locator(".day-total").inner_text()) == 7000 + 3899

    # cancel leaves it alone
    app.ui.locator('.row[data-id="seed-002"]').click()
    app.ui.locator("#e-amount").fill("1")
    app.ui.locator("#e-cancel").click()
    assert [e for e in app.expenses() if e["id"] == "seed-002"][0]["amountCents"] == 7000

    # delete asks first
    app.ui.locator('.row[data-id="seed-002"]').click()
    app.ui.locator("#e-delete").click()
    assert app.ui.locator("#e-confirm-text").inner_text() == "Delete this expense?"
    assert len(app.expenses()) == len(SAMPLE_ROWS)
    app.ui.locator("#e-confirm-cancel").click()
    assert app.ui.locator("#e-confirm").is_hidden()
    app.ui.locator("#e-delete").click()
    app.ui.locator("#e-confirm-delete").click()
    assert app.ui.locator("#sheet-root").is_hidden()
    assert len(app.expenses()) == len(SAMPLE_ROWS) - 1
    assert app.ui.locator('.row[data-id="seed-002"]').count() == 0
    assert cents(app.ui.locator("#month-total").inner_text()) == total_before - 6230
    assert app.dialogs == [] and app.console_errors == []


# ---------------------------------------------------------------- 8
def test_08_summary(app):
    app.seed(make_state(SAMPLE_ROWS))
    nov = [r for r in SAMPLE_ROWS if r[0].startswith("2026-11")]
    app.tab("history")
    history_total = cents(app.ui.locator("#month-total").inner_text())
    app.tab("summary")
    assert app.ui.locator("#month-label").inner_text() == "November 2026"
    assert cents(app.ui.locator("#summary-total").inner_text()) == history_total == sum(r[1] for r in nov)
    assert app.ui.locator("#summary-count").inner_text() == f"{len(nov)} expenses"

    # v2.2: the list is by group; each group opens to its items
    amounts = [cents(t) for t in app.ui.locator("#by-group .grp-row .amt").all_inner_texts()]
    assert amounts == sorted(amounts, reverse=True)
    assert sum(amounts) == history_total
    pcts = [int(t.rstrip("%")) for t in app.ui.locator("#by-group .grp-row .pct").all_inner_texts()]
    assert sum(pcts) == 100
    names = app.ui.locator("#by-group .grp-row .name").all_inner_texts()
    assert names[0] == "Housing"
    assert amounts[names.index("Food")] == 8412 + 9575 + 475 + 3899
    assert app.ui.locator("#by-group .grp-row .bar").count() == len(names)
    app.ui.locator('#by-group .grp-row:has-text("Food")').click()
    items = dict(zip(app.ui.locator("#by-group .item-row .name").all_inner_texts(),
                     [cents(t) for t in app.ui.locator("#by-group .item-row .amt").all_inner_texts()]))
    assert items == {"Groceries": 8412 + 9575, "Restaurant / Take-Out": 475 + 3899}
    app.ui.locator('#by-group .grp-row:has-text("Food")').click()

    card = app.ui.locator("#tax-card")
    assert card.locator(".card-title").inner_text() == "Tax time 2026"
    y = [r for r in SAMPLE_ROWS if r[0].startswith("2026")]
    assert cents(card.locator('[data-tax="medical"] .v').inner_text()) == sum(r[1] for r in y if r[2] == "medical") == 28400
    assert cents(card.locator('[data-tax="donation"] .v').inner_text()) == sum(r[1] for r in y if r[2] == "donations") == 7150
    assert cents(card.locator('[data-tax="childcare"] .v').inner_text()) == 42000
    assert "Totals of tagged categories. Only private health plan premiums count; provincial plan premiums don't." in card.inner_text()

    # previous year card
    for _ in range(11):
        app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert card.locator(".card-title").inner_text() == "Tax time 2025"
    assert cents(card.locator('[data-tax="medical"] .v').inner_text()) == 12000


# ---------------------------------------------------------------- 9
TRICKY = [
    ("2026-11-02", 123450, "groceries", "debit", 'Joe\'s "Fresh" Market, Inc.', "line one\nline two, with comma"),
    ("2026-11-03", 999, "dining", "cash", "=SUM(A1:A9)", "+1 403 555 0100"),
    ("2026-11-03", 1, "gas", "pad", "-minus", "@handle"),
    ("2026-11-01", 9999999, "medical", "etransfer", "Plain", "Café 🍔 naïve"),
]


def parse_csv(text):
    import csv, io
    return list(csv.reader(io.StringIO(text, newline="")))


def test_09_csv_export(make_app):
    app = make_app(init_scripts=[CAPTURE_CLIPBOARD])
    app.seed(make_state(TRICKY))
    text = copied_csv(app)
    assert "Backup copied (4 expenses)" in app.toast().inner_text()
    assert not text.startswith("﻿")
    lines = text.split("\r\n")
    assert lines[0] == HEADER
    assert text.endswith("\r\n") and "\r\n" in text
    rows = parse_csv(text)
    assert rows[0] == HEADER.split(",")
    body = rows[1:]
    assert len(body) == 4
    assert [r[1] for r in body] == ["2026-11-01", "2026-11-02", "2026-11-03", "2026-11-03"]  # date, then createdAt
    assert [r[2] for r in body] == ["99999.99", "1234.50", "9.99", "0.01"]
    M, N, T, P = COL["merchant"], COL["note"], COL["tax_tag"], COL["payment_method"]
    assert [body[0][i] for i in (COL["category"], P, M, N, T)] == ["Medical", "e-Transfer (Interac)", "Plain", "Café 🍔 naïve", "medical"]
    assert body[0][COL["card"]] == "" and body[0][COL["latitude"]] == "" and len(body[0]) == len(COL)
    assert body[1][M] == 'Joe\'s "Fresh" Market, Inc.'
    assert body[1][N] == "line one\nline two, with comma"
    assert '"Joe\'s ""Fresh"" Market, Inc."' in text
    assert body[2][M] == "'=SUM(A1:A9)" and body[2][N] == "'+1 403 555 0100"
    assert body[3][M] == "'-minus" and body[3][N] == "'@handle"
    assert body[1][P] == "Debit card" and body[3][P] == "Pre-authorised debit"
    assert body[1][T] == ""

    # standalone download: BOM, filename, same content
    assert app.ui.locator("#btn-download").is_visible()
    with app.page.expect_download() as info:
        app.ui.locator("#btn-download").click()
    dl = info.value
    assert dl.suggested_filename == "daily-spend-2026-11-15.csv"
    raw = open(dl.path(), "rb").read()
    assert raw[:3] == b"\xef\xbb\xbf"
    assert raw[3:].decode("utf-8") == text
    assert app.console_errors == []


# ---------------------------------------------------------------- 10
def test_10_restore(make_app):
    src = make_app(init_scripts=[CAPTURE_CLIPBOARD])
    src.seed(make_state(TRICKY + SAMPLE_ROWS[:6]))
    # a custom tagged category must come back too
    src.tab("profile")
    src.cat_add()
    src.ui.locator("#c-name").fill("Vet")
    src.ui.locator('#c-tags label:has-text("Medical")').click()
    src.ui.locator("#c-save").click()
    src.close_sheet()
    src.tab("add")
    src.type_amount("88")
    src.more_pick("Vet")
    src.save()
    text = copied_csv(src)
    original = src.expenses()
    assert len(original) == 11

    dst = make_app()
    assert dst.expenses() == []
    dst.tab("profile")
    dst.ui.locator("#btn-restore").click()
    dst.ui.locator("#r-text").fill(text)
    dst.ui.locator("#r-go").click()
    assert dst.ui.locator("#r-result").inner_text() == "Restored 11 expenses. Skipped 0 already here and 0 invalid rows."
    key = lambda e: e["id"]
    fields = ["id", "amountCents", "date", "paymentMethodId", "merchant", "note", "createdAt", "updatedAt"]
    got = sorted(dst.expenses(), key=key)
    want = sorted(original, key=key)
    assert [[e[f] for f in fields] for e in got] == [[e[f] for f in fields] for e in want]
    name = lambda st, e: [c for c in st["categories"] if c["id"] == e["categoryId"]][0]["name"]
    assert [name(dst.state(), e) for e in got] == [name(src.state(), e) for e in want]
    vet = [c for c in dst.state()["categories"] if c["name"] == "Vet"][0]
    assert vet["taxTag"] == "medical" and vet["builtIn"] is False and vet["emoji"] == "📦"

    # second restore, this time through the file input with a BOM: everything is already here
    import os, tempfile
    path = os.path.join(tempfile.mkdtemp(), "backup.csv")
    with open(path, "wb") as f:
        f.write(b"\xef\xbb\xbf" + text.encode("utf-8"))
    dst.ui.locator("#r-file").set_input_files(path)
    dst.ui.locator("#r-result").filter(has_text="Skipped 11").wait_for()
    assert dst.ui.locator("#r-result").inner_text() == "Restored 0 expenses. Skipped 11 already here and 0 invalid rows."
    assert len(dst.expenses()) == 11
    assert len(dst.state()["categories"]) == 46

    # invalid rows are counted; LF endings, shuffled columns, missing optional columns
    mixed = "\n".join([
        "Amount,DATE,Category,merchant,payment_method,tax_tag",
        "10.00,2026-11-05,Groceries,Ok one,cash,",
        "5.5,2026-02-29,Groceries,Bad date,,",          # not a real date
        "0,2026-11-05,Groceries,Zero,,",                # not above zero
        "100000.00,2026-11-05,Groceries,Too big,,",     # above the maximum
        "1.234,2026-11-05,Groceries,Three decimals,,",
        "3.00,2026-11-05,,No category,,",
        "abc,2026-11-05,Groceries,Not a number,,",
        '7.25,2026-11-06,Pet care,"\'=Quoted, name",DEBIT,donation',
        "2.00,2026-11-07,gRoCeRiEs,Case,Nonsense,",
    ]) + "\n"
    dst.ui.locator("#r-text").fill(mixed)
    dst.ui.locator("#r-go").click()
    assert dst.ui.locator("#r-result").inner_text() == "Restored 3 expenses. Skipped 0 already here and 6 invalid rows."
    st = dst.state()
    assert len(st["expenses"]) == 14
    pet = [c for c in st["categories"] if c["name"] == "Pet care"][0]
    assert pet["taxTag"] == "donation"
    new = {e["merchant"]: e for e in st["expenses"] if e["merchant"] in ("Ok one", "=Quoted, name", "Case")}
    assert new["Ok one"]["paymentMethodId"] == "cash" and new["Ok one"]["amountCents"] == 1000
    assert new["=Quoted, name"]["paymentMethodId"] == "debit" and new["=Quoted, name"]["categoryId"] == pet["id"]
    assert new["Case"]["paymentMethodId"] == "other" and new["Case"]["categoryId"] == "food.groceries"
    assert all(e["id"] for e in st["expenses"]) and len({e["id"] for e in st["expenses"]}) == 14

    # not a backup at all
    dst.ui.locator("#r-text").fill("hello,world\n1,2\n")
    dst.ui.locator("#r-go").click()
    assert "doesn't look like a Daily Spend backup" in dst.ui.locator("#r-error").inner_text()
    assert len(dst.expenses()) == 14
    assert dst.console_errors == [] and dst.dialogs == []


# ---------------------------------------------------------------- 11
def test_11_categories(app):
    app.tab("profile")
    app.cat_add()
    assert app.ui.locator("#c-emoji").input_value() == "📦"
    assert app.ui.locator("#c-name").get_attribute("maxlength") == "32"
    app.ui.locator("#c-save").click()
    assert app.ui.locator("#c-error").inner_text() == "Enter a name."
    app.ui.locator("#c-name").fill("groceries")
    app.ui.locator("#c-save").click()
    assert "already a category" in app.ui.locator("#c-error").inner_text()
    app.ui.locator("#c-name").fill("Physio")
    app.ui.locator("#c-emoji").fill("abc")
    app.ui.locator("#c-save").click()
    assert app.ui.locator("#c-error").inner_text() == "Use one or two emoji."
    app.ui.locator("#c-emoji").fill("🏃‍♀️")
    app.ui.locator('#c-tags label:has-text("Medical")').click()
    app.ui.locator("#c-save").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Miscellaneous"            # back on the section's list
    assert "Medical" in app.cat_row("Physio").inner_text()
    app.close_sheet()
    assert app.ui.locator("#sheet-root").is_hidden()

    # appears in the More picker (by section, and in search with its tag) and saves from there
    app.tab("add")
    app.type_amount("60")
    app.ui.locator(".chip-more").click()
    sections = app.browser_sections()
    assert len(sections) == 8 and sum(len(names) for _, names in sections) == 46       # by section, not alphabetical
    assert "Physio" in dict(sections)["misc"]
    app.ui.locator("#cp-search").fill("physio")
    item = app.ui.locator('#cp-results .row:has-text("Physio")')
    assert "Medical" in item.locator(".badge").inner_text()
    app.ui.locator("#cp-search").fill("donations")
    assert app.ui.locator('#cp-results .row:has-text("Donations") .badge').inner_text() == "Donation"
    app.ui.locator("#cp-search").fill("physio")
    item.click()
    app.save()
    assert app.toast().inner_text() == "Saved $60.00 · Physio"

    # counts in Tax time together with the built-in medical category
    app.add("40", "Groceries")
    app.type_amount("25.50")
    app.more_pick(cat_id="misc.medical")
    app.save()
    app.tab("summary")
    assert cents(app.ui.locator('#tax-card [data-tax="medical"] .v').inner_text()) == 6000 + 2550

    # hide Groceries: gone from chips and the More sheet, still in History and Summary
    app.tab("profile")
    app.cat_edit("Groceries")
    app.ui.locator("#c-hidden").check()
    app.ui.locator("#c-save").click()
    assert "Hidden" in app.cat_row("Groceries").inner_text()
    app.close_sheet()
    app.tab("add")
    chip_names = app.ui.locator("#chips .chip-name").all_inner_texts()
    assert "Groceries" not in chip_names and len(chip_names) == 8
    app.type_amount("1")
    app.ui.locator(".chip-more").click()
    assert "Groceries" not in dict(app.browser_sections())["food"]
    app.ui.locator("#cp-search").fill("groceries")
    assert app.ui.locator("#cp-results").count() == 0 and app.ui.locator("#cp-status").inner_text() == 'No categories match "groceries".'
    app.page.keyboard.press("Escape")
    app.tab("history")
    assert app.ui.locator('.row[data-act="edit"]:has-text("Groceries")').count() == 1
    app.ui.locator('.row[data-act="edit"]:has-text("Groceries")').click()
    assert "Groceries (hidden)" in app.ui.locator("#e-category option:checked").inner_text()
    app.ui.locator("#e-cancel").click()
    app.tab("summary")
    app.ui.locator('#by-group .grp-row:has-text("Food")').click()
    assert "Groceries" in app.ui.locator("#by-group .item-row .name").all_inner_texts()

    # most recent first: Medical (logged last), then Physio; hidden Groceries is skipped, then the unused defaults
    app.tab("add")
    assert app.ui.locator("#chips .chip-name").all_inner_texts()[:3] == ["Medical", "Physio", "Restaurant / Take-Out"]

    # a built-in has no delete; a used custom one cannot be deleted; an unused one can
    app.tab("profile")
    app.cat_edit("Transit")
    assert app.ui.locator("#c-delete").count() == 0
    app.page.keyboard.press("Escape")                                                # up a level: Transportation's list
    assert app.ui.locator("#sheet-title").inner_text() == "Transportation"
    app.cat_edit("Physio")
    assert app.ui.locator("#c-delete").count() == 0
    app.page.keyboard.press("Escape")
    app.cat_add()
    app.ui.locator("#c-name").fill("Temp")
    app.ui.locator("#c-save").click()
    app.cat_edit("Temp")
    app.ui.locator("#c-delete").click()
    app.ui.locator("#c-confirm-delete").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Miscellaneous" and app.toast().inner_text() == "Category deleted"
    assert app.ui.locator('#cm-list .row:has-text("Temp")').count() == 0
    assert len(app.state()["categories"]) == 46
    assert app.console_errors == []


# ---------------------------------------------------------------- 12
def test_12_delete_all(app):
    app.seed(make_state(SAMPLE_ROWS, test_notice_dismissed=True))
    app.tab("profile")
    app.cat_add()
    app.ui.locator("#c-name").fill("Custom")
    app.ui.locator("#c-save").click()
    app.close_sheet()
    assert app.ui.locator("#category-summary").inner_text() == "46 categories in 8 sections"
    app.ui.locator("#btn-delete-all").click()
    go = app.ui.locator("#da-go")
    assert go.is_disabled()
    for text in ["delete", "DELET", "DELETE "]:
        app.ui.locator("#da-input").fill(text)
        assert go.is_disabled()
    # a backdrop tap must not close this sheet
    app.page.mouse.click(195, 40)
    assert app.ui.locator("#da-input").is_visible()
    app.ui.locator("#da-input").fill("DELETE")
    assert go.is_enabled()
    go.click()
    assert app.ui.locator("#sheet-root").is_hidden()
    st = app.state()
    assert st["expenses"] == []
    assert len(st["categories"]) == 45 and all(c["builtIn"] and not c["hidden"] for c in st["categories"])
    assert st["settings"] == {"lastPayment": {"methodId": "credit", "cardId": None}, "testNoticeDismissed": False,
                              "autoLocation": False, "mapsNoticeShown": False, "onboarded": False, "groupsNotice": False,
                              "pay": None, "paySkipped": False}
    assert st["cards"] == [] and st["schemaVersion"] == 3
    assert app.ui.locator("#category-summary").inner_text() == "45 categories in 8 sections"
    app.tab("history")
    assert "No expenses in November 2026." in app.ui.locator(".empty").inner_text()
    assert app.dialogs == []


def test_12b_backdrop_closes_other_sheets(app):
    app.ui.locator("#details-row").click()
    assert app.ui.locator("#d-done").is_visible()
    app.page.mouse.click(195, 40)
    assert app.ui.locator("#sheet-root").is_hidden()


# ---------------------------------------------------------------- 13
def test_13_storage_blocked(make_app):
    app = make_app(init_scripts=[THROWING_STORAGE, CAPTURE_CLIPBOARD])
    banner = app.ui.locator("#banner-memory")
    assert banner.inner_text().startswith("Not saving: this browser blocked storage.")
    app.add("12.34", "Groceries")
    assert app.toast().inner_text() == "Saved $12.34 · Groceries"
    app.add("5", "Transit")
    for tab in ["history", "summary", "profile", "add"]:
        app.tab(tab)
        assert banner.is_visible()
    app.tab("history")
    assert app.ui.locator('.row[data-act="edit"]').count() == 2
    assert app.ui.locator("#month-total").inner_text() == "$17.34"
    app.ui.locator('.row[data-act="edit"]:has-text("Transit")').click()
    app.ui.locator("#e-amount").fill("6")
    app.ui.locator("#e-save").click()
    assert app.ui.locator("#month-total").inner_text() == "$18.34"
    app.tab("summary")
    assert app.ui.locator("#summary-total").inner_text() == "$18.34"
    app.tab("profile")
    assert app.ui.locator("#storage-status").inner_text().startswith("Not saving")
    assert len(copied_csv(app).strip().split("\r\n")) == 3
    assert app.console_errors == [] and app.dialogs == []


def test_13b_setitem_throws_and_corrupt_data(make_app):
    # Quota style failure: reading works, writing throws.
    a = make_app(init_scripts=["Storage.prototype.setItem = function () { throw new DOMException('full', 'QuotaExceededError'); };"])
    assert a.ui.locator("#banner-memory").is_visible()
    a.add("1", "Groceries")
    a.tab("history")
    assert a.ui.locator('.row[data-act="edit"]').count() == 1

    # Unparseable JSON: keep a copy, start fresh, warn.
    b = make_app()
    b.page.evaluate("localStorage.setItem('dailyspend.state', '{not json')")
    b.reload()
    assert "could not be read" in b.ui.locator("#banner-corrupt").inner_text()
    keys = b.page.evaluate("Object.keys(localStorage)")
    kept = [k for k in keys if k.startswith("dailyspend.state.corrupt.")]
    assert len(kept) == 1
    assert b.page.evaluate("k => localStorage.getItem(k)", kept[0]) == "{not json"
    b.add("2", "Groceries")
    assert len(b.expenses()) == 1
    assert b.console_errors == []


# ---------------------------------------------------------------- 14
def embedded(make_app, **kw):
    app = make_app(open_page=False, **kw)
    app.ui = app.page.frame_locator("#app-frame")
    app.goto("/tests/embed.html")
    return app


def test_14_embedded_harness(make_app):
    app = embedded(make_app)
    frame = app.page.frames[1]
    sandbox = app.page.locator("#app-frame").get_attribute("sandbox")
    assert sandbox == "allow-scripts allow-same-origin allow-forms"
    assert app.page.locator("#app-frame").get_attribute("allow") == "clipboard-write"
    assert frame.evaluate("window.self !== window.top")
    assert frame.evaluate("typeof window.claude") == "undefined"

    # test notice shows and can be dismissed for good
    notice = app.ui.locator("#banner-test")
    assert notice.inner_text().strip().startswith(
        "Test version: entries are kept in this browser only and may be cleared. Copy a backup from Profile.")

    # full add, edit and delete flow
    app.add("12.34", "Groceries")
    assert app.toast().inner_text() == "Saved $12.34 · Groceries"
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-merchant").fill("Co-op")
    app.ui.locator("#d-done").click()
    app.add("20", "Transit")
    state = lambda: frame.evaluate("JSON.parse(localStorage.getItem('dailyspend.state'))")
    assert len(state()["expenses"]) == 2
    app.tab("history")
    assert app.ui.locator("#month-total").inner_text() == "$32.34"
    app.ui.locator('.row[data-act="edit"]:has-text("Transit")').click()
    app.ui.locator("#e-amount").fill("25.5")
    app.ui.locator("#e-category").select_option("food.restaurant-take-out")
    app.ui.locator("#e-save").click()
    assert app.ui.locator("#month-total").inner_text() == "$37.84"
    assert app.ui.locator('.row[data-act="edit"]:has-text("Restaurant / Take-Out")').count() == 1
    app.ui.locator('.row[data-act="edit"]:has-text("Groceries")').click()
    app.ui.locator("#e-delete").click()
    assert app.ui.locator("#e-confirm-text").inner_text() == "Delete this expense?"
    app.ui.locator("#e-confirm-delete").click()
    assert app.ui.locator("#month-total").inner_text() == "$25.50"
    assert len(state()["expenses"]) == 1

    # More: storage line, Download hidden (no window.claude), Copy works or falls back
    app.tab("profile")
    assert app.ui.locator("#storage-status").inner_text().startswith("Saved in this browser only.")
    app.page.wait_for_timeout(400)
    assert app.ui.locator("#btn-download").is_hidden()
    app.ui.locator("#btn-copy").click()
    app.ui.locator("#toast-region .toast-text, #copy-fallback").first.wait_for()
    if app.ui.locator("#copy-fallback").count():
        outcome = "fallback textarea"
        value = app.ui.locator("#copy-fallback").input_value()
        assert value.startswith("id,date,amount,category") and "25.50" in value
        assert app.ui.locator("#copy-fallback").get_attribute("readonly") is not None
        assert "Select all and copy" in app.ui.locator(".sheet .help").inner_text()
        app.ui.locator("#copy-select").click()
        assert frame.evaluate("document.activeElement.selectionEnd - document.activeElement.selectionStart") == len(value)
        app.ui.locator("[data-sheet-close]").first.click()
    else:
        outcome = "clipboard"
        assert "Backup copied (1 expense)" in app.toast().inner_text()
    print("test 14 copy outcome:", outcome)

    notice.locator("button").click()
    assert notice.count() == 0
    assert state()["settings"]["testNoticeDismissed"] is True
    app.reload()
    assert app.ui.locator("#banner-test").count() == 0

    assert app.dialogs == [] and app.console_errors == []
    network = [u for u in app.requests if not u.startswith("data:")]
    assert set(network) == {app.base_url + "/tests/embed.html"} | set(n for n in network if site_only(app, [n])), network


def test_14b_copy_refused_falls_back(make_app):
    refuse = """Object.defineProperty(navigator, 'clipboard', { configurable: true,
      value: { writeText: () => Promise.reject(new DOMException('denied', 'NotAllowedError')) } });"""
    app = embedded(make_app, init_scripts=[refuse])
    app.add("9.99", "Groceries")
    app.tab("profile")
    app.ui.locator("#btn-copy").click()
    assert app.ui.locator("#copy-fallback").input_value().startswith("id,date,amount,category")
    assert app.console_errors == []

    # clipboard API missing entirely
    app2 = make_app(init_scripts=["Object.defineProperty(navigator, 'clipboard', { configurable: true, value: undefined });"])
    app2.tab("profile")
    app2.ui.locator("#btn-copy").click()
    assert app2.ui.locator("#copy-fallback").is_visible()
    assert app2.console_errors == []


def test_14c_platform_downloads_capability(make_app):
    app = embedded(make_app, init_scripts=[FAKE_CLAUDE])
    frame = app.page.frames[1]
    app.add("12.34", "Groceries")
    app.tab("profile")
    btn = app.ui.locator("#btn-download")
    btn.wait_for()
    assert frame.evaluate("window.__useCalls") == ["downloads"]
    btn.click()
    app.ui.locator('#toast-region .toast-text:has-text("Backup saved")').wait_for()
    saved = frame.evaluate("window.__saves[0]")
    assert saved["filename"] == "daily-spend-2026-11-15.csv"
    assert saved["data"].startswith("﻿id,date,amount,category_group,category,payment_method,card,")
    assert "12.34" in saved["data"]

    frame.evaluate("window.__rejectCode = 'declined'")
    app.page.wait_for_timeout(3200)            # let the earlier toast expire
    btn.click()
    app.page.wait_for_timeout(300)
    assert app.toast().count() == 0 and btn.is_visible()

    frame.evaluate("window.__rejectCode = 'rate_limited'")
    btn.click()
    app.ui.locator('#toast-region .toast-text:text-is("Try again in a moment")').wait_for()
    assert btn.is_visible()

    frame.evaluate("window.__rejectCode = 'unsupported'")
    btn.click()
    app.ui.locator('#toast-region .toast-text:text-is("Download isn\'t available here. Use Copy backup instead.")').wait_for()
    assert btn.is_hidden()
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 15
LAYOUT_CHECK = """
() => {
  const W = window.innerWidth, H = window.innerHeight, bad = [];
  const doc = document.documentElement;
  if (doc.scrollWidth > W) bad.push('page scrolls sideways: ' + doc.scrollWidth);
  if (doc.scrollHeight > H) bad.push('page scrolls vertically: ' + doc.scrollHeight);
  const sheetOpen = !document.getElementById('sheet-root').hidden;
  const roots = sheetOpen ? ['#sheet-root .sheet'] : ['#app'];
  const name = (n) => n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') + (n.className && n.className.baseVal === undefined ? '.' + String(n.className).split(' ')[0] : '');
  roots.forEach((sel) => document.querySelectorAll(sel + ', ' + sel + ' *').forEach((n) => {
    const r = n.getBoundingClientRect();
    if (!r.width || !r.height) return;
    if (getComputedStyle(n).visibility === 'hidden') return;
    if (r.left < -0.5 || r.right > W + 0.5) bad.push('outside viewport sideways: ' + name(n) + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
    const cs = getComputedStyle(n);
    const clipsX = cs.overflowX !== 'visible' && cs.textOverflow !== 'ellipsis';
    if (clipsX && n.scrollWidth > n.clientWidth + 1 && n.tagName !== 'TEXTAREA' && n.tagName !== 'INPUT' && n.tagName !== 'SELECT')
      bad.push('clipped sideways: ' + name(n) + ' ' + n.scrollWidth + '>' + n.clientWidth);
  }));
  // fixed chrome stays on screen
  ['.topbar', '.tabbar'].forEach((sel) => {
    const r = document.querySelector(sel).getBoundingClientRect();
    if (r.top < -0.5 || r.bottom > H + 0.5) bad.push(sel + ' off screen');
  });
  if (sheetOpen) {
    const r = document.querySelector('#sheet-root .sheet').getBoundingClientRect();
    if (r.top < -0.5 || r.bottom > H + 0.5) bad.push('sheet off screen ' + r.top + '..' + r.bottom);
  }
  // text not cut off inside chips, keys, tabs and buttons
  document.querySelectorAll('.chip-name, .key, .tab span, .btn, .option span, .badge, .month-label, .big').forEach((n) => {
    if (!n.getClientRects().length) return;
    if (n.scrollHeight > n.clientHeight + 1 || n.scrollWidth > n.clientWidth + 1) bad.push('text clipped: ' + name(n) + ' "' + n.textContent.trim().slice(0, 24) + '"');
  });
  // tap targets
  const scope = sheetOpen ? '#sheet-root .sheet' : '#app';
  document.querySelectorAll(scope + ' button, ' + scope + ' .option, ' + scope + ' input:not([type=radio]):not([type=checkbox]), ' + scope + ' select').forEach((n) => {
    const r = n.getBoundingClientRect();
    if (!r.width) return;
    if (r.width < 43.5 || r.height < 43.5) bad.push('small tap target: ' + name(n) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
    if (/^(INPUT|SELECT|TEXTAREA)$/.test(n.tagName) && parseFloat(getComputedStyle(n).fontSize) < 16) bad.push('input font below 16px: ' + name(n));
  });
  return bad;
}
"""
ADD_FITS = """
() => {
  const v = document.getElementById('view'), bad = [];
  if (v.scrollHeight > v.clientHeight + 1) bad.push('Add needs scrolling: ' + v.scrollHeight + '>' + v.clientHeight);
  // v2.3 lets keys and chips shrink on short phones, down to the 44 px tap target, to make room for Save
  document.querySelectorAll('.key, .chip').forEach((k) => { if (k.getBoundingClientRect().height < 44) bad.push('key or chip under 44px'); });
  const save = document.getElementById('btn-save').getBoundingClientRect();
  if (save.height < 44 || save.bottom > document.querySelector('.tabbar').getBoundingClientRect().top + 0.5) bad.push('Save button not fully above the tab bar');
  const tab = document.querySelector('.tabbar').getBoundingClientRect();
  const pad = document.getElementById('keypad').getBoundingClientRect();
  if (pad.bottom > save.top + 0.5) bad.push('keypad under the Save button');
  if (getComputedStyle(document.querySelector('.key')).touchAction !== 'manipulation') bad.push('touch-action');
  return bad;
}
"""
SIZES = [(375, 667), (390, 844), (430, 932), (360, 800)]


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("size", SIZES, ids=lambda s: f"{s[0]}x{s[1]}")
def test_15_layout(make_app, size, scheme):
    app = make_app(width=size[0], height=size[1], scheme=scheme, reduced_motion="reduce")
    long_rows = SAMPLE_ROWS + [
        ("2026-11-15", 9999999, "utilities", "pad", "A very long merchant name that keeps going and going on",
         "And an equally long note that should be truncated rather than pushing the amount off the screen"),
    ]
    app.seed(make_state(long_rows))
    want_bg = "rgb(250, 253, 252)" if scheme == "light" else "rgb(0, 0, 0)"      # v2.4: pastel light theme
    assert app.page.evaluate("getComputedStyle(document.body).backgroundColor") == want_bg

    def check(label):
        bad = app.page.evaluate(LAYOUT_CHECK)
        assert bad == [], f"{label} at {size} {scheme}: {bad}"

    check("add")
    assert app.page.evaluate(ADD_FITS) == []
    app.type_amount("99999.99")
    check("add typed")
    assert app.page.evaluate(ADD_FITS) == []
    box = app.ui.locator("#amount").bounding_box()
    assert box["x"] >= 0 and box["x"] + box["width"] <= size[0]
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-merchant").fill("C")
    check("details sheet")
    app.page.keyboard.press("Escape")
    app.ui.locator(".chip-more").click()
    app.page.wait_for_timeout(250)
    check("category picker")
    app.ui.locator('#cp-tiles [data-section="misc"]').click()
    app.page.wait_for_timeout(300)
    check("category picker section")
    app.close_sheet()
    app.chip("Groceries").click()
    app.save()
    check("toast")
    t = app.ui.locator(".toast").bounding_box()
    assert t["x"] >= 0 and t["x"] + t["width"] <= size[0] and t["y"] >= 0

    app.tab("history")
    check("history")
    app.ui.locator('.row[data-act="edit"]').first.click()
    check("edit sheet")
    app.ui.locator("#e-delete").scroll_into_view_if_needed()
    app.ui.locator("#e-delete").click()
    check("edit confirm")
    app.page.keyboard.press("Escape")
    app.tab("summary")
    check("summary")
    app.tab("profile")
    check("profile")
    for opener in ["#btn-restore", "#btn-modify-categories", "#btn-delete-all"]:
        app.ui.locator(opener).scroll_into_view_if_needed()
        app.ui.locator(opener).click()
        check(opener)
        app.page.keyboard.press("Escape")
    assert app.console_errors == []


def test_15b_embedded_layout_with_notice(make_app):
    app = embedded(make_app, width=375, height=667)
    frame = app.page.frames[1]
    assert frame.evaluate(LAYOUT_CHECK) == []
    assert app.ui.locator("#banner-test").is_visible()


# ---------------------------------------------------------------- extras
def test_16_focus_trap_and_labels(app):
    app.ui.locator("#details-row").click()
    for _ in range(14):
        app.page.keyboard.press("Tab")
        assert app.page.evaluate("document.querySelector('#sheet-root .sheet').contains(document.activeElement)")
    for _ in range(14):
        app.page.keyboard.press("Shift+Tab")
        assert app.page.evaluate("document.querySelector('#sheet-root .sheet').contains(document.activeElement)")
    assert app.page.evaluate("document.querySelector('.sheet').getAttribute('role')") == "dialog"
    app.page.keyboard.press("Escape")
    unlabelled = app.page.evaluate("""() => Array.from(document.querySelectorAll('#app button'))
      .filter((b) => !(b.getAttribute('aria-label') || b.textContent.trim())).length""")
    assert unlabelled == 0
    assert app.ui.locator('[data-key="back"]').get_attribute("aria-label").startswith("Backspace")


def test_17_no_forbidden_apis_in_source():
    app_js, sw_js, tax_js = source("app.js"), source("sw.js"), source("tax.js")
    html, css = source("index.html"), source("styles.css")
    everything = "\n".join([app_js, sw_js, tax_js, html, css])
    for pattern in [r"\balert\s*\(", r"\bconfirm\s*\(", r"\bprompt\s*\(", r"window\.print", r"window\.open",
                    r"XMLHttpRequest", r"WebSocket", r"sendBeacon", r"EventSource", r"importScripts",
                    r"location\.hash", r"<datalist", r"@import", r"url\((?!\"?data:)", r"\beval\s*\(", r"new Function"]:
        assert not re.search(pattern, everything), pattern
    # The only absolute addresses: the SVG namespace and the Google Maps link the user taps.
    urls = set(re.findall(r"https?://[^\s'\"`<>)]+", everything))
    assert urls <= {"http://www.w3.org/2000/svg", "https://www.google.com/maps/search/?api=1&query="}, urls
    # One network call in the page (the site's own card list) and one in the worker (same-origin files).
    # (v2.4: one helper fetches the site's own JSON files: the card list and the tax figures)
    assert re.findall(r"\bfetch\s*\(([^,)]*)", app_js) == ["url"]
    assert sorted(re.findall(r"fetchJson\((\w+)\)", app_js)) == ["CARDS_URL", "TAX_DATA_URL", "url"]
    assert "const CARDS_URL = 'data/cards-ca.json';" in app_js and "const TAX_DATA_URL = 'data/tax-ca-2026.json';" in app_js
    # the estimator is pure: no page, storage or network access
    assert not re.search(r"document\.|localStorage|\bfetch\b|navigator\.", tax_js)
    assert len(re.findall(r"\bfetch\s*\(", sw_js)) == 1 and "self.location.origin" in sw_js
    # No inline script or style element; every file reference is relative.
    assert not re.search(r"<script(?![^>]*\bsrc=)", html) and "<style" not in html
    assert html.index('src="tax.js" defer') < html.index('src="app.js" defer')
    for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
        assert not re.match(r"([a-z]+:|/)", ref), ref
    assert "Content-Security-Policy" in html and "default-src 'self'" in html
    # toISOString appears once, for createdAt/updatedAt timestamps only
    assert app_js.count("toISOString") == 1


# ---------------------------------------------------------------- review round 2
def test_18_chip_order_is_fixed_on_the_add_screen(app):
    chips = lambda: app.ui.locator("#chips .chip-name").all_inner_texts()
    start = chips()
    assert "Travel / Vacation" not in start
    for amount in ["10", "20", "30"]:
        app.type_amount(amount)
        app.more_pick("Travel / Vacation")
        app.save()
        assert chips() == start
    assert len(app.expenses()) == 3
    app.ui.locator(".toast-undo").click()                 # undo does not reorder either
    assert chips() == start
    app.tab("history")                                    # arriving from another tab re-ranks: most recent first
    app.ui.locator('.row[data-act="edit"]').first.click()
    app.ui.locator("#e-amount").fill("11")
    app.ui.locator("#e-save").click()
    app.tab("add")
    assert chips() == ["Travel / Vacation"] + start[:6] + ["More"]
    app.reload()
    assert chips() == ["Travel / Vacation"] + start[:6] + ["More"]
    # a hidden category drops out
    app.tab("profile")
    app.cat_edit("Travel / Vacation")
    app.ui.locator("#c-hidden").check()
    app.ui.locator("#c-save").click()
    app.close_sheet()
    app.tab("add")
    assert chips() == start


def test_19_keyboard_overlap_variable_and_sheets(app):
    overlap = lambda: app.page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--kb-overlap').trim()")
    assert overlap() == "0px"
    app.ui.locator("#details-row").click()
    assert overlap() == "0px"
    app.ui.locator("#d-note").focus()
    app.page.wait_for_timeout(450)
    box = app.ui.locator(".sheet").bounding_box()
    assert box["y"] >= 0 and abs(box["y"] + box["height"] - 844) < 1
    # simulated keyboard: the sheet lifts and its height is capped to the visible area
    app.page.evaluate("document.documentElement.style.setProperty('--kb-overlap', '300px')")
    box = app.ui.locator(".sheet").bounding_box()
    assert abs(box["y"] + box["height"] - 544) < 1 and box["y"] >= 12 - 1
    app.ui.locator("#d-done").scroll_into_view_if_needed()
    app.ui.locator("#d-done").click()
    assert app.ui.locator("#sheet-root").is_hidden()
    assert overlap() == "0px"                             # reset when the sheet closes
    app.tab("profile")
    app.ui.locator("#btn-restore").click()
    assert app.ui.locator("#r-text").is_visible()
    app.page.keyboard.press("Escape")
    assert app.ui.locator("#sheet-root").is_hidden() and overlap() == "0px"
    # no visualViewport at all: still works
    b = App(app.page.context.browser, app.base_url,
            init_scripts=["Object.defineProperty(window, 'visualViewport', { configurable: true, value: undefined });"])
    try:
        b.ui.locator("#details-row").click()
        b.ui.locator("#d-merchant").fill("x")
        b.ui.locator("#d-done").click()
        assert b.ui.locator("#sheet-root").is_hidden()
        assert b.console_errors == []
    finally:
        b.close()
    assert app.console_errors == []


def test_20_category_formula_prefix_round_trip(make_app):
    src = make_app(init_scripts=[CAPTURE_CLIPBOARD])
    src.tab("profile")
    src.cat_add()
    src.ui.locator("#c-name").fill("=Test")
    src.ui.locator('#c-tags label:has-text("Donation")').click()
    src.ui.locator("#c-save").click()
    src.close_sheet()
    src.tab("add")
    src.type_amount("15")
    src.more_pick("=Test")
    src.save()
    text = copied_csv(src)
    row = parse_csv(text)[1]
    assert row[COL["category"]] == "'=Test" and row[COL["category_group"]] == "Miscellaneous" and row[COL["tax_tag"]] == "donation"

    dst = make_app()
    dst.tab("profile")
    dst.ui.locator("#btn-restore").click()
    dst.ui.locator("#r-text").fill(text)
    dst.ui.locator("#r-go").click()
    assert dst.ui.locator("#r-result").inner_text() == "Restored 1 expense. Skipped 0 already here and 0 invalid rows."
    st = dst.state()
    custom = [c for c in st["categories"] if not c["builtIn"]]
    assert [c["name"] for c in custom] == ["=Test"] and custom[0]["taxTag"] == "donation"
    assert st["expenses"][0]["categoryId"] == custom[0]["id"]
    # a row without an id matches the existing category instead of creating "'=Test"
    dst.ui.locator("#r-text").fill("date,amount,category\r\n2026-11-02,3.00,'=Test\r\n")
    dst.ui.locator("#r-go").click()
    assert "Restored 1 expense." in dst.ui.locator("#r-result").inner_text()
    assert len([c for c in dst.state()["categories"] if not c["builtIn"]]) == 1
