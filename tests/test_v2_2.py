"""Acceptance tests from the v2.2 brief, section 8 (test numbers match the brief)."""
import json
import os
import re

from conftest import (CAT, GROUPS, ITEMS, OLD_CATS, ROOT, cents, item_id, make_card, make_state, make_v2_state,
                      names_the_template)
from test_v1 import CAPTURE_CLIPBOARD, COL, HEADER, copied_csv, parse_csv, source
from test_v2 import pick_payment, restore, tap_inside, wait_cached, wait_until

NOTICE = "Categories are now arranged in 8 budget groups. Your entries were moved; nothing was deleted."
BACKUP_KEY = "dailyspend.state.v2-backup"
DEFAULT_CHIPS = ["Groceries", "Restaurant / Take-Out", "Gas / Diesel", "Shopping", "Transit", "Personal Care", "Medical"]
GROUP_NAMES = [g[1] for g in GROUPS]


def heads(app, scope):
    """Group headings in a list, without their emoji."""
    return [t.split(" ", 1)[1] for t in app.ui.locator(f"{scope} .group-head").all_inner_texts()]


# ---------------------------------------------------------------- 1
def test_01_fresh_state_groups_items_and_chips(app):
    st = app.state()
    cats = st["categories"]
    assert st["schemaVersion"] == 3 and len(cats) == 45
    assert [(c["id"], c["groupId"], c["name"], c["emoji"], c["taxTag"]) for c in cats] == [
        (item_id(i[0], i[1]), i[0], i[1], i[2], i[3]) for i in ITEMS]
    assert len({c["name"].lower() for c in cats}) == 45 and len({c["id"] for c in cats}) == 45       # unique across the app
    assert list(dict.fromkeys(c["groupId"] for c in cats)) == [g[0] for g in GROUPS] and len(GROUPS) == 8
    assert all(c["builtIn"] and not c["hidden"] for c in cats)
    assert {c["name"]: c["taxTag"] for c in cats if c["taxTag"]} == {
        "Medical": "medical", "Health / Dental Insurance": "medical", "Donations": "donation", "Childcare": "childcare"}
    for must in ["food.groceries", "food.restaurant-take-out", "transportation.gas-diesel", "housing.mortgage-rent", "misc.other"]:
        assert must in {c["id"] for c in cats}
    # the seven default chips, in order, with no group captions (nothing to confuse)
    assert app.ui.locator("#chips .chip-name").all_inner_texts() == DEFAULT_CHIPS + ["More"]
    assert app.ui.locator("#chips .chip-group").count() == 0
    emoji = app.ui.locator("#chips .chip-emoji").all_inner_texts()
    assert emoji[:3] == ["🛒", "🍔", "⛽"]
    # the More sheet: every item under the 8 group headings, in order
    app.type_amount("9")
    app.ui.locator(".chip-more").click()
    assert heads(app, "#all-categories") == GROUP_NAMES
    assert app.ui.locator("#all-categories .row-title").all_inner_texts() == [i[1] for i in ITEMS]
    order = app.ui.locator("#all-categories > *").evaluate_all("(els) => els.map((e) => e.dataset.group || e.dataset.pick.split('.')[0])")
    assert order == sorted(order, key=[g[0] for g in GROUPS].index)                    # each item sits under its own heading
    app.ui.locator('#all-categories [data-pick="insurance.life-insurance"]').click()
    app.save()
    assert app.toast().inner_text() == "Saved $9.00 · Life Insurance"
    assert app.expenses()[0]["categoryId"] == "insurance.life-insurance"
    app.tab("history")
    assert app.ui.locator('.row[data-act="edit"] .row-title').inner_text() == "Life Insurance"
    assert app.ui.locator('.row[data-act="edit"] .row-sub').inner_text() == "Insurance"       # the group, in small text
    # the source of the category list is not named anywhere
    for name in ["app.js", "tax.js", "index.html", "styles.css", "sw.js", "README.md", "manifest.webmanifest"]:
        assert not names_the_template(source(name)), name
    assert app.console_errors == []


def test_01b_confusable_chips_show_their_group(app):
    # "Gas / Diesel" and "Gas & Hydro" as chips at the same time: each says which group it is in
    rows = [("2026-11-10", 100, "housing.gas-hydro", "credit", "", "")] * 3 + [("2026-11-11", 100, "gas", "credit", "", "")] * 2
    app.seed(make_state(rows))
    names = app.ui.locator("#chips .chip-name").all_inner_texts()
    assert names[:2] == ["Gas & Hydro", "Gas / Diesel"]
    assert app.ui.locator('.chip[data-cat="housing.gas-hydro"] .chip-group').inner_text() == "Housing"
    assert app.ui.locator('.chip[data-cat="transportation.gas-diesel"] .chip-group').inner_text() == "Transportation"
    assert app.ui.locator("#chips .chip-group").count() == 2
    assert app.ui.locator('.chip[data-cat="housing.gas-hydro"]').get_attribute("aria-label") == "Gas & Hydro, Housing"
    app.type_amount("5")
    app.ui.locator('.chip[data-cat="housing.gas-hydro"]').click()
    app.save()
    assert app.toast().inner_text() == "Saved $5.00 · Gas & Hydro"


# ---------------------------------------------------------------- 2
def test_02_migration_from_v2(make_app):
    rows = [(f"2026-11-{i + 1:02d}", 1000 + i * 111, c[0], "credit", f"Shop {i}", f"note {i}") for i, c in enumerate(OLD_CATS)]
    rows += [("2026-11-21", 5500, "c_vet", "debit", "Clinic", ""), ("2026-11-22", 3300, "c_pets", "cash", "Pet store", ""),
             ("2026-10-05", 700, "dining", "credit", "Cafe", "")]
    card = make_card("card-a", "Maple Rewards Visa", catalogue_id="maple-rewards-visa")
    v2 = make_v2_state(rows, cards=[card])
    v2["expenses"][0]["cardId"] = "card-a"
    v2["settings"]["lastPayment"] = {"methodId": "credit", "cardId": "card-a"}
    cats = {c["id"]: c for c in v2["categories"]}
    cats["dining"]["name"] = "Coffee runs"                 # renamed built-in
    cats["gifts"]["hidden"] = True                          # hidden built-in
    v2["categories"] += [
        {"id": "c_vet", "emoji": "🐶", "name": "Vet", "taxTag": "medical", "hidden": False, "builtIn": False, "order": 21},
        {"id": "c_pets", "emoji": "🐕", "name": "pets", "taxTag": None, "hidden": False, "builtIn": False, "order": 22}]   # now a built-in name
    app = make_app(skip_welcome=False, open_page=False)
    app.page.goto(app.base_url + "/")
    app.page.evaluate("s => { localStorage.clear(); localStorage.setItem('dailyspend.state', JSON.stringify(s)); }", v2)
    raw_before = app.page.evaluate("localStorage.getItem('dailyspend.state')")
    app.page.reload()
    app.ui.locator("#amount").wait_for()

    # the one-time notice
    assert app.ui.locator("#mig-text").inner_text() == NOTICE
    assert app.ui.locator("#ob-skip").count() == 0 and app.state()["settings"]["groupsNotice"] is True
    app.ui.locator("#mig-ok").click()
    assert app.sheet_hidden() and app.state()["settings"]["groupsNotice"] is False

    st = app.state()
    assert st["schemaVersion"] == 3
    # nothing lost: same count, same total, every field the same except the category
    assert len(st["expenses"]) == len(v2["expenses"]) == 23
    assert sum(e["amountCents"] for e in st["expenses"]) == sum(e["amountCents"] for e in v2["expenses"])
    special = {"c_vet": "c_vet", "c_pets": "misc.pets"}
    for old, new in zip(v2["expenses"], st["expenses"]):
        want = special.get(old["categoryId"]) or CAT[old["categoryId"]]
        assert new == {**old, "categoryId": want}, old["id"]
    landed = {old["categoryId"]: new["categoryId"] for old, new in zip(v2["expenses"], st["expenses"])}
    assert {k: landed[k] for k in CAT} == CAT and len(set(CAT.values())) == 20             # all 20, per the table
    new_cats = {c["id"]: c for c in st["categories"]}
    assert len(new_cats) == 46 and "c_pets" not in new_cats                                # 45 items, Vet; "pets" merged into Pets
    vet = new_cats["c_vet"]
    assert (vet["name"], vet["groupId"], vet["taxTag"], vet["builtIn"], vet["emoji"]) == ("Vet", "misc", "medical", False, "🐶")
    assert new_cats["food.restaurant-take-out"]["name"] == "Coffee runs"                   # the rename carried over
    assert new_cats["misc.gifts"]["hidden"] is True                                        # hidden carried over
    assert sum(1 for c in new_cats.values() if c["hidden"]) == 1
    assert sum(1 for c in new_cats.values() if c["name"] != {item_id(i[0], i[1]): i[1] for i in ITEMS}.get(c["id"], c["name"])) == 1
    assert st["cards"] == v2["cards"] and st["settings"]["lastPayment"] == {"methodId": "credit", "cardId": "card-a"}
    assert st["settings"]["onboarded"] is True
    # the backup: the version 2 state exactly as it was
    assert app.page.evaluate("k => localStorage.getItem(k)", BACKUP_KEY) == raw_before
    assert json.loads(raw_before)["schemaVersion"] == 2

    # and the app shows it
    assert "Gifts" not in app.ui.locator("#chips .chip-name").all_inner_texts()
    assert "Coffee runs" in app.ui.locator("#chips .chip-name").all_inner_texts()
    app.tab("history")
    assert cents(app.ui.locator("#month-total").inner_text()) == sum(r[1] for r in rows if r[0].startswith("2026-11"))
    assert app.ui.locator('.row[data-id="seed-001"] .row-title').inner_text() == "Coffee runs"
    assert app.ui.locator('.row[data-id="seed-021"] .row-title').inner_text() == "Pets"
    app.tab("summary")
    assert cents(app.ui.locator('#tax-card [data-tax="medical"] .v').inner_text()) == (1000 + 11 * 111) + 5500
    # the notice shows once, and the migration runs once
    app.tab("add")
    app.add("1", "Transit")
    app.page.reload()
    app.ui.locator("#amount").wait_for()
    app.page.wait_for_timeout(200)
    assert app.sheet_hidden() and app.ui.locator("#mig-ok").count() == 0
    assert len(app.expenses()) == 24
    assert app.page.evaluate("k => localStorage.getItem(k)", BACKUP_KEY) == raw_before     # kept...
    app.tab("profile")
    app.ui.locator("#btn-delete-all").click()
    app.ui.locator("#da-input").fill("DELETE")
    app.ui.locator("#da-go").click()
    assert app.page.evaluate("k => localStorage.getItem(k)", BACKUP_KEY) is None           # ...until all data is deleted
    assert app.console_errors == [] and app.dialogs == []

    # closing the notice any other way also counts as seen
    b = make_app(skip_welcome=False, open_page=False)
    b.page.goto(b.base_url + "/")
    b.page.evaluate("s => { localStorage.clear(); localStorage.setItem('dailyspend.state', JSON.stringify(s)); }", make_v2_state(rows[:3]))
    b.page.reload()
    b.ui.locator("#mig-text").wait_for()
    b.page.keyboard.press("Escape")
    assert b.state()["settings"]["groupsNotice"] is False
    # a v2 state with no entries: no notice (nothing was moved); a fresh install: no notice, no backup
    c = make_app(skip_welcome=False, open_page=False)
    c.page.goto(c.base_url + "/")
    c.page.evaluate("s => { localStorage.clear(); localStorage.setItem('dailyspend.state', JSON.stringify(s)); }", make_v2_state([]))
    c.page.reload()
    c.ui.locator("#amount").wait_for()
    assert c.ui.locator("#mig-ok").count() == 0 and c.state()["schemaVersion"] == 3 and len(c.state()["categories"]) == 45
    d = make_app()
    assert d.ui.locator("#mig-ok").count() == 0 and d.page.evaluate("k => localStorage.getItem(k)", BACKUP_KEY) is None


# ---------------------------------------------------------------- 3
SUMMARY_ROWS = [
    ("2026-11-01", 150000, "housing", "etransfer", "", "Rent"), ("2026-11-02", 9000, "utilities", "pad", "Enmax", ""),
    ("2026-11-03", 8000, "groceries", "credit", "Co-op", ""), ("2026-11-04", 2000, "dining", "credit", "Cafe", ""),
    ("2026-11-05", 6000, "gas", "credit", "", ""), ("2026-11-06", 4000, "insurance.life-insurance", "pad", "", ""),
    ("2026-11-07", 1000, "debt.student-loan", "pad", "", ""), ("2026-10-10", 5000, "groceries", "credit", "", ""),
]


def test_03_summary_by_group(app):
    app.seed(make_state(SUMMARY_ROWS))
    app.tab("summary")
    total = 180000
    assert cents(app.ui.locator("#summary-total").inner_text()) == total
    slices = app.ui.locator("#donut .slice").evaluate_all("(els) => els.map((e) => [e.dataset.group, Number(e.dataset.cents), e.getAttribute('aria-label')])")
    assert [(s[0], s[1]) for s in slices] == [("housing", 159000), ("food", 10000), ("transportation", 6000), ("insurance", 4000), ("debt", 1000)]
    assert sum(s[1] for s in slices) == total and len(slices) <= 8                    # empty groups are left out
    assert slices[0][2] == "Housing, $1,590.00, 88%" and slices[1][2] == "Food, $100.00, 6%"
    assert cents(app.ui.locator("#donut-total").text_content()) == total
    # a group keeps its colour whatever its rank
    colour = lambda group: app.ui.locator(f'#donut .slice[data-group="{group}"]').get_attribute("class").split()[1]
    assert (colour("housing"), colour("debt"), colour("food"), colour("insurance")) == ("gc0", "gc1", "gc3", "gc7")

    # By group: one row per group with amount, share and bar; each opens to its items
    assert app.ui.locator("#view .section-head").all_inner_texts() == ["By group"]
    assert app.ui.locator("#by-group .grp-row .name").all_inner_texts() == ["Housing", "Food", "Transportation", "Insurance", "Debt Payments"]
    assert [int(p.rstrip("%")) for p in app.ui.locator("#by-group .grp-row .pct").all_inner_texts()] == [88, 6, 3, 2, 1]
    assert app.ui.locator("#by-group .grp-row .bar").count() == 5 and app.ui.locator("#by-group .item-row").count() == 0
    row = app.ui.locator('#by-group .grp-row:has-text("Housing")')
    assert row.get_attribute("aria-expanded") == "false"
    row.click()
    assert row.get_attribute("aria-expanded") == "true"
    assert app.ui.locator("#by-group .item-row .name").all_inner_texts() == ["Mortgage / Rent", "Gas & Hydro"]
    assert [cents(t) for t in app.ui.locator("#by-group .item-row .amt").all_inner_texts()] == [150000, 9000]
    row.click()
    assert app.ui.locator("#by-group .item-row").count() == 0

    # tapping a group on the donut shows its items, inside Summary
    tap_inside(app, app.ui.locator('#donut .slice[data-group="food"]'))
    assert app.ui.locator('.tab[data-tab="summary"]').get_attribute("aria-current") == "page"
    assert app.ui.locator("#group-name").inner_text().endswith("Food")
    assert cents(app.ui.locator("#group-total").inner_text()) == 10000
    assert app.ui.locator("#group-share").inner_text() == "6% of November 2026"
    assert app.ui.locator("#group-items .name").all_inner_texts() == ["Groceries", "Restaurant / Take-Out"]
    assert [cents(t) for t in app.ui.locator("#group-items .amt").all_inner_texts()] == [8000, 2000]
    assert app.ui.locator("#group-items .pct").all_inner_texts() == ["80%", "20%"]      # shares of the group
    assert app.ui.locator("#group-items .bar").count() == 2
    assert app.ui.locator("#donut").count() == 0 and app.ui.locator("#tax-card").count() == 0
    # the month switcher still works there
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert cents(app.ui.locator("#group-total").inner_text()) == 5000 and app.ui.locator("#group-items .name").all_inner_texts() == ["Groceries"]
    app.ui.locator('[data-act="month"][data-delta="-1"]').click()
    assert "No expenses in September 2026." in app.ui.locator("#group-share").inner_text() and app.ui.locator("#group-items").count() == 0
    app.ui.locator('[data-act="month"][data-delta="1"]').click()
    app.ui.locator('[data-act="month"][data-delta="1"]').click()
    # tapping an item filters History to that item, for the month
    app.ui.locator('#group-items .cat-row:has-text("Groceries")').click()
    assert app.ui.locator('.tab[data-tab="history"]').get_attribute("aria-current") == "page"
    assert app.ui.locator("#f-category").inner_text() == "Groceries" and app.ui.locator("#f-month").inner_text() == "November 2026 ×"
    assert cents(app.ui.locator("#results-total").inner_text()) == 8000 and app.ui.locator('.row[data-act="edit"]').count() == 1
    app.ui.locator("#f-clear").click()
    # back from a group view to the overview
    app.tab("summary")
    assert app.ui.locator("#donut").count() == 1                                        # the overview again
    tap_inside(app, app.ui.locator('#donut .slice[data-group="housing"]'))
    assert app.ui.locator("#group-back").inner_text() == "‹ All groups"
    app.ui.locator("#group-back").click()
    assert app.ui.locator("#donut").count() == 1 and app.ui.locator("#tax-card").count() == 1

    # the History category filter is grouped, with a whole-group option
    app.tab("history")
    app.ui.locator("#f-category").click()
    assert app.ui.locator("#fc-list input[data-group]").count() == 8 and app.ui.locator("#fc-list input[data-item]").count() == 45
    app.ui.locator('#fc-list input[data-group="housing"]').check()
    assert app.ui.locator('#fc-list input[data-item="housing"]:checked').count() == 8
    assert app.ui.locator("#f-category").inner_text() == "Housing"
    app.ui.locator("#fc-done").click()
    assert cents(app.ui.locator("#results-total").inner_text()) == 159000
    app.ui.locator("#f-category").click()
    app.ui.locator('#fc-list label:has-text("Gas & Hydro")').click()                    # one off: the group box is partly on
    assert app.ui.locator('#fc-list input[data-group="housing"]').evaluate("(e) => [e.checked, e.indeterminate]") == [False, True]
    assert app.ui.locator("#f-category").inner_text() == "Category · 7"
    app.ui.locator('#fc-list input[data-group="housing"]').check()
    app.ui.locator('#fc-list input[data-group="housing"]').uncheck()
    assert app.ui.locator("#fc-list input[data-item]:checked").count() == 0
    assert app.console_errors == []


# ---------------------------------------------------------------- 4
def test_04_tax_time(app):
    rows = [("2026-11-01", 10000, "medical", "credit", "Dentist", ""), ("2026-11-02", 25000, "insurance.health-dental-insurance", "pad", "", ""),
            ("2026-11-03", 4000, "gifts", "credit", "", ""), ("2026-11-04", 6000, "donations", "credit", "", ""),
            ("2026-11-05", 7000, "childcare", "etransfer", "", ""), ("2026-11-06", 9000, "insurance.life-insurance", "pad", "", ""),
            ("2026-03-01", 1500, "insurance.health-dental-insurance", "pad", "", ""), ("2025-12-01", 9999, "medical", "credit", "", "")]
    app.seed(make_state(rows))
    app.tab("summary")
    card = app.ui.locator("#tax-card")
    value = lambda tag: cents(card.locator(f'[data-tax="{tag}"] .v').inner_text())
    assert card.locator(".card-title").inner_text() == "Tax time 2026"
    assert value("medical") == 10000 + 25000 + 1500                                    # Health / Dental Insurance counts
    assert value("donation") == 6000                                                   # gifts are not donations
    assert value("childcare") == 7000
    assert [t.split("\n")[0] for t in card.locator(".kv").all_inner_texts()] == ["Medical", "Donations", "Childcare"]
    assert app.ui.locator("#tax-footnote").inner_text() == (
        "Totals of tagged categories. Only private health plan premiums count; provincial plan premiums don't.")
    tags = {c["name"]: c["taxTag"] for c in app.state()["categories"]}
    assert tags["Gifts"] is None and tags["Health / Dental Insurance"] == "medical" and tags["Life Insurance"] is None
    # the tag shows in the More sheet
    app.tab("add")
    app.type_amount("1")
    app.ui.locator(".chip-more").click()
    assert app.ui.locator('#all-categories [data-pick="insurance.health-dental-insurance"] .badge').inner_text() == "Medical"
    assert app.ui.locator('#all-categories [data-pick="misc.gifts"] .badge').count() == 0


# ---------------------------------------------------------------- 5
V2_CSV = "\r\n".join([
    "id,date,amount,category,payment_method,card,card_last4,merchant,note,tax_tag,latitude,longitude,location_accuracy_m,created_at,updated_at",
    "o-1,2026-11-02,12.50,Dining & coffee,Credit card,,,Cafe,,,,,,2026-11-02T10:00:00.000Z,2026-11-02T10:00:00.000Z",
    "o-2,2026-11-03,60.00,Gas & parking,Credit card,,,Esso,,,,,,2026-11-03T10:00:00.000Z,2026-11-03T10:00:00.000Z",
    "o-3,2026-11-01,1800.00,RENT OR MORTGAGE,e-Transfer (Interac),,,,,,,,,2026-11-01T10:00:00.000Z,2026-11-01T10:00:00.000Z",
    "o-4,2026-11-04,95.00,Medical & dental,Credit card,,,Dentist,,medical,,,,2026-11-04T10:00:00.000Z,2026-11-04T10:00:00.000Z",
    "o-5,2026-11-05,300.00,Travel,Credit card,,,WestJet,,,,,,2026-11-05T10:00:00.000Z,2026-11-05T10:00:00.000Z",
    "o-6,2026-11-06,20.00,Personal care,Cash,,,,,,,,,2026-11-06T10:00:00.000Z,2026-11-06T10:00:00.000Z",
    "o-7,2026-11-07,80.00,Phone & internet,Pre-authorised debit,,,Telus,,,,,,2026-11-07T10:00:00.000Z,2026-11-07T10:00:00.000Z",
    "o-8,2026-11-08,40.00,Groceries,Credit card,,,Co-op,,,,,,2026-11-08T10:00:00.000Z,2026-11-08T10:00:00.000Z",
    "o-9,2026-11-09,75.00,Llama rental,Cash,,,,,donation,,,,2026-11-09T10:00:00.000Z,2026-11-09T10:00:00.000Z",
]) + "\r\n"


def test_05_csv_v3(make_app):
    src = make_app(init_scripts=[CAPTURE_CLIPBOARD])
    rows = [("2026-11-01", 1234, "groceries", "credit", "Co-op", ""), ("2026-11-02", 5000, "insurance.health-dental-insurance", "pad", "", ""),
            ("2026-11-03", 700, "c_bakery", "cash", "Bakery", "bread, rolls"), ("2026-11-04", 900, "housing.other-housing", "credit", "", "")]
    st = make_state(rows)
    st["categories"].append({"id": "c_bakery", "groupId": "food", "emoji": "🥖", "name": "Bakery", "taxTag": None,
                             "hidden": False, "builtIn": False, "order": 46})
    src.seed(st)
    text = copied_csv(src)
    assert text.split("\r\n")[0] == HEADER == (
        "id,date,amount,category_group,category,payment_method,card,card_last4,merchant,note,tax_tag,"
        "latitude,longitude,location_accuracy_m,created_at,updated_at")
    body = {r[0]: dict(zip(HEADER.split(","), r)) for r in parse_csv(text)[1:]}
    assert [(body[f"seed-00{i}"]["category_group"], body[f"seed-00{i}"]["category"], body[f"seed-00{i}"]["tax_tag"]) for i in range(4)] == [
        ("Food", "Groceries", ""), ("Insurance", "Health / Dental Insurance", "medical"), ("Food", "Bakery", ""), ("Housing", "Other housing", "")]

    # v3 round trip into an empty app
    dst = make_app(init_scripts=[CAPTURE_CLIPBOARD])
    assert restore(dst, text) == "Restored 4 expenses. Skipped 0 already here and 0 invalid rows."
    got = {e["id"]: e for e in dst.expenses()}
    want = {e["id"]: e for e in src.expenses()}
    for i in ["seed-000", "seed-001", "seed-003"]:
        assert got[i] == want[i]
    bakery = [c for c in dst.state()["categories"] if c["name"] == "Bakery"][0]
    assert bakery["builtIn"] is False and bakery["groupId"] == "food"                  # recreated in the group the file names
    assert got["seed-002"]["categoryId"] == bakery["id"] and len(dst.state()["categories"]) == 46
    assert copied_csv(dst) == text
    assert restore(dst, text) == "Restored 0 expenses. Skipped 4 already here and 0 invalid rows."
    # group + name wins; a wrong or missing group still matches by name; names ignore case
    extra = "\r\n".join(["date,amount,category_group,category", "2026-11-10,1.00,food,GROCERIES", "2026-11-10,2.00,Housing,Groceries",
                         "2026-11-10,3.00,,groceries", "2026-11-10,4.00,'=Odd group,Brand new", "2026-11-10,5.00,Recreation,Bowling"]) + "\r\n"
    assert restore(dst, extra) == "Restored 5 expenses. Skipped 0 already here and 0 invalid rows."
    by_amount = {e["amountCents"]: e["categoryId"] for e in dst.expenses()}
    assert by_amount[100] == by_amount[200] == by_amount[300] == "food.groceries"
    new = {c["name"]: c for c in dst.state()["categories"] if not c["builtIn"]}
    assert new["Brand new"]["groupId"] == "misc" and new["Bowling"]["groupId"] == "recreation"

    # a v2 file with the old names restores into the mapped items
    old = make_app()
    assert restore(old, V2_CSV) == "Restored 9 expenses. Skipped 0 already here and 0 invalid rows."
    ex = {e["id"]: e for e in old.expenses()}
    assert [ex[f"o-{i}"]["categoryId"] for i in range(1, 9)] == [
        "food.restaurant-take-out", "transportation.gas-diesel", "housing.mortgage-rent", "misc.medical",
        "recreation.travel-vacation", "misc.personal-care", "communications.cell-telephone", "food.groceries"]
    # an unknown category becomes a custom item in Miscellaneous, with its tax tag
    cats = old.state()["categories"]
    assert len(cats) == 46
    llama = [c for c in cats if c["name"] == "Llama rental"][0]
    assert (llama["groupId"], llama["taxTag"], llama["builtIn"]) == ("misc", "donation", False) and ex["o-9"]["categoryId"] == llama["id"]
    assert ex["o-1"]["amountCents"] == 1250 and ex["o-3"]["paymentMethodId"] == "etransfer"
    # an old name still finds its item after the user renamed it
    old.tab("profile")
    old.ui.locator('#category-list .row:has-text("Restaurant / Take-Out")').click()
    old.ui.locator("#c-name").fill("Eating out")
    old.ui.locator("#c-save").click()
    assert "Restored 1 expense." in restore(old, "date,amount,category\r\n2026-11-11,9.00,Dining & coffee\r\n")
    assert [e for e in old.expenses() if e["amountCents"] == 900][0]["categoryId"] == "food.restaurant-take-out"
    assert len(old.state()["categories"]) == 46
    for a in (src, dst, old):
        assert a.console_errors == [] and a.dialogs == []


# ---------------------------------------------------------------- 6
def test_06_categories_screen(app):
    app.tab("profile")
    assert heads(app, "#category-list") == [g[1] for g in GROUPS]
    assert app.ui.locator("#category-list .row-title").all_inner_texts() == [i[1] for i in ITEMS]
    position = lambda name: app.ui.locator("#category-list > *").evaluate_all(
        "(els, name) => { let g = null; for (const e of els) { if (e.dataset.group) g = e.dataset.group; else if (e.textContent.includes(name)) return g; } return null; }", name)

    # add an item to a chosen group
    app.ui.locator("#btn-add-category").click()
    assert app.ui.locator("#c-group option").count() == 8
    assert app.ui.locator("#c-group").input_value() == "misc"                           # Miscellaneous unless chosen
    app.ui.locator("#c-name").fill("groceries")
    app.ui.locator("#c-save").click()
    assert "already a category" in app.ui.locator("#c-error").inner_text()            # names are unique across all groups
    app.ui.locator("#c-name").fill("Bakery")
    app.ui.locator("#c-emoji").fill("🥖")
    app.ui.locator("#c-group").select_option("food")
    app.ui.locator("#c-save").click()
    bakery = [c for c in app.state()["categories"] if c["name"] == "Bakery"][0]
    assert (bakery["groupId"], bakery["builtIn"], bakery["taxTag"], bakery["emoji"]) == ("food", False, None, "🥖")
    assert position("Bakery") == "food"
    # it can be picked on Add, under its group
    app.tab("add")
    app.type_amount("6.50")
    app.ui.locator(".chip-more").click()
    order = app.ui.locator("#all-categories > *").evaluate_all("(els) => els.map((e) => e.dataset.group || e.querySelector('.row-title').textContent)")
    assert order[order.index("food") + 1:order.index("transportation")] == ["Groceries", "Restaurant / Take-Out", "Bakery"]
    app.ui.locator(f'#all-categories [data-pick="{bakery["id"]}"]').click()
    app.save()
    assert app.toast().inner_text() == "Saved $6.50 · Bakery"

    # rename, change group, change tax tag
    app.tab("profile")
    app.ui.locator('#category-list .row:has-text("Bakery")').click()
    assert app.ui.locator("#c-group").input_value() == "food"
    app.ui.locator("#c-name").fill("Bakery & deli")
    app.ui.locator("#c-group").select_option("recreation")
    app.ui.locator('#c-tags label:has-text("Donation")').click()
    app.ui.locator("#c-save").click()
    moved = [c for c in app.state()["categories"] if c["id"] == bakery["id"]][0]
    assert (moved["name"], moved["groupId"], moved["taxTag"]) == ("Bakery & deli", "recreation", "donation")
    assert position("Bakery & deli") == "recreation" and position("Groceries") == "food"
    app.tab("summary")
    assert app.ui.locator("#by-group .grp-row .name").all_inner_texts() == ["Recreation"]                 # its entry moved with it
    assert cents(app.ui.locator('#tax-card [data-tax="donation"] .v').inner_text()) == 650

    # hide: gone from Add, kept in History
    app.tab("profile")
    app.ui.locator('#category-list .row:has-text("Bakery & deli")').click()
    app.ui.locator("#c-hidden").check()
    app.ui.locator("#c-save").click()
    assert "Hidden" in app.ui.locator('#category-list .row:has-text("Bakery & deli")').inner_text()
    app.tab("add")
    app.type_amount("1")
    app.ui.locator(".chip-more").click()
    assert "Bakery & deli" not in app.ui.locator("#all-categories .row-title").all_inner_texts()
    assert app.ui.locator("#all-categories .row").count() == 45
    app.page.keyboard.press("Escape")
    app.tab("history")
    assert app.ui.locator('.row[data-act="edit"] .row-title').inner_text() == "Bakery & deli"

    # built-in items: can be hidden, renamed and moved, never deleted; a used custom item cannot be deleted either
    app.tab("profile")
    app.ui.locator('#category-list .row:has-text("Property / Tenant Insurance")').click()
    assert app.ui.locator("#c-delete").count() == 0 and app.ui.locator("#c-name").input_value() == "Property / Tenant Insurance"
    app.ui.locator("#c-group").select_option("insurance")
    app.ui.locator("#c-hidden").check()
    app.ui.locator("#c-save").click()
    item = [c for c in app.state()["categories"] if c["id"] == "housing.property-tenant-insurance"][0]
    assert (item["name"], item["groupId"], item["hidden"], item["builtIn"]) == ("Property / Tenant Insurance", "insurance", True, True)
    assert position("Property / Tenant Insurance") == "insurance"
    app.ui.locator('#category-list .row:has-text("Bakery & deli")').click()
    assert app.ui.locator("#c-delete").count() == 0
    app.page.keyboard.press("Escape")
    app.ui.locator("#btn-add-category").click()
    app.ui.locator("#c-name").fill("Temp")
    app.ui.locator("#c-save").click()
    app.ui.locator('#category-list .row:has-text("Temp")').click()
    app.ui.locator("#c-delete").click()
    app.ui.locator("#c-confirm-delete").click()
    assert len(app.state()["categories"]) == 46
    # groups themselves are fixed: nothing to add, rename or delete
    assert app.ui.locator("#category-list .group-head button, #category-list button.group-head").count() == 0
    app.reload()
    assert [c for c in app.state()["categories"] if c["id"] == bakery["id"]][0]["groupId"] == "recreation"   # survives a reload
    assert app.console_errors == []


# ---------------------------------------------------------------- 7
BADGES = """() => Array.from(document.querySelectorAll('#ac-list [data-issuer]')).map((row) => {
  const b = row.querySelector('.ibadge'), cs = getComputedStyle(b), box = b.getBoundingClientRect();
  return { name: row.dataset.issuer, text: b.dataset.t, shown: getComputedStyle(b, '::before').content.replace(/"/g, ''),
    bg: cs.backgroundColor, fg: cs.color, w: box.width, weight: cs.fontWeight, radius: parseFloat(cs.borderRadius) };
})"""
POPULAR = ["RBC Royal Bank", "TD", "Scotiabank", "BMO", "CIBC", "National Bank", "Desjardins", "American Express Canada"]


def luminance(rgb):
    r, g, b = [int(v) / 255 for v in re.findall(r"\d+", rgb)[:3]]
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def badge_contrast(badge):
    """Text against its own background (v2.4: pastel with dark text in light, white on colour in dark)."""
    hi, lo = sorted([luminance(badge["fg"]), luminance(badge["bg"])], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def az_key(name):
    return re.sub(r"^the\s+", "", name.lower())


def test_07_badges_real_list(make_app):
    data = json.load(open(os.path.join(ROOT, "data", "cards-ca.json"), encoding="utf-8"))
    shorts = [i["short"] for i in data["issuers"]]
    assert len(shorts) == len(set(s.lower() for s in shorts)) == 29 and all(2 <= len(s) <= 6 for s in shorts)

    app = make_app(cards="real")
    app.tab("profile")
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()
    badges = app.page.evaluate(BADGES)
    assert len(badges) == 29
    by_name = {i["name"]: i["short"] for i in data["issuers"]}
    assert all(b["text"] == b["shown"] == by_name[b["name"]] for b in badges)          # the planner's short names, as drawn
    assert len({b["text"] for b in badges}) == 29                                      # every institution has its own badge text
    # Level 1 with no cards yet: Popular (in the brief's order), then everything else A to Z
    assert app.ui.locator("#ac-list .group-head").all_inner_texts() == ["Popular", "All institutions"]
    names = [b["name"] for b in badges]
    assert names[:8] == POPULAR
    assert names[8:] == sorted(names[8:], key=az_key) and len(names[8:]) == 21
    # the badge: rounded rectangle, at least 40 px wide, bold white text on one of 12 colours with AA contrast
    colours = {b["bg"] for b in badges}
    assert len(colours) == 12
    for b in badges:
        assert b["w"] >= 40 and int(b["weight"]) >= 700 and 4 <= b["radius"] <= 10
        assert badge_contrast(b) >= 4.5, b
    assert max(b["w"] for b in badges) > 40                                            # six letters make it grow
    # colours follow the A to Z position, so neighbours in that list never match
    az = sorted(badges, key=lambda b: az_key(b["name"]))
    assert all(az[i]["bg"] != az[i + 1]["bg"] for i in range(len(az) - 1))
    assert [b["bg"] for b in az[:12]] == [b["bg"] for b in az[12:24]]                  # the palette cycles in order
    # search collapses the sections into results
    app.ui.locator("#ac-search").fill("bank")
    assert app.ui.locator("#ac-yours, #ac-popular, #ac-all").count() == 0
    found = [b["name"] for b in app.page.evaluate(BADGES)]
    assert found and all("bank" in n.lower() for n in found) and found == sorted(found, key=az_key)
    # no logos anywhere
    assert app.page.locator("#sheet-root img, #sheet-root svg image, #app img").count() == 0
    assert app.console_errors == []


def test_07b_badges_sections_and_other_places(app):
    app.tab("profile")
    app.ui.locator("#btn-add-card").click()
    app.ui.locator("#ac-list .row").first.wait_for()
    assert app.ui.locator("#ac-list .group-head").all_inner_texts() == ["Popular", "All institutions"]
    before = app.page.evaluate(BADGES)
    assert [(b["name"], b["text"]) for b in before] == [("American Express", "Amex"), ("Maple Bank", "Maple"),
                                                        ("The Northern Trust", "NT"), ("Prairie Credit Union", "PCU")]   # no short name: initials
    assert len({b["bg"] for b in before}) == 4
    app.pick_card("Maple Bank", "Maple Rewards Visa", kind="credit")
    app.ui.locator('#cf-colours .swatch:has(input[value="rose"])').click()
    app.ui.locator("#cf-save").click()

    # My cards: badge on the left, the chosen card colour kept as an accent
    tile = app.ui.locator("#card-list .card-tile")
    assert tile.locator(".ibadge").get_attribute("data-t") == "Maple" and tile.locator(".card-swatch.sw-rose").count() == 1
    assert tile.locator(".ibadge").evaluate("(e) => getComputedStyle(e).backgroundColor") == before[1]["bg"]
    assert tile.evaluate("(t) => t.querySelector('.ibadge').getBoundingClientRect().left < t.querySelector('.row-title').getBoundingClientRect().left")
    # Level 1 now: Your institutions, then Popular, then the rest A to Z
    app.ui.locator("#btn-add-card").click()
    assert app.ui.locator("#ac-list .group-head").all_inner_texts() == ["Your institutions", "Popular", "All institutions"]
    order = app.ui.locator("#ac-list > *").evaluate_all("(els) => els.map((e) => e.dataset.issuer || e.textContent)")
    assert order == ["Your institutions", "Maple Bank", "Popular", "American Express", "All institutions", "The Northern Trust", "Prairie Credit Union"]
    # a popular institution the user already has moves up and is not repeated
    app.pick_card("American Express", "American Express Cobalt Card")
    app.ui.locator("#cf-save").click()
    app.ui.locator("#btn-add-card").click()
    order = app.ui.locator("#ac-list > *").evaluate_all("(els) => els.map((e) => e.dataset.issuer || e.textContent)")
    assert order == ["Your institutions", "American Express", "Maple Bank", "All institutions", "The Northern Trust", "Prairie Credit Union"]
    # a card added by hand: initials from the typed issuer on neutral grey; it adds no institution section entry
    app.ui.locator("#ac-manual").click()
    app.ui.locator("#cf-issuer").fill("Corner Credit Union")
    app.ui.locator("#cf-name").fill("Member Card")
    app.ui.locator("#cf-save").click()
    hand = app.ui.locator('#card-list .card-tile:has-text("Member Card") .ibadge')
    assert hand.get_attribute("data-t") == "CC" and "ib-n" in hand.get_attribute("class")
    assert hand.evaluate("(e) => getComputedStyle(e).backgroundColor") == "rgb(243, 244, 246)"          # neutral grey (light theme)

    # the payment picker rows
    app.tab("add")
    app.ui.locator("#details-row").click()
    assert app.ui.locator('#d-pay [data-group="cards"] .ibadge').evaluate_all("(els) => els.map((e) => e.dataset.t)") == ["Maple", "Amex", "CC"]
    assert app.ui.locator('#d-pay [data-group="other"] .ibadge').count() == 0
    drawn = app.ui.locator('#d-pay [data-group="cards"] .ibadge').first.evaluate(
        "(e) => [getComputedStyle(e).backgroundColor, getComputedStyle(e).color, Math.round(e.getBoundingClientRect().height)]")
    assert drawn == [before[1]["bg"], before[1]["fg"], 26]
    assert [t.strip() for t in app.ui.locator('#d-pay [data-group="cards"] .option').all_inner_texts()] == [
        "Maple Rewards Visa", "American Express Cobalt Card", "Member Card"]            # the badge is decoration, not part of the label
    app.page.keyboard.press("Escape")
    # Summary → By card
    pick_payment(app, "Maple Rewards Visa")
    app.add("20", "Groceries")
    pick_payment(app, "Member Card")
    app.add("5", "Groceries")
    pick_payment(app, "Cash")
    app.add("1", "Groceries")
    app.tab("summary")
    assert app.ui.locator("#by-card .ibadge").evaluate_all("(els) => els.map((e) => e.dataset.t)") == ["Maple", "CC"]
    assert app.ui.locator("#by-card .name").all_inner_texts() == ["Maple Rewards Visa", "Member Card", "Cash & other"]
    # after a restart the badges come back without opening the picker
    app.reload()
    app.tab("profile")
    wait_until(lambda: app.ui.locator("#card-list .card-tile .ibadge").evaluate_all("(els) => els.map((e) => e.dataset.t)") == ["Maple", "CC", "Amex"])   # most used first
    assert app.page.locator("#app img").count() == 0
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 8
def test_08_version(make_app):
    sw = source("sw.js")
    assert "const VERSION = '0.2.4';" in sw and "const CACHE = 'ds-' + VERSION;" in sw
    assert "version: '0.2.4'," in source("app.js") and not re.search(r"0\.2\.[0123]\b", sw + source("app.js"))
    app = make_app(service_workers="allow", cards=None, tax=None)
    wait_cached(app.page, cache="ds-0.2.4")
    assert app.page.evaluate("caches.keys()") == ["ds-0.2.4"]
    app.tab("profile")
    assert app.ui.locator("#app-version").inner_text() == "Version 0.2.4"
    assert app.console_errors == []
