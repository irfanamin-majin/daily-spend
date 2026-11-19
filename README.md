# Daily Spend

A small expense tracker for Canadians, built to make typing in an expense on a phone as fast as possible: type the amount, tap a category, press Save.

It is a plain static web app (HTML, CSS and JavaScript, no build step, no dependencies) that can be added to a phone's home screen and works offline.

## What it does

- **Add**: an in-page keypad, category chips, a Save button that turns green once the amount and category are in, and a one-line details row for the date, payment method or card, merchant, note and location.
- **Quick repeat**: log an earlier expense again today from the Recent sheet, a swipe, or the Edit sheet.
- **Merchant memory**: a merchant you have used before offers its usual category.
- **History**: search by merchant or note, filter by category, by card or whole institution, or by location; swipe a row to delete or repeat it.
- **Categories**: 45 everyday items arranged in 8 fixed budget groups (Housing, Debt Payments, Communications, Food, Transportation, Recreation, Miscellaneous, Insurance). You can add, rename, move and hide items.
- **Summary**: for the month, the last 3 months or the last 12; a donut by group and bars per day or per month that you can tap, each group opening to its items, totals by card, and a Tax time card for medical, donation and childcare categories.
- **Profile**: your cards (picked from a built-in Canadian list or added by hand), location setting, categories, CSV backup and restore.
- **Location (optional)**: saves a GPS pin with an expense. Off unless you turn it on or tap the button.

Amounts are in Canadian dollars, as totals only (no sales tax split). English only.

## Privacy

> Your entries stay on this device. No account, no tracking. Nothing is sent anywhere, except that opening a location in Google Maps shares that location with Google.

In detail:

- Everything you enter is kept in this browser's storage on your device. There is no server, no account and no analytics.
- The page only loads its own files. A content security policy in `index.html` blocks requests to anywhere else.
- "Open in Google Maps" is an ordinary link. Nothing is shared with Google unless you tap it, and the app tells you so the first time.
- Cards are stored by name only. The app never asks for a card number, expiry date or security code; the last 4 digits are optional.
- The only way data leaves the device is a backup you copy or download yourself.

Because the data lives only in the browser, clearing the browser's site data deletes it. Use **Profile → Backup** now and then.

## Files

| Path | What it is |
|---|---|
| `index.html`, `styles.css`, `app.js` | The app |
| `sw.js` | Service worker: keeps the app's files on the device for offline use |
| `manifest.webmanifest`, `icons/` | Home-screen install details and icons |
| `data/cards-ca.json` | The built-in list of Canadian cards (names only) |
| `tools/make_icons.py` | Redraws the icons (needs Pillow) |
| `tests/` | Automated tests |

All paths are relative, so the site works from a subfolder such as `https://<user>.github.io/daily-spend/`.

## Running it locally

Any static file server works. From the folder that contains this one:

```
python3 -m http.server 8000
```

Then open `http://127.0.0.1:8000/daily-spend/`. (Service workers and location need `https` or `localhost`/`127.0.0.1`.)

## Running the tests

The tests use Python, [pytest](https://pytest.org) and [Playwright](https://playwright.dev/python/) with Google Chrome.

```
pip install pytest playwright
python3 -m pytest tests -q
```

- The tests start their own local server and open the site from a subpath, the way GitHub Pages serves it.
- Chrome is expected at `/usr/bin/google-chrome`. Change `CHROME` in `tests/conftest.py` if yours is elsewhere.
- `tests/test_v1.py` holds the original acceptance tests; `tests/test_v2.py` covers offline use, location, cards, charts, quick repeat, search, swipes, first-run setup, backups and data migration; `tests/test_v2_1.py` covers the card picker and chart scaling; `tests/test_v2_2.py` covers budget groups, the move from the old categories, and institution badges; `tests/test_v2_3.py` covers the Save button, the institution filter, group colours and time ranges.
- Screenshots: `python3 tests/take_screenshots.py <output folder>`.

## Releasing a change

The service worker serves files from its cache first, so a change only reaches people who have the app installed when the version changes:

1. Set the same new version in `sw.js` (`VERSION`) and in `app.js` (`STRINGS.version`).
2. Publish. People with the app open see an "Update ready · Reload" banner.

## Card list

`data/cards-ca.json` holds issuers and card names, with each card's kind (`credit`, `debit` or `prepaid`) and networks. Each issuer also has a `short` name used for its badge in the app. It is reference data only: no logos, no artwork, no brand colours, no rates or offers. Card and issuer names belong to their owners; Daily Spend is not affiliated with or endorsed by any of them.
