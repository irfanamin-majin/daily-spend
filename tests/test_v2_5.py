"""Acceptance tests from the v2.5 brief, section 7 (test numbers match the brief)."""
import re
import unicodedata

from conftest import GROUPS, ITEMS, item_id, make_state
from test_v1 import source
from test_v2 import wait_cached
from test_v2_4 import contrast, luminance

DEFAULT_CHIPS = ["Groceries", "Restaurant / Take-Out", "Gas / Diesel", "Shopping", "Transit", "Personal Care", "Medical"]
GROUP_NAMES = [g[1] for g in GROUPS]
COUNTS = {g[0]: sum(1 for i in ITEMS if i[0] == g[0]) for g in GROUPS}
SHOW = "document.dispatchEvent(new Event('visibilitychange'))"       # the page is visible in the test browser


def chips(app):
    return app.ui.locator("#chips .chip-name").all_inner_texts()


def stamped(rows, stamps):
    """A state whose expenses were logged (createdAt) at the given times, whatever their dates."""
    st = make_state(rows)
    for expense, stamp in zip(st["expenses"], stamps):
        expense["createdAt"] = expense["updatedAt"] = stamp
    return st


def fold(text):
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c)).lower()


def expected_search(query, items=ITEMS):
    """The brief's order: starts with, contains, section name only; within each, section order then item order."""
    q, out = fold(query), []
    for gi, (gid, gname) in enumerate(GROUPS):
        for ii, item in enumerate(i for i in items if i[0] == gid):
            at = fold(item[1]).find(q)
            rank = 0 if at == 0 else 1 if at > 0 else 2 if q in fold(gname) else None
            if rank is not None:
                out.append((rank, gi, ii, item[1], gname))
    return [(name, section) for _, _, _, name, section in sorted(out)]


def results(app):
    return app.ui.locator("#cp-results .row").evaluate_all(
        "(els) => els.map((e) => [e.querySelector('.row-title').textContent, e.querySelector('.row-sub').textContent])")


def search(app, text):
    app.ui.locator("#cp-search").fill(text)
    return [tuple(r) for r in results(app)]


# ---------------------------------------------------------------- 1
def test_01_recency_not_frequency(app):
    # Groceries 10 times a month ago, Gas / Diesel once yesterday, Parking once today (by when each was logged)
    rows = [("2026-11-14", 1000 + i, "groceries", "credit", "", "") for i in range(10)]
    rows += [("2026-10-01", 4000, "gas", "credit", "", ""), ("2026-09-01", 300, "transportation.parking", "credit", "", "")]
    stamps = [f"2026-10-15T{10 + i}:00:00.000Z" for i in range(10)] + ["2026-11-14T18:00:00.000Z", "2026-11-15T15:00:00.000Z"]
    app.seed(stamped(rows, stamps))
    # the expense dates point the other way on purpose: only createdAt counts
    unused = [n for n in DEFAULT_CHIPS if n not in ("Groceries", "Gas / Diesel")]
    assert chips(app) == ["Parking", "Gas / Diesel", "Groceries"] + unused[:4] + ["More"]
    assert unused[:4] == ["Restaurant / Take-Out", "Shopping", "Transit", "Personal Care"]            # never used: default order
    # a hidden category never shows, however recent
    st = stamped(rows, stamps)
    [c for c in st["categories"] if c["id"] == "transportation.parking"][0]["hidden"] = True
    app.seed(st)
    assert chips(app) == ["Gas / Diesel", "Groceries"] + unused[:5] + ["More"]
    # the same timestamp: default order decides (Groceries before Transit)
    app.seed(stamped([("2026-11-10", 100, "transit", "credit", "", ""), ("2026-11-10", 100, "groceries", "credit", "", "")],
                     ["2026-11-10T10:00:00.000Z"] * 2))
    assert chips(app)[:3] == ["Groceries", "Transit", "Restaurant / Take-Out"]
    # a new user sees the defaults
    app.seed(make_state([]))
    assert chips(app) == DEFAULT_CHIPS + ["More"]
    assert "daysAgoStr(90)" not in source("app.js")[source("app.js").index("function rankTopCategories"):][:900]
    assert app.console_errors == []


# ---------------------------------------------------------------- 2
def test_02_order_fixed_on_add(app):
    app.seed(stamped([("2026-11-10", 100, "groceries", "credit", "", ""), ("2026-11-11", 100, "gas", "credit", "", "")],
                     ["2026-11-10T10:00:00.000Z", "2026-11-11T10:00:00.000Z"]))
    start = chips(app)
    assert start[:2] == ["Gas / Diesel", "Groceries"] and start.index("Transit") == 4
    app.add("12", "Transit")                                             # not the first chip
    assert chips(app) == start and len(app.expenses()) == 3
    app.ui.locator(".toast-undo").click()                                # Undo keeps the order too
    assert chips(app) == start and len(app.expenses()) == 2
    app.add("12", "Transit")
    # sheets and re-renders on the Add screen do not move chips either
    app.ui.locator("#details-row").click()
    app.ui.locator("#d-done").click()
    app.ui.locator(".chip-more").click()
    app.page.keyboard.press("Escape")
    app.tab("add")                                                       # tapping Add while on Add is not an arrival
    assert chips(app) == start
    app.tab("history")
    app.tab("add")
    assert chips(app) == ["Transit", "Gas / Diesel", "Groceries"] + [n for n in start[2:7] if n != "Transit"] + ["More"]
    # the seventh-slot rule is unchanged: a More pick outside the seven borrows the last slot for this entry
    now = chips(app)
    app.more_pick("Pets")
    assert chips(app) == now[:6] + ["Pets", "More"]
    app.chip("Pets").click()
    assert chips(app) == now
    assert app.console_errors == []


# ---------------------------------------------------------------- 3
def test_03_foreground_reranks_only_an_empty_draft(app):
    app.seed(stamped([("2026-11-10", 100, "groceries", "credit", "", "")], ["2026-11-10T10:00:00.000Z"]))
    start = chips(app)
    app.add("12", "Transit")
    assert chips(app) == start
    app.type_amount("7")                                                 # an amount typed: no re-rank
    app.page.evaluate(SHOW)
    assert chips(app) == start and app.amount() == "$7"
    app.ui.locator('[data-key="back"]').click()
    app.chip("Shopping").click()                                         # a category selected, no amount: no re-rank
    app.page.evaluate(SHOW)
    assert chips(app) == start and app.chip("Shopping").get_attribute("aria-pressed") == "true"
    app.chip("Shopping").click()                                         # empty draft: re-ranks
    app.page.evaluate(SHOW)
    assert chips(app) == ["Transit", "Groceries"] + [n for n in start[1:7] if n != "Transit"] + ["More"]
    # not while a sheet is open
    app.add("3", "Medical")
    app.ui.locator("#details-row").click()
    before = chips(app)
    app.page.evaluate(SHOW)
    app.ui.locator("#d-done").click()
    assert chips(app) == before
    assert app.console_errors == []


# ---------------------------------------------------------------- 4
def test_04_more_sections_view(make_app):
    app = make_app()
    app.ui.locator(".chip-more").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Choose a category"
    box = app.ui.locator("#cp-search")
    assert (box.get_attribute("type"), box.get_attribute("enterkeyhint"), box.get_attribute("autocomplete"), box.get_attribute("aria-label")) == (
        "search", "search", "off", "Search categories")
    assert app.page.evaluate("document.activeElement.id") != "cp-search"                 # not autofocused
    tiles = app.ui.locator("#cp-tiles .cp-tile")
    assert tiles.count() == 8 and app.ui.locator("#cp-tiles .cp-name").all_inner_texts() == GROUP_NAMES
    assert app.ui.locator("#cp-tiles .cp-count").all_inner_texts() == [f"{COUNTS[g[0]]} categories" for g in GROUPS]
    food = app.ui.locator('#cp-tiles [data-section="food"]')
    assert food.locator(".cp-count").inner_text() == "2 categories" and food.get_attribute("aria-label") == "Food, 2 categories"
    assert food.locator(".cp-emoji").inner_text() == "🍽️" or len(food.locator(".cp-emoji").inner_text()) >= 1
    # two per row, at least 64 px tall, in the section's colour pair, with readable text
    app.page.wait_for_timeout(300)
    boxes = tiles.evaluate_all("(els) => els.map((e) => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), r.width, r.height]; })")
    assert all(b[3] >= 64 for b in boxes) and boxes[0][1] == boxes[1][1] and boxes[0][0] < boxes[1][0] and boxes[2][1] > boxes[0][1]
    assert boxes[2][0] == boxes[0][0] and all(b[0] >= 0 and b[0] + b[2] <= 390 for b in boxes)
    for scheme, target in (("light", app), ("dark", None)):
        if target is None:
            target = make_app(scheme="dark")
            target.ui.locator(".chip-more").click()
            target.page.wait_for_timeout(300)
        looks = target.ui.locator("#cp-tiles .cp-tile").evaluate_all("""(els) => els.map((e) => { const s = getComputedStyle(e), root = getComputedStyle(document.documentElement);
          const hue = ['teal', 'blue', 'orange', 'purple', 'green', 'rose', 'indigo', 'slate'][Number(/gc(\\d)/.exec(e.className)[1])];
          return { bg: s.backgroundColor, edge: s.borderTopColor, text: s.color, count: getComputedStyle(e.querySelector('.cp-count')).color,
            fill: root.getPropertyValue('--c-' + hue).trim(), tokenEdge: root.getPropertyValue('--c-' + hue + '-edge').trim(),
            sheet: getComputedStyle(document.querySelector('.sheet')).backgroundColor }; })""")
        assert len({l["bg"] for l in looks}) == 8
        for l in looks:
            assert abs(luminance(l["bg"]) - luminance(l["fill"])) < 0.002 and abs(luminance(l["edge"]) - luminance(l["tokenEdge"])) < 0.002
            assert contrast(l["text"], l["bg"]) >= 4.5 and contrast(l["count"], l["bg"]) >= 4.5, (scheme, l)
            assert contrast(l["edge"], l["sheet"]) >= 3, (scheme, l)
    # the tiles pop in with a short stagger: under 200 ms in all
    timing = tiles.evaluate_all("(els) => els.map((e) => { const s = getComputedStyle(e); return [s.animationName, parseFloat(s.animationDuration) * 1000 + parseFloat(s.animationDelay) * 1000]; })")
    assert all(t[0] == "tile-in" for t in timing) and max(t[1] for t in timing) < 200 and timing[0][1] < timing[7][1]

    # a tile slides forward to that section's categories as chips
    food.click()
    assert app.ui.locator("#sheet-title").inner_text() == "Food" and app.ui.locator("[data-sheet-back]").count() == 1
    assert app.ui.locator("#cp-chips .chip-name").all_inner_texts() == ["Groceries", "Restaurant / Take-Out"]
    assert "slide-fwd" in app.ui.locator(".sheet-body").get_attribute("class")
    assert app.page.evaluate("getComputedStyle(document.getElementById('cp-chips')).gridTemplateColumns.split(' ').length") == 4
    assert app.ui.locator("#cp-chips .chip").first.evaluate("(e) => e.getBoundingClientRect().height") >= 56
    # Back returns to the tiles
    app.ui.locator("[data-sheet-back]").click()
    assert app.ui.locator("#cp-tiles .cp-tile").count() == 8 and app.ui.locator("#sheet-title").inner_text() == "Choose a category"
    assert "slide-back" in app.ui.locator(".sheet-body").get_attribute("class") and app.ui.locator("[data-sheet-back]").count() == 0
    # Escape goes up a level from a section, then closes
    app.ui.locator('#cp-tiles [data-section="insurance"]').click()
    app.page.keyboard.press("Escape")
    assert app.ui.locator("#cp-tiles").count() == 1
    # a chip selects without saving, closes the sheet, and takes the seventh slot
    app.ui.locator('#cp-tiles [data-section="insurance"]').click()
    app.ui.locator('#cp-chips .chip:has-text("Life Insurance")').click()
    assert app.sheet_hidden() and app.expenses() == [] and app.toast().count() == 0
    assert chips(app) == DEFAULT_CHIPS[:6] + ["Life Insurance", "More"]
    assert app.chip("Life Insurance").get_attribute("aria-pressed") == "true" and app.amount() == "$0"
    # the tile of the selected category's section says so; inside, the chip is checked
    app.ui.locator(".chip-more").click()
    tile = app.ui.locator('#cp-tiles [data-section="insurance"]')
    assert tile.locator(".cp-selected").inner_text() == "Selected: Life Insurance" and tile.locator(".cp-check").count() == 1
    assert tile.get_attribute("aria-label") == "Insurance, 5 categories, Selected: Life Insurance"
    assert app.ui.locator("#cp-tiles .cp-selected").count() == 1
    tile.click()
    assert app.ui.locator('#cp-chips .chip[aria-pressed="true"] .chip-name').all_inner_texts() == ["Life Insurance"]
    assert app.ui.locator("#cp-chips .chip.selected .chip-check").count() == 1
    app.close_sheet()
    # a pick that is already one of the seven just selects that chip
    app.more_pick("Groceries")
    assert chips(app) == DEFAULT_CHIPS + ["More"] and app.chip("Groceries").get_attribute("aria-pressed") == "true"

    # a section with no visible categories has no tile; counts are of visible categories
    st = make_state([])
    for c in st["categories"]:
        if c["groupId"] == "food" or c["id"] == "insurance.life-insurance":
            c["hidden"] = True
    app.seed(st)
    app.ui.locator(".chip-more").click()
    assert app.ui.locator("#cp-tiles .cp-name").all_inner_texts() == [n for n in GROUP_NAMES if n != "Food"]
    assert app.ui.locator('#cp-tiles [data-section="insurance"] .cp-count').inner_text() == "4 categories"
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 5
def test_05_search(app):
    st = make_state([])
    st["categories"].append({"id": "c_cafe", "groupId": "food", "name": "Café", "emoji": "☕", "taxTag": None, "hidden": False,
                             "builtIn": False, "order": 100})
    app.seed(st)
    items = ITEMS + [("food", "Café", "☕", None)]
    app.ui.locator(".chip-more").click()
    status = app.ui.locator("#cp-status")
    assert status.get_attribute("aria-live") == "polite"
    # park: only Parking, with its section as the sub-line; the tiles are replaced
    assert search(app, "park") == [("Parking", "Transportation")]
    assert app.ui.locator("#cp-tiles").count() == 0 and status.inner_text() == "1 category found"
    assert app.ui.locator("#cp-results .row .row-emoji").inner_text() == "🅿️"
    # INSUR: the five Insurance items plus the two insurance items in other sections
    found = search(app, "INSUR")
    assert sorted(n for n, _ in found) == sorted(["Life Insurance", "Disability Insurance", "Critical Illness Insurance", "Health / Dental Insurance",
                                                 "Other insurance", "Car Insurance", "Property / Tenant Insurance"])
    assert found == expected_search("INSUR", items) and found[0] == ("Property / Tenant Insurance", "Housing")
    assert status.inner_text() == "7 categories found"
    # accents and case are ignored, both ways
    assert search(app, "cafe") == [("Café", "Food")] and search(app, "CAFÉ") == [("Café", "Food")]
    # order: names that start with the query, then names that contain it, then section-name matches
    for query in ["re", "in", "food", "tra", "o", "house", "misc"]:
        assert search(app, query) == expected_search(query, items), query
    assert search(app, "food") == [("Groceries", "Food"), ("Restaurant / Take-Out", "Food"), ("Café", "Food")]      # section name only
    tra = search(app, "tra")
    assert tra[0] == ("Transit", "Transportation") and tra[1] == ("Travel / Vacation", "Recreation")              # starts-with first, by section
    assert tra[-1][1] == "Transportation" and "tra" not in tra[-1][0].lower()                                      # section-only last
    # no matches: the message; clearing shows the tiles again
    assert search(app, "xyz") == [] and status.inner_text() == 'No categories match "xyz".'
    assert app.ui.locator("#cp-tiles").count() == 0
    app.ui.locator("#cp-search").fill("")
    assert app.ui.locator("#cp-tiles .cp-tile").count() == 8 and status.inner_text() == "" and app.ui.locator("#cp-results").count() == 0
    app.ui.locator("#cp-search").fill("   ")
    assert app.ui.locator("#cp-tiles .cp-tile").count() == 8
    # the native clear button fires a search event with an empty field
    app.ui.locator("#cp-search").fill("park")
    app.page.evaluate("(() => { const i = document.getElementById('cp-search'); i.value = ''; i.dispatchEvent(new Event('search')); })()")
    assert app.ui.locator("#cp-tiles .cp-tile").count() == 8
    # typing keeps the focus in the field
    app.ui.locator("#cp-search").click()
    app.page.keyboard.type("par")
    assert app.page.evaluate("document.activeElement.id") == "cp-search" and len(results(app)) == 1
    # a result selects and closes, exactly as a chip in a section does
    app.ui.locator("#cp-results .row").click()
    assert app.sheet_hidden() and app.expenses() == []
    assert chips(app) == DEFAULT_CHIPS[:6] + ["Parking", "More"] and app.chip("Parking").get_attribute("aria-pressed") == "true"
    # back from a section clears the search (the field is empty again)
    app.ui.locator(".chip-more").click()
    assert app.ui.locator("#cp-search").input_value() == ""
    # hidden categories are excluded
    st = make_state([])
    [c for c in st["categories"] if c["id"] == "transportation.parking"][0]["hidden"] = True
    app.seed(st)
    app.ui.locator(".chip-more").click()
    assert search(app, "park") == [] and status.inner_text() == 'No categories match "park".'
    assert "Parking" not in [n for n, _ in search(app, "transportation")]
    assert app.console_errors == []


# ---------------------------------------------------------------- 6
def test_06_profile_row(app):
    app.tab("profile")
    row = app.ui.locator("#btn-modify-categories")
    assert row.locator(".row-title").inner_text() == "Modify categories"
    assert app.ui.locator("#category-summary").inner_text() == "45 categories in 8 sections"
    # no category rows, and no Add category row, on Profile itself
    assert app.ui.locator("#category-settings .row").count() == 1 and app.ui.locator("#btn-add-category, #category-list").count() == 0
    page_text = app.ui.locator("#view").inner_text()
    assert "Groceries" not in page_text and "Add category" not in page_text and "Mortgage / Rent" not in page_text
    assert app.ui.locator("#view .section-head").all_inner_texts()[2] == "Categories"
    # hide one
    app.cat_edit("Parking")
    app.ui.locator("#c-hidden").check()
    app.ui.locator("#c-save").click()
    app.close_sheet()
    assert app.ui.locator("#category-summary").inner_text() == "45 categories in 8 sections · 1 hidden"
    # counts include custom categories
    app.cat_add("recreation")
    app.ui.locator("#c-name").fill("Climbing")
    app.ui.locator("#c-save").click()
    app.close_sheet()
    assert app.ui.locator("#category-summary").inner_text() == "46 categories in 8 sections · 1 hidden"
    app.cat_edit("Climbing")
    app.ui.locator("#c-hidden").check()
    app.ui.locator("#c-save").click()
    app.close_sheet()
    assert app.ui.locator("#category-summary").inner_text() == "46 categories in 8 sections · 2 hidden"
    assert app.console_errors == []


# ---------------------------------------------------------------- 7
def test_07_manager(app):
    st = make_state([("2026-11-10", 100, "groceries", "credit", "", "")])
    for c in st["categories"]:
        if c["id"] in ("transportation.parking", "food.restaurant-take-out"):
            c["hidden"] = True
    app.seed(st)
    app.tab("profile")
    app.ui.locator("#btn-modify-categories").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Categories" and app.ui.locator("#cp-search").count() == 1
    # counts on the tiles include hidden categories
    assert app.ui.locator("#cp-tiles .cp-count").all_inner_texts() == [f"{COUNTS[g[0]]} categories" for g in GROUPS]
    assert app.ui.locator("#cp-tiles .cp-selected").count() == 0
    # a section view lists hidden items with the badge, as rows, and ends with Add category
    app.ui.locator('#cp-tiles [data-section="transportation"]').click()
    assert app.ui.locator("#sheet-title").inner_text() == "Transportation"
    assert app.ui.locator("#cm-list .row-title").all_inner_texts() == [i[1] for i in ITEMS if i[0] == "transportation"]
    assert app.ui.locator('#cm-list .row:has-text("Parking") .badge').all_inner_texts() == ["Hidden"]
    assert app.ui.locator("#cm-list .badge").count() == 1
    assert app.ui.locator("#cm-list > *").last.inner_text() == "Add category"
    # row -> edit -> back returns to that section
    app.ui.locator('#cm-list .row:has-text("Transit")').click()
    assert app.ui.locator("#sheet-title").inner_text() == "Edit category" and app.ui.locator("#c-name").input_value() == "Transit"
    assert "slide-fwd" in app.ui.locator(".sheet-body").get_attribute("class")
    app.ui.locator("[data-sheet-back]").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Transportation" and app.ui.locator("#cm-list .row").count() == COUNTS["transportation"] + 1
    assert "slide-back" in app.ui.locator(".sheet-body").get_attribute("class")
    # Cancel returns there too, changing nothing
    app.ui.locator('#cm-list .row:has-text("Transit")').click()
    app.ui.locator("#c-name").fill("Nope")
    app.ui.locator("#c-cancel").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Transportation" and app.category("Transit")["name"] == "Transit"
    # a rename saved returns to the section list showing the new name, with the toast
    app.ui.locator('#cm-list .row:has-text("Transit")').click()
    app.ui.locator("#c-name").fill("Bus & train")
    app.ui.locator("#c-save").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Transportation" and app.toast().inner_text() == "Category saved"
    names = app.ui.locator("#cm-list .row-title").all_inner_texts()
    assert "Bus & train" in names and "Transit" not in names
    # validation still applies, and keeps the sheet open
    app.ui.locator('#cm-list .row:has-text("Bus & train")').click()
    app.ui.locator("#c-name").fill("groceries")
    app.ui.locator("#c-save").click()
    assert "already a category" in app.ui.locator("#c-error").inner_text() and app.ui.locator("#sheet-title").inner_text() == "Edit category"
    app.ui.locator("[data-sheet-back]").click()
    # back from the section returns to the tiles
    app.ui.locator("[data-sheet-back]").click()
    assert app.ui.locator("#cp-tiles .cp-tile").count() == 8

    # Add category in Recreation: that section is preselected, the item lands in Recreation, and we return to its list
    app.ui.locator('#cp-tiles [data-section="recreation"]').click()
    app.ui.locator("#cm-add").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Add category" and app.ui.locator("#c-group").input_value() == "recreation"
    app.ui.locator("#c-name").fill("Climbing")
    app.ui.locator("#c-emoji").fill("🧗")
    app.ui.locator("#c-save").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Recreation" and app.toast().inner_text() == "Category saved"
    assert app.ui.locator("#cm-list .row-title").all_inner_texts()[-1] == "Climbing"
    assert app.category("Climbing")["groupId"] == "recreation" and app.category("Climbing")["builtIn"] is False
    # deleting it returns to the list as well
    app.ui.locator('#cm-list .row:has-text("Climbing")').click()
    app.ui.locator("#c-delete").click()
    app.ui.locator("#c-confirm-delete").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Recreation" and app.toast().inner_text() == "Category deleted"
    assert "Climbing" not in app.ui.locator("#cm-list .row-title").all_inner_texts()
    app.ui.locator("[data-sheet-back]").click()

    # search includes hidden items, marked Hidden
    assert search(app, "park") == [("Parking", "Transportation")]
    assert app.ui.locator("#cp-results .row .badge").all_inner_texts() == ["Hidden"]
    assert app.ui.locator("#cp-status").inner_text() == "1 category found"
    found = search(app, "re")
    assert ("Restaurant / Take-Out", "Food") in found
    # result -> edit -> back returns to the results with the query kept
    app.ui.locator('#cp-results .row:has-text("Restaurant / Take-Out")').click()
    assert app.ui.locator("#sheet-title").inner_text() == "Edit category" and app.ui.locator("#c-hidden").is_checked()
    app.ui.locator("[data-sheet-back]").click()
    assert app.ui.locator("#sheet-title").inner_text() == "Categories" and app.ui.locator("#cp-search").input_value() == "re"
    assert [tuple(r) for r in results(app)] == found and app.ui.locator("#cp-tiles").count() == 0
    # ...and so does a save from there, updated
    app.ui.locator('#cp-results .row:has-text("Restaurant / Take-Out")').click()
    app.ui.locator("#c-hidden").uncheck()
    app.ui.locator("#c-save").click()
    assert app.ui.locator("#cp-search").input_value() == "re" and app.toast().inner_text() == "Category saved"
    assert app.ui.locator('#cp-results .row:has-text("Restaurant / Take-Out") .badge').count() == 0
    # Escape in the edit sheet goes up a level; × closes everything
    app.ui.locator('#cp-results .row:has-text("Restaurant / Take-Out")').click()
    app.page.keyboard.press("Escape")
    assert app.ui.locator("#cp-search").input_value() == "re"
    app.ui.locator('#cp-results .row:has-text("Restaurant / Take-Out")').click()
    app.ui.locator("[data-sheet-close]").first.click()
    assert app.sheet_hidden()
    assert app.page.evaluate("document.activeElement.id") == "btn-modify-categories"
    assert app.ui.locator("#category-summary").inner_text() == "45 categories in 8 sections · 1 hidden"
    # a tile shows even for a section with no categories
    st = make_state([])
    for c in st["categories"]:                                           # every Debt Payments item moved elsewhere
        if c["groupId"] == "debt":
            c["groupId"] = "misc"
    app.seed(st)
    app.tab("profile")
    app.ui.locator("#btn-modify-categories").click()
    assert app.ui.locator("#cp-tiles .cp-tile").count() == 8
    assert app.ui.locator('#cp-tiles [data-section="debt"] .cp-count').inner_text() == "0 categories"
    app.ui.locator('#cp-tiles [data-section="debt"]').click()
    assert app.ui.locator("#cm-list .row").count() == 1 and app.ui.locator("#cm-add").count() == 1
    assert app.console_errors == [] and app.dialogs == []


# ---------------------------------------------------------------- 8
def test_08_no_external_requests_and_reduced_motion(make_app):
    app = make_app()
    app.ui.locator(".chip-more").click()
    search(app, "insur")
    app.ui.locator("#cp-search").fill("")
    app.ui.locator('#cp-tiles [data-section="food"]').click()
    app.ui.locator("#cp-chips .chip").first.click()
    app.tab("profile")
    app.ui.locator("#btn-modify-categories").click()
    search(app, "café")
    app.close_sheet()
    prefix = app.base_url + "/"
    assert [u for u in app.requests if not u.startswith(prefix) and not u.startswith("data:")] == []
    assert not any("insur" in u or "caf" in u for u in app.requests)
    assert app.console_errors == []

    calm = make_app(reduced_motion="reduce")
    calm.ui.locator(".chip-more").click()
    assert set(calm.ui.locator("#cp-tiles .cp-tile").evaluate_all("(els) => els.map((e) => getComputedStyle(e).animationName)")) == {"none"}
    calm.ui.locator('#cp-tiles [data-section="food"]').click()
    assert calm.page.evaluate("getComputedStyle(document.querySelector('.sheet-body')).animationName") == "none"
    assert calm.ui.locator("#cp-chips .chip").count() == 2


# ---------------------------------------------------------------- 9
def test_09_version(make_app):
    sw = source("sw.js")
    assert "const VERSION = '0.2.5';" in sw and "const CACHE = 'ds-' + VERSION;" in sw
    assert "version: '0.2.5'," in source("app.js") and not re.search(r"0\.2\.[01234]\b", sw + source("app.js"))
    app = make_app(service_workers="allow", cards=None, tax=None)
    wait_cached(app.page, cache="ds-0.2.5")
    assert app.page.evaluate("caches.keys()") == ["ds-0.2.5"]
    app.tab("profile")
    assert app.ui.locator("#app-version").inner_text() == "Version 0.2.5"
    assert app.console_errors == []
