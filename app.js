(function () {
'use strict';

/* =====================================================================
   1. Strings (every user-visible text; English only)
   ===================================================================== */
const STRINGS = {
  appName: 'Daily Spend',
  version: '0.2.0',
  versionLabel: (v) => `Version ${v}`,
  privacy: 'Your entries stay on this device. No account, no tracking. Nothing is sent anywhere, except that opening a location in Google Maps shares that location with Google.',
  tabs: { add: 'Add', history: 'History', summary: 'Summary', profile: 'Profile' },
  titles: { add: 'Add expense', history: 'History', summary: 'Summary', profile: 'Profile' },
  months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  weekdaysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
  today: 'Today',
  yesterday: 'Yesterday',
  sep: ' · ',
  close: 'Close',
  cancel: 'Cancel',
  save: 'Save',
  done: 'Done',
  del: 'Delete',
  dismiss: 'Dismiss',
  // Add
  amountLabel: (a) => `Amount ${a}`,
  keyLabels: { '.': 'Decimal point', back: 'Backspace. Hold to clear' },
  detailsRowLabel: 'Date, payment method, merchant, note and location',
  addMerchantOrNote: 'Add merchant or note',
  enterAmountFirst: 'Enter an amount first',
  moreChip: 'More',
  moreChipLabel: 'More categories',
  chipLabel: (name) => `Save to ${name}`,
  saved: (amount, cat, day) => `Saved ${amount} · ${cat}${day ? ' · ' + day : ''}`,
  undo: 'Undo',
  undone: 'Expense removed',
  // Details sheet
  detailsTitle: 'Details',
  date: 'Date',
  paymentMethod: 'Payment method',
  merchant: 'Merchant',
  merchantPlaceholder: 'Where did you pay?',
  note: 'Note',
  notePlaceholder: 'Optional',
  suggestionsLabel: 'Earlier merchants',
  allCategoriesTitle: 'All categories',
  // History
  prevMonth: 'Previous month',
  nextMonth: 'Next month',
  monthTotal: 'Total this month',
  noExpenses: (month) => `No expenses in ${month}.`,
  addExpense: 'Add an expense',
  hiddenSuffix: ' (hidden)',
  editTitle: 'Edit expense',
  amount: 'Amount',
  category: 'Category',
  deleteConfirm: 'Delete this expense?',
  errAmount: 'Enter an amount above $0.',
  errDate: 'Choose a date.',
  expenseSaved: 'Changes saved',
  expenseDeleted: 'Expense deleted',
  // Summary
  expenseCount: (n) => `${n} ${n === 1 ? 'expense' : 'expenses'}`,
  byCategory: 'By category',
  taxTime: (year) => `Tax time ${year}`,
  taxRows: { medical: 'Medical & dental', donation: 'Donations', childcare: 'Childcare' },
  taxFootnote: 'Totals of expenses in tagged categories. Eligibility rules apply.',
  // Profile: storage
  storageStandalone: 'Saved on this device',
  storageEmbedded: 'Saved in this browser only. This test version can be cleared, so copy a backup now and then.',
  storageMemory: 'Not saving: this browser blocked storage. Copy a backup before you close this page.',
  testNotice: 'Test version: entries are kept in this browser only and may be cleared. Copy a backup from Profile.',
  corruptKept: 'Saved data could not be read, so the app started fresh. The unreadable data was kept in this browser.',
  corruptLost: 'Saved data could not be read, so the app started fresh.',
  // Profile: backup
  backup: 'Backup',
  copyBackup: 'Copy backup (CSV)',
  downloadCsv: 'Download CSV',
  restore: 'Restore from backup',
  copied: (n) => `Backup copied (${n} ${n === 1 ? 'expense' : 'expenses'})`,
  copyFallbackTitle: 'Copy backup',
  copyFallbackHelp: 'Copying was blocked here. Select all and copy the text below, then paste it somewhere safe.',
  selectAll: 'Select all',
  backupText: 'Backup text',
  downloaded: 'Backup saved',
  rateLimited: 'Try again in a moment',
  downloadUnavailable: "Download isn't available here. Use Copy backup instead.",
  restoreTitle: 'Restore from backup',
  restoreHelp: 'Adds expenses from a Daily Spend backup. Expenses already here are never changed.',
  chooseFile: 'Choose a .csv file',
  orPaste: 'Or paste CSV text',
  restoreBtn: 'Restore',
  restoreResult: (r, a, i) =>
    `Restored ${r} ${r === 1 ? 'expense' : 'expenses'}. Skipped ${a} already here and ${i} invalid ${i === 1 ? 'row' : 'rows'}.`,
  restoreBadHeader: "This doesn't look like a Daily Spend backup. The first line needs date, amount and category columns.",
  restoreEmpty: 'Choose a file or paste CSV text first.',
  restoreReadError: 'That file could not be read.',
  // Profile: categories
  categories: 'Categories',
  addCategory: 'Add category',
  editCategory: 'Edit category',
  hidden: 'Hidden',
  catName: 'Name',
  catEmoji: 'Emoji',
  catTaxTag: 'Tax tag',
  catHide: 'Hide from Add',
  taxTags: { none: 'None', medical: 'Medical', donation: 'Donation', childcare: 'Childcare' },
  errCatName: 'Enter a name.',
  errCatDup: 'There is already a category with that name.',
  errCatEmoji: 'Use one or two emoji.',
  deleteCategory: 'Delete category',
  deleteCategoryConfirm: 'Delete this category?',
  catInUse: (n) => `Used by ${n} ${n === 1 ? 'expense' : 'expenses'}, so it can be hidden but not deleted.`,
  catSaved: 'Category saved',
  catDeleted: 'Category deleted',
  // Profile: delete all
  deleteAll: 'Delete all data',
  deleteAllHelp: 'This removes every expense, your cards, your own categories and your settings from this browser. It cannot be undone. Type DELETE to confirm.',
  deleteAllInput: 'Type DELETE',
  deleteAllWord: 'DELETE',
  deleteAllDone: 'All data deleted',
  about: 'About',
  // Shared
  remove: 'Remove',
  back: 'Back',
  next: 'Next',
  skip: 'Skip',
  clear: 'Clear',
  continue: 'Continue',
  optional: 'Optional',
  again: 'Again',
  reload: 'Reload',
  updateReady: 'Update ready',
  // Location
  location: 'Location',
  pin: '📍',
  pinFinding: '📍…',
  hasLocation: 'Has location',
  locAdd: '📍 Add current location',
  locAddPlain: 'Add current location',
  locNowNote: 'This records where you are now, not where the expense happened.',
  locFinding: 'Finding your location…',
  locAccuracy: (m) => ` (±${m} m)`,
  locAdded: (accuracy) => `📍 Location added${accuracy}`,
  locHas: (accuracy) => `📍 Location${accuracy}`,
  locDenied: "Location is off for Daily Spend. You can allow it in your phone's settings.",
  locFailed: "Couldn't get your location. Try again in a moment.",
  openInMaps: 'Open in Google Maps',
  mapsNotice: 'This opens Google Maps and shares this location with Google.',
  autoLocation: 'Add location automatically',
  autoLocationHelp: 'Saves a pin with each new expense. The pin stays on this device.',
  offByDefault: 'Off unless you turn it on. You can change it later in Profile.',
  // Quick repeat and the usual category
  recent: 'Recent',
  recentLabel: 'Recent expenses, to log one again',
  recentTitle: 'Recent',
  recentHelp: 'Again logs a copy dated today.',
  recentEmpty: 'Nothing here yet.',
  againLabel: (what) => `Log ${what} again today`,
  logAgainToday: 'Log again today',
  usual: (emoji, name) => `Usual: ${emoji} ${name}`,
  usualLabel: (name) => `Save to ${name}, the usual category for this merchant`,
  // History: search and filters
  searchPlaceholder: 'Search merchant or note',
  searchLabel: 'Search expenses by merchant or note',
  filterCategory: 'Category',
  filterCategoryCount: (n) => `Category · ${n}`,
  filterCategoryTitle: 'Filter by category',
  filterCard: 'Card',
  filterCardTitle: 'Filter by card',
  filterAllCards: 'All cards and other ways',
  filterHasLocation: '📍 Has location',
  filterRemovable: (label) => `${label} ×`,
  filterRemove: (label) => `Remove filter: ${label}`,
  cashAndOther: 'Cash & other',
  cashAndOtherHelp: 'Expenses not paid with one of your cards',
  resultCount: (n) => `${n} ${n === 1 ? 'result' : 'results'} across all months`,
  noResults: 'No matching expenses.',
  // Summary: charts and cards
  byCard: 'By card',
  otherSlice: 'Other categories',
  sliceLabel: (name, amount, pct) => `${name}, ${amount}, ${pct}%`,
  barLabel: (day, amount) => `${day}, ${amount}`,
  donutLabel: 'Spending by category. Each slice opens its expenses.',
  dailyTitle: 'Day by day',
  dailyLabel: 'Spending by day. Each bar opens that day.',
  chartHint: 'Tap a slice or a bar to see its expenses.',
  // Cards
  myCards: 'My cards',
  otherWays: 'Other ways',
  noCards: 'No cards yet. Add the ones you pay with to see spending by card.',
  addCard: 'Add card',
  editCard: 'Edit card',
  archived: 'Archived',
  archivedSuffix: ' (archived)',
  restoreCard: 'Restore',
  restoreCardLabel: (name) => `Restore ${name}`,
  cardNumberNote: "Only the card's name is stored. Never enter your full card number.",
  cardSearchPlaceholder: 'Search by bank or card name',
  cardSearchLabel: 'Search the card list',
  cardKindLabel: 'Card type',
  cardKindFilters: { all: 'All', credit: 'Credit', debit: 'Debit', prepaid: 'Prepaid' },
  cardKinds: { credit: 'Credit', debit: 'Debit', prepaid: 'Prepaid' },
  cardListLoading: 'Loading the card list…',
  cardListFailed: "The card list couldn't be loaded. You can still add your card yourself.",
  cardNoMatch: 'No cards match. You can add yours yourself.',
  cardManual: "Can't find your card? Add it yourself",
  cardAdded: 'Added',
  otherIssuer: 'Other',
  cardIssuer: 'Bank or issuer',
  cardIssuerPlaceholder: 'For example, your bank',
  cardName: 'Card name',
  cardNamePlaceholder: 'The name printed on the card',
  cardKind: 'Type',
  cardNetwork: 'Network',
  cardNetworkNone: 'Not sure',
  cardNickname: 'Nickname',
  cardLast4: 'Last 4 digits',
  cardColour: 'Colour',
  colourNames: { teal: 'Teal', blue: 'Blue', indigo: 'Indigo', purple: 'Purple', rose: 'Rose', orange: 'Orange', green: 'Green', slate: 'Slate' },
  last4Dots: (d) => `•••• ${d}`,
  errCardName: "Enter the card's name.",
  errLast4: 'Enter exactly 4 digits, or leave it empty.',
  errCardNumber: "That looks like a card number. Use only the card's name.",
  removeCard: 'Remove card',
  removeCardConfirm: 'Remove this card?',
  archiveCardConfirm: (n) => `Remove this card? It stays on the ${n} ${n === 1 ? 'expense' : 'expenses'} that used it and moves to Archived.`,
  cardAddedToast: 'Card added',
  cardSaved: 'Card saved',
  cardArchived: 'Card archived',
  cardRemoved: 'Card removed',
  cardRestored: 'Card restored',
  // First-run setup
  obStep: (n, of) => `Step ${n} of ${of}`,
  obTitle1: 'Track spending in seconds',
  obBody1: 'Type the amount, tap a category, and it is saved. Add the merchant, card or location only when you want to.',
  obTitle2: 'Pick your cards',
  obBody2: 'Choose the cards you pay with to see spending by card. This is optional.',
  obCardListFailed: "The card list couldn't be loaded. You can add cards later in Profile.",
  obTitle3: 'Add location to expenses?',
  obBody3: 'Daily Spend can save a pin of where you were with each expense. Turning this on asks for permission.',
  runSetupAgain: 'Run setup again'
};

/* =====================================================================
   2. Constants
   ===================================================================== */
const STORAGE_KEY = 'dailyspend.state';
const LEGACY_KEY = 'dailyspend.v1';          // the v1 test page; read once and migrated
const SCHEMA_VERSION = 2;
const MAX_CENTS = 9999999;
const BOM = '﻿';
const CSV_HEADER = ['id', 'date', 'amount', 'category', 'payment_method', 'card', 'card_last4', 'merchant', 'note', 'tax_tag',
  'latitude', 'longitude', 'location_accuracy_m', 'created_at', 'updated_at'];
const TAX_TAGS = ['medical', 'donation', 'childcare'];
const DEFAULT_EMOJI = '📦';

// The only two addresses in the app. The card list is one of the site's own files.
// The maps address is only ever used as the href of a link the user taps.
const CARDS_URL = 'data/cards-ca.json';
const MAPS_URL = 'https://www.google.com/maps/search/?api=1&query=';
const GEO_OPTIONS = { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 };
const LATE_FIX_MS = 30000;                    // a fix this long after a save still attaches to it

// Fixed payment methods, in the order of the "Other ways" list.
// `other` is the label used once the user has cards of their own.
const PAYMENT_METHODS = [
  { id: 'cash', label: 'Cash', short: 'Cash' },
  { id: 'etransfer', label: 'e-Transfer (Interac)', short: 'e-Transfer' },
  { id: 'pad', label: 'Pre-authorised debit', short: 'PAD' },
  { id: 'debit', label: 'Debit card', other: 'Other debit card', short: 'Debit' },
  { id: 'credit', label: 'Credit card', other: 'Other credit card', short: 'Credit' },
  { id: 'prepaid', label: 'Prepaid card', other: 'Other prepaid card', short: 'Prepaid' },
  { id: 'other', label: 'Other', short: 'Other' }
];
const PAYMENT_ALIASES = { 'debit (interac)': 'debit' };   // the v1 label, for old backups
const DEFAULT_PAYMENT = 'credit';

const CARD_KINDS = ['credit', 'debit', 'prepaid'];
const CARD_NETWORKS = ['Visa', 'Mastercard', 'American Express', 'Interac', 'Visa Debit', 'Debit Mastercard'];
const CARD_COLOURS = ['teal', 'blue', 'indigo', 'purple', 'rose', 'orange', 'green', 'slate'];
const NO_CARD = 'none';                       // filter value for "Cash & other"

const DEFAULT_CATEGORIES = [
  ['groceries', '🛒', 'Groceries', null],
  ['dining', '☕', 'Dining & coffee', null],
  ['gas', '⛽', 'Gas & parking', null],
  ['transit', '🚇', 'Transit', null],
  ['shopping', '🛍️', 'Shopping', null],
  ['phone', '📱', 'Phone & internet', null],
  ['utilities', '💡', 'Hydro & utilities', null],
  ['housing', '🏠', 'Rent or mortgage', null],
  ['condo', '🏢', 'Condo fees', null],
  ['propertytax', '🏛️', 'Property tax', null],
  ['car', '🚗', 'Car costs', null],
  ['medical', '🩺', 'Medical & dental', 'medical'],
  ['childcare', '🧸', 'Childcare', 'childcare'],
  ['donations', '🎗️', 'Donations', 'donation'],
  ['subscriptions', '📺', 'Subscriptions', null],
  ['entertainment', '🎟️', 'Entertainment', null],
  ['travel', '✈️', 'Travel', null],
  ['personalcare', '💇', 'Personal care', null],
  ['gifts', '🎁', 'Gifts', null],
  ['other', '📦', 'Other', null]
];

const SVG_OPEN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">';
const ICONS = {
  add: SVG_OPEN + '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/></svg>',
  history: SVG_OPEN + '<path d="M8 7h12M8 12h12M8 17h12"/><circle cx="4" cy="7" r=".6"/><circle cx="4" cy="12" r=".6"/><circle cx="4" cy="17" r=".6"/></svg>',
  summary: SVG_OPEN + '<path d="M5 20v-7M12 20V5M19 20v-11"/></svg>',
  profile: SVG_OPEN + '<circle cx="12" cy="8.5" r="3.6"/><path d="M4.8 20c.9-3.6 3.7-5.4 7.2-5.4s6.3 1.8 7.2 5.4"/></svg>',
  back: SVG_OPEN + '<path d="M9 6h10a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H9l-6-6z"/><path d="M12 10l4 4M16 10l-4 4"/></svg>',
  recent: SVG_OPEN + '<path d="M4 12a8 8 0 1 0 2.6-5.9"/><path d="M4 5v4h4"/><path d="M12 8v4.3l2.8 1.7"/></svg>',
  check: '<svg class="toast-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  chev: '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
};

// Context: a top-level page (the normal case) or inside a frame (the retired test viewer).
let embedded;
try { embedded = window.self !== window.top; } catch (e) { embedded = true; }

/* =====================================================================
   3. Small helpers
   ===================================================================== */
const $ = (sel, root) => (root || document).querySelector(sel);
const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
const pad2 = (n) => (n < 10 ? '0' : '') + n;

function esc(value) {
  return String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function newId() {
  try {
    if (window.crypto && typeof crypto.randomUUID === 'function') return crypto.randomUUID();
  } catch (e) { /* fall through */ }
  let out = '';
  for (let i = 0; i < 32; i++) {
    out += Math.floor(Math.random() * 16).toString(16);
    if (i === 7 || i === 11 || i === 15 || i === 19) out += '-';
  }
  return out;
}

// Timestamps only. Calendar dates never go through this (see section 4).
function nowIso() { return new Date().toISOString(); }

// Lower case with accents removed, for matching ("Café" finds "cafe").
function fold(text) {
  let s = String(text);
  try { s = s.normalize('NFD').replace(/[\u0300-\u036f]/g, ''); } catch (e) { /* keep as is */ }
  return s.toLowerCase();
}

function graphemeCount(text) {
  try {
    if (typeof Intl !== 'undefined' && Intl.Segmenter) {
      return Array.from(new Intl.Segmenter('en', { granularity: 'grapheme' }).segment(text)).length;
    }
  } catch (e) { /* fall through */ }
  return Array.from(text.replace(/[️‍]/g, '')).length;
}

/* =====================================================================
   4. Dates (local calendar dates, never UTC)
   ===================================================================== */
function ymd(d) { return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate()); }
function todayStr() { return ymd(new Date()); }
function yesterdayStr() { const d = new Date(); d.setDate(d.getDate() - 1); return ymd(d); }
function daysAgoStr(n) { const d = new Date(); d.setDate(d.getDate() - n); return ymd(d); }

function parseYmd(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
  if (!m) return null;
  const y = +m[1], mo = +m[2], d = +m[3];
  const date = new Date(y, mo - 1, d);
  if (date.getFullYear() !== y || date.getMonth() !== mo - 1 || date.getDate() !== d) return null;
  return date;
}
function isValidYmd(s) { return typeof s === 'string' && parseYmd(s) !== null; }

function dayLabel(dateStr) {
  if (dateStr === todayStr()) return STRINGS.today;
  if (dateStr === yesterdayStr()) return STRINGS.yesterday;
  const d = parseYmd(dateStr);
  if (!d) return dateStr;
  let out = `${STRINGS.weekdaysShort[d.getDay()]}, ${STRINGS.monthsShort[d.getMonth()]} ${d.getDate()}`;
  if (d.getFullYear() !== new Date().getFullYear()) out += `, ${d.getFullYear()}`;
  return out;
}
function monthLabel(m) { return `${STRINGS.months[m.m]} ${m.y}`; }
function monthPrefix(m) { return m.y + '-' + pad2(m.m + 1); }
function currentMonth() { const d = new Date(); return { y: d.getFullYear(), m: d.getMonth() }; }
function shiftMonth(m, delta) {
  const d = new Date(m.y, m.m + delta, 1);
  return { y: d.getFullYear(), m: d.getMonth() };
}

/* =====================================================================
   5. Money (integer cents, no floating point arithmetic)
   ===================================================================== */
const moneyFmt = new Intl.NumberFormat('en-CA', { style: 'currency', currency: 'CAD' });
const intFmt = new Intl.NumberFormat('en-CA');

function fmtMoney(cents) { return moneyFmt.format(cents / 100).replace(/^CA\$/, '$'); }

// "1234.5" -> 123450. Splits on the dot; returns 0 for an empty string.
function typedToCents(str) {
  const parts = String(str).split('.');
  const whole = parts[0] === '' ? 0 : parseInt(parts[0], 10);
  const frac = ((parts[1] || '') + '00').slice(0, 2);
  return whole * 100 + parseInt(frac, 10);
}

// Strict parser for CSV amounts. Returns cents or null.
function parseAmountStrict(str) {
  const s = String(str).trim();
  if (!/^\d+(\.\d{1,2})?$/.test(s)) return null;
  const parts = s.split('.');
  const whole = parts[0].replace(/^0+(?=\d)/, '');
  if (whole.length > 5) return null;
  const cents = typedToCents(whole + '.' + (parts[1] || ''));
  return cents >= 1 && cents <= MAX_CENTS ? cents : null;
}

function centsToPlain(cents) {
  const whole = Math.floor(cents / 100);
  return whole + '.' + pad2(cents % 100);
}

// One keypad rule set, shared by the keypad and the Edit sheet amount field.
// Returns the new string, or null when the keystroke is refused.
function applyKey(str, key) {
  if (key === '.') {
    if (str.indexOf('.') !== -1) return null;
    return str === '' ? '0.' : str + '.';
  }
  if (!/^\d$/.test(key)) return null;
  const dot = str.indexOf('.');
  if (dot !== -1) return str.length - dot - 1 >= 2 ? null : str + key;
  if (str === '' || str === '0') return key;
  return str.length >= 5 ? null : str + key;
}

function sanitizeAmountText(raw) {
  let text = String(raw);
  text = text.indexOf('.') !== -1 ? text.replace(/,/g, '') : text.replace(/,/g, '.');
  let out = '';
  for (const ch of text) {
    const next = applyKey(out, ch);
    if (next !== null) out = next;
  }
  return out;
}

function fmtTyped(str) {
  if (str === '') return '$0';
  const parts = str.split('.');
  let out = '$' + intFmt.format(parseInt(parts[0], 10));
  if (parts.length > 1) out += '.' + parts[1];
  return out;
}

/* =====================================================================
   6. Storage (every call wrapped; memory fallback)
   ===================================================================== */
const store = { mode: 'ok', corrupt: null, persistAsked: false };

function storageHandle() { return window.localStorage; }

function storageProbe() {
  try {
    const ls = storageHandle();
    const key = STORAGE_KEY + '.probe';
    ls.setItem(key, '1');
    const ok = ls.getItem(key) === '1';
    ls.removeItem(key);
    return ok;
  } catch (e) { return false; }
}

function storageRead(key) {
  try { return storageHandle().getItem(key); } catch (e) { return null; }
}

function keepCorruptCopy(raw) {
  try { storageHandle().setItem(STORAGE_KEY + '.corrupt.' + Date.now(), raw); return true; } catch (e) { return false; }
}

// "Delete all" means all: unreadable copies and the old v1 key go too.
function removeLeftovers() {
  try {
    const ls = storageHandle();
    const doomed = [];
    for (let i = 0; i < ls.length; i++) {
      const k = ls.key(i);
      if (k && (k.indexOf(STORAGE_KEY + '.corrupt.') === 0 || k.indexOf(LEGACY_KEY) === 0)) doomed.push(k);
    }
    doomed.forEach((k) => ls.removeItem(k));
  } catch (e) { /* nothing to do */ }
}

function askPersistence() {
  if (store.persistAsked) return;
  store.persistAsked = true;
  try {
    const p = navigator.storage?.persist?.();
    if (p && typeof p.catch === 'function') p.catch(() => {});
  } catch (e) { /* ignored on purpose */ }
}

function saveState() {
  if (store.mode !== 'ok') return;
  try {
    storageHandle().setItem(STORAGE_KEY, JSON.stringify(state));
    askPersistence();
  } catch (e) {
    store.mode = 'memory';
    renderBanners();
  }
}

/* =====================================================================
   7. Model
   ===================================================================== */
let state;

function defaultCategories() {
  return DEFAULT_CATEGORIES.map((c, i) => ({
    id: c[0], emoji: c[1], name: c[2], taxTag: c[3], hidden: false, builtIn: true, order: i + 1
  }));
}

function defaultSettings() {
  return {
    lastPayment: { methodId: DEFAULT_PAYMENT, cardId: null },
    testNoticeDismissed: false,
    autoLocation: false,
    mapsNoticeShown: false,
    onboarded: false
  };
}

function defaultState() {
  return { schemaVersion: SCHEMA_VERSION, expenses: [], categories: defaultCategories(), cards: [], settings: defaultSettings() };
}

// MIGRATIONS[n] upgrades a version n state to version n + 1. Nothing is dropped.
const MIGRATIONS = {
  1: (old) => {
    const s = old.settings && typeof old.settings === 'object' ? old.settings : {};
    const expenses = Array.isArray(old.expenses) ? old.expenses : [];
    return {
      schemaVersion: 2,
      expenses: expenses.map((e) => (e && typeof e === 'object' ? Object.assign({}, e, { cardId: null, location: null }) : e)),
      categories: old.categories,
      cards: [],
      settings: {
        lastPayment: { methodId: s.lastPaymentMethodId, cardId: null },
        testNoticeDismissed: s.testNoticeDismissed === true,
        autoLocation: false,
        mapsNoticeShown: false,
        onboarded: expenses.length > 0
      }
    };
  }
};

function migrate(raw) {
  let data = raw;
  let version = Number.isInteger(data.schemaVersion) ? data.schemaVersion : 1;
  while (version < SCHEMA_VERSION) {
    if (typeof MIGRATIONS[version] !== 'function') return null;
    data = MIGRATIONS[version](data);
    version += 1;
  }
  return version === SCHEMA_VERSION ? data : null;
}

const isPaymentId = (id) => PAYMENT_METHODS.some((p) => p.id === id);
const str = (v, max) => (typeof v === 'string' ? v.slice(0, max) : '');
const round5 = (n) => Math.round(n * 1e5) / 1e5;
const isLast4 = (v) => typeof v === 'string' && /^\d{4}$/.test(v);

function cleanCategories(list) {
  const cats = defaultCategories();
  const byId = new Map(cats.map((c) => [c.id, c]));
  let order = cats.length;
  (Array.isArray(list) ? list : []).forEach((raw) => {
    if (!raw || typeof raw.id !== 'string' || typeof raw.name !== 'string' || !raw.name.trim()) return;
    const tag = TAX_TAGS.indexOf(raw.taxTag) !== -1 ? raw.taxTag : null;
    const emoji = typeof raw.emoji === 'string' && raw.emoji ? raw.emoji : DEFAULT_EMOJI;
    const known = byId.get(raw.id);
    if (known) {
      known.name = raw.name; known.emoji = emoji; known.taxTag = tag; known.hidden = raw.hidden === true;
    } else {
      order += 1;
      const cat = { id: raw.id, name: raw.name, emoji, taxTag: tag, hidden: raw.hidden === true, builtIn: false, order };
      cats.push(cat);
      byId.set(cat.id, cat);
    }
  });
  return cats;
}

function cleanCards(list) {
  const seen = new Set();
  const out = [];
  (Array.isArray(list) ? list : []).forEach((raw) => {
    if (!raw || typeof raw.id !== 'string' || !raw.id || seen.has(raw.id)) return;
    if (typeof raw.name !== 'string' || !raw.name.trim()) return;
    seen.add(raw.id);
    out.push({
      id: raw.id,
      catalogueId: typeof raw.catalogueId === 'string' && raw.catalogueId ? raw.catalogueId : null,
      issuer: str(raw.issuer, 60),
      name: raw.name.slice(0, 80),
      kind: CARD_KINDS.indexOf(raw.kind) !== -1 ? raw.kind : 'credit',
      networks: (Array.isArray(raw.networks) ? raw.networks : []).filter((n) => CARD_NETWORKS.indexOf(n) !== -1),
      nickname: str(raw.nickname, 24),
      last4: isLast4(raw.last4) ? raw.last4 : '',
      colour: CARD_COLOURS.indexOf(raw.colour) !== -1 ? raw.colour : CARD_COLOURS[0],
      archived: raw.archived === true,
      createdAt: typeof raw.createdAt === 'string' ? raw.createdAt : nowIso()
    });
  });
  return out;
}

// Returns a tidy location or null. Out-of-range or non-numeric values are dropped.
function cleanLocation(raw, fallbackStamp) {
  if (!raw || typeof raw !== 'object') return null;
  const lat = raw.lat, lng = raw.lng;
  if (typeof lat !== 'number' || typeof lng !== 'number' || !Number.isFinite(lat) || !Number.isFinite(lng)) return null;
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) return null;
  const acc = raw.accuracyM;
  return {
    lat: round5(lat),
    lng: round5(lng),
    accuracyM: typeof acc === 'number' && Number.isFinite(acc) && acc >= 0 ? Math.round(acc) : null,
    capturedAt: typeof raw.capturedAt === 'string' ? raw.capturedAt : (fallbackStamp || nowIso())
  };
}

function cleanExpenses(list, cats, cards) {
  const ids = new Set(cats.map((c) => c.id));
  const cardIds = new Set(cards.map((c) => c.id));
  const seen = new Set();
  const out = [];
  (Array.isArray(list) ? list : []).forEach((raw) => {
    if (!raw || typeof raw.id !== 'string' || !raw.id || seen.has(raw.id)) return;
    if (!Number.isInteger(raw.amountCents) || raw.amountCents < 1 || raw.amountCents > MAX_CENTS) return;
    if (!isValidYmd(raw.date)) return;
    seen.add(raw.id);
    const created = typeof raw.createdAt === 'string' ? raw.createdAt : nowIso();
    out.push({
      id: raw.id,
      amountCents: raw.amountCents,
      date: raw.date,
      categoryId: ids.has(raw.categoryId) ? raw.categoryId : 'other',
      paymentMethodId: isPaymentId(raw.paymentMethodId) ? raw.paymentMethodId : 'other',
      cardId: typeof raw.cardId === 'string' && cardIds.has(raw.cardId) ? raw.cardId : null,
      merchant: str(raw.merchant, 60),
      note: str(raw.note, 200),
      location: cleanLocation(raw.location, created),
      createdAt: created,
      updatedAt: typeof raw.updatedAt === 'string' ? raw.updatedAt : created
    });
  });
  return out;
}

function validateState(raw) {
  const fresh = defaultSettings();
  const categories = cleanCategories(raw.categories);
  const cards = cleanCards(raw.cards);
  const s = raw.settings && typeof raw.settings === 'object' ? raw.settings : {};
  const lp = s.lastPayment && typeof s.lastPayment === 'object' ? s.lastPayment : {};
  return {
    schemaVersion: SCHEMA_VERSION,
    expenses: cleanExpenses(raw.expenses, categories, cards),
    categories,
    cards,
    settings: {
      lastPayment: {
        methodId: isPaymentId(lp.methodId) ? lp.methodId : fresh.lastPayment.methodId,
        cardId: typeof lp.cardId === 'string' && cards.some((c) => c.id === lp.cardId) ? lp.cardId : null
      },
      testNoticeDismissed: s.testNoticeDismissed === true,
      autoLocation: s.autoLocation === true,
      mapsNoticeShown: s.mapsNoticeShown === true,
      onboarded: s.onboarded === true
    }
  };
}

function loadState() {
  store.mode = storageProbe() ? 'ok' : 'memory';
  if (store.mode !== 'ok') { if (!state) state = defaultState(); return; }
  let raw = storageRead(STORAGE_KEY);
  let fromLegacy = false;
  if (raw === null) {
    raw = storageRead(LEGACY_KEY);      // first run after the v1 test page: carry the data over
    fromLegacy = raw !== null;
  }
  if (raw === null) { state = defaultState(); return; }
  let parsed = null;
  try {
    const data = JSON.parse(raw);
    if (data && typeof data === 'object' && !Array.isArray(data)) parsed = migrate(data);
  } catch (e) { parsed = null; }
  if (!parsed) {
    store.corrupt = keepCorruptCopy(raw) ? 'kept' : 'lost';
    state = defaultState();
    saveState();
    return;
  }
  state = validateState(parsed);
  if (fromLegacy) saveState();          // the old key is left untouched as a safety copy
}

const catById = (id) => state.categories.find((c) => c.id === id) ||
  { id, name: 'Other', emoji: DEFAULT_EMOJI, taxTag: null, hidden: true, builtIn: false, order: 9999 };
const payById = (id) => PAYMENT_METHODS.find((p) => p.id === id) || PAYMENT_METHODS[PAYMENT_METHODS.length - 1];
const sumCents = (list) => list.reduce((total, e) => total + e.amountCents, 0);
const expensesInMonth = (m) => { const p = monthPrefix(m); return state.expenses.filter((e) => e.date.slice(0, 7) === p); };
const byOrder = (a, b) => a.order - b.order;
const newestFirst = (a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0) ||
  (a.createdAt < b.createdAt ? 1 : a.createdAt > b.createdAt ? -1 : 0);

function addExpense(fields) {
  const now = nowIso();
  const expense = Object.assign({ id: newId(), cardId: null, location: null, createdAt: now, updatedAt: now }, fields);
  state.expenses.push(expense);
  saveState();
  return expense;
}

function updateExpense(id, fields) {
  const expense = state.expenses.find((e) => e.id === id);
  if (!expense) return;
  Object.assign(expense, fields, { updatedAt: nowIso() });
  saveState();
}

function deleteExpense(id) {
  state.expenses = state.expenses.filter((e) => e.id !== id);
  saveState();
}

// Puts a deleted expense back (Undo). Does nothing if it is somehow already there.
function restoreExpense(expense) {
  if (state.expenses.some((e) => e.id === expense.id)) return;
  state.expenses.push(expense);
  saveState();
}

// Seven most used visible categories over the last 90 days; ties keep default order.
function rankTopCategories() {
  const since = daysAgoStr(90);
  const counts = new Map();
  state.expenses.forEach((e) => { if (e.date >= since) counts.set(e.categoryId, (counts.get(e.categoryId) || 0) + 1); });
  return state.categories
    .filter((c) => !c.hidden)
    .sort((a, b) => (counts.get(b.id) || 0) - (counts.get(a.id) || 0) || a.order - b.order)
    .slice(0, 7);
}

function visibleCategoriesAlpha() {
  return state.categories.filter((c) => !c.hidden)
    .sort((a, b) => a.name.localeCompare(b.name, 'en', { sensitivity: 'base' }));
}

// Up to five earlier merchants: prefix matches, then contains matches, each by use count.
function merchantSuggestions(query) {
  const q = query.trim().toLowerCase();
  const seen = new Map();
  state.expenses.forEach((e) => {
    if (!e.merchant) return;
    const key = e.merchant.toLowerCase();
    const item = seen.get(key) || { key, name: e.merchant, count: 0 };
    item.count += 1;
    seen.set(key, item);
  });
  const rank = (a, b) => b.count - a.count || a.name.localeCompare(b.name, 'en');
  const all = Array.from(seen.values()).filter((m) => m.key !== q);
  const prefix = all.filter((m) => m.key.indexOf(q) === 0).sort(rank);
  const contains = all.filter((m) => m.key.indexOf(q) > 0).sort(rank);
  return prefix.concat(contains).slice(0, 5).map((m) => m.name);
}

// The category a merchant was most often filed under; ties go to the most recent use.
// Returns null for an unknown merchant or when that category is hidden.
function usualCategoryFor(merchant) {
  const key = fold(merchant.trim());
  if (!key) return null;
  const stats = new Map();
  state.expenses.forEach((e) => {
    if (!e.merchant || fold(e.merchant.trim()) !== key) return;
    const s = stats.get(e.categoryId) || { id: e.categoryId, count: 0, last: '' };
    s.count += 1;
    const stamp = e.date + ' ' + e.createdAt;
    if (stamp > s.last) s.last = stamp;
    stats.set(e.categoryId, s);
  });
  const best = Array.from(stats.values()).sort((a, b) => b.count - a.count || (a.last < b.last ? 1 : a.last > b.last ? -1 : 0))[0];
  if (!best) return null;
  const cat = state.categories.find((c) => c.id === best.id);
  return cat && !cat.hidden ? cat : null;
}

// The most recent expenses, one per distinct amount + category + merchant + card.
function recentDistinct(limit) {
  const seen = new Set();
  const out = [];
  const sorted = state.expenses.slice().sort((a, b) =>
    (a.createdAt < b.createdAt ? 1 : a.createdAt > b.createdAt ? -1 : 0) || newestFirst(a, b));
  for (const e of sorted) {
    const key = [e.amountCents, e.categoryId, fold(e.merchant.trim()), e.cardId || ''].join('|');
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(e);
    if (out.length >= limit) break;
  }
  return out;
}

function taxTotalsForYear(year) {
  const totals = { medical: 0, donation: 0, childcare: 0 };
  const tagOf = new Map(state.categories.map((c) => [c.id, c.taxTag]));
  state.expenses.forEach((e) => {
    const tag = tagOf.get(e.categoryId);
    if (tag && e.date.slice(0, 4) === String(year)) totals[tag] += e.amountCents;
  });
  return totals;
}

/* ----- Cards and payment choices ----- */
const cardById = (id) => (id ? state.cards.find((c) => c.id === id) || null : null);
const cardDisplayName = (card) => card.nickname || card.name;
const cardShortLabel = (card) => cardDisplayName(card) + (card.last4 ? ' ••' + card.last4 : '');

function cardUseCounts() {
  const counts = new Map();
  state.expenses.forEach((e) => { if (e.cardId) counts.set(e.cardId, (counts.get(e.cardId) || 0) + 1); });
  return counts;
}

// Cards in pickers and lists: not archived, most used first, then oldest first.
function activeCards() {
  const counts = cardUseCounts();
  return state.cards.filter((c) => !c.archived)
    .sort((a, b) => (counts.get(b.id) || 0) - (counts.get(a.id) || 0) || (a.createdAt < b.createdAt ? -1 : a.createdAt > b.createdAt ? 1 : 0));
}
const archivedCards = () => state.cards.filter((c) => c.archived);

function methodLabel(id) {
  const method = payById(id);
  return method.other && activeCards().length ? method.other : method.label;
}

function paymentLabel(methodId, cardId) {
  const card = cardById(cardId);
  return card ? cardShortLabel(card) : methodLabel(methodId);
}

// A payment choice travels through form controls as "card:<id>" or "m:<method id>".
const payValue = (methodId, cardId) => (cardId ? 'card:' + cardId : 'm:' + methodId);
function parsePayValue(value) {
  const v = String(value || '');
  if (v.indexOf('card:') === 0) {
    const card = cardById(v.slice(5));
    if (card) return { methodId: card.kind, cardId: card.id };
  }
  const id = v.indexOf('m:') === 0 ? v.slice(2) : '';
  return { methodId: isPaymentId(id) ? id : 'other', cardId: null };
}

// The last choice sticks. If that card was archived or removed, fall back to its method.
function defaultPayment() {
  const lp = state.settings.lastPayment;
  const card = cardById(lp.cardId);
  if (card && !card.archived) return { methodId: card.kind, cardId: card.id };
  return { methodId: lp.methodId, cardId: null };
}

function nextCardColour() {
  const used = new Set(state.cards.map((c) => c.colour));
  return CARD_COLOURS.find((c) => !used.has(c)) || CARD_COLOURS[state.cards.length % CARD_COLOURS.length];
}

function createCard(fields) {
  const card = Object.assign({
    id: 'k_' + newId(), catalogueId: null, issuer: '', name: '', kind: 'credit', networks: [],
    nickname: '', last4: '', colour: nextCardColour(), archived: false, createdAt: nowIso()
  }, fields);
  state.cards.push(card);
  return card;
}

// Archives a card that expenses still point at; deletes one that nothing uses.
function removeCard(id) {
  const card = cardById(id);
  if (!card) return null;
  if (state.expenses.some((e) => e.cardId === id)) {
    card.archived = true;
    saveState();
    return 'archived';
  }
  state.cards = state.cards.filter((c) => c.id !== id);
  if (state.settings.lastPayment.cardId === id) state.settings.lastPayment.cardId = null;
  saveState();
  return 'deleted';
}

/* ----- History filters ----- */
function emptyFilters() { return { text: '', cats: [], card: null, hasLocation: false, day: null, month: null }; }

function filtersActive(f) {
  return !!(f.text.trim() || f.cats.length || f.card !== null || f.hasLocation || f.day || f.month);
}

function filterExpenses(f) {
  const q = fold(f.text.trim());
  const cats = new Set(f.cats);
  const month = f.month ? monthPrefix(f.month) : null;
  return state.expenses.filter((e) => {
    if (q && fold(e.merchant + ' ' + e.note).indexOf(q) === -1) return false;
    if (cats.size && !cats.has(e.categoryId)) return false;
    if (f.card !== null && (f.card === NO_CARD ? !!e.cardId : e.cardId !== f.card)) return false;
    if (f.hasLocation && !e.location) return false;
    if (f.day && e.date !== f.day) return false;
    if (month && e.date.slice(0, 7) !== month) return false;
    return true;
  });
}

/* =====================================================================
   8. CSV (export and restore)
   ===================================================================== */
function csvField(value) {
  const v = String(value);
  return /[",\r\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
}
const formulaSafe = (v) => (/^[=+\-@]/.test(v) ? "'" + v : v);
const formulaUnsafe = (v) => (/^'[=+\-@]/.test(v) ? v.slice(1) : v);

function buildCsv() {
  const rows = state.expenses.slice().sort((a, b) =>
    (a.date < b.date ? -1 : a.date > b.date ? 1 : 0) || (a.createdAt < b.createdAt ? -1 : a.createdAt > b.createdAt ? 1 : 0));
  const lines = [CSV_HEADER.join(',')];
  rows.forEach((e) => {
    const cat = catById(e.categoryId);
    const card = cardById(e.cardId);
    const loc = e.location;
    lines.push([
      e.id, e.date, centsToPlain(e.amountCents), formulaSafe(cat.name), payById(e.paymentMethodId).label,
      card ? formulaSafe(cardDisplayName(card)) : '', card ? card.last4 : '',
      formulaSafe(e.merchant), formulaSafe(e.note), cat.taxTag || '',
      loc ? loc.lat.toFixed(5) : '', loc ? loc.lng.toFixed(5) : '', loc && loc.accuracyM !== null ? String(loc.accuracyM) : '',
      e.createdAt, e.updatedAt
    ].map(csvField).join(','));
  });
  return lines.join('\r\n') + '\r\n';
}

// RFC 4180 reader: CRLF or LF, quoted fields with commas, quotes and newlines.
function parseCsv(text) {
  let src = String(text);
  if (src.charCodeAt(0) === 0xFEFF) src = src.slice(1);
  const rows = [];
  let row = [], field = '', quoted = false, i = 0;
  const endField = () => { row.push(field); field = ''; };
  const endRow = () => { endField(); rows.push(row); row = []; };
  while (i < src.length) {
    const ch = src[i];
    if (quoted) {
      if (ch === '"') {
        if (src[i + 1] === '"') { field += '"'; i += 2; continue; }
        quoted = false; i += 1; continue;
      }
      field += ch; i += 1; continue;
    }
    if (ch === '"' && field === '') { quoted = true; i += 1; continue; }
    if (ch === ',') { endField(); i += 1; continue; }
    if (ch === '\r' || ch === '\n') {
      endRow();
      i += (ch === '\r' && src[i + 1] === '\n') ? 2 : 1;
      continue;
    }
    field += ch; i += 1;
  }
  if (field !== '' || row.length) endRow();
  return rows.filter((r) => !(r.length === 1 && r[0].trim() === ''));
}

function findCategoryByName(name) {
  const key = name.toLowerCase();
  return state.categories.find((c) => c.name.trim().toLowerCase() === key);
}

function createCategory(name, emoji, taxTag) {
  const order = state.categories.reduce((max, c) => Math.max(max, c.order), 0) + 1;
  const cat = { id: 'c_' + newId(), name, emoji, taxTag, hidden: false, builtIn: false, order };
  state.categories.push(cat);
  return cat;
}

function paymentFromText(text) {
  const key = text.trim().toLowerCase();
  if (PAYMENT_ALIASES[key]) return PAYMENT_ALIASES[key];
  const hit = PAYMENT_METHODS.find((p) => p.id === key || p.label.toLowerCase() === key || (p.other && p.other.toLowerCase() === key));
  return hit ? hit.id : 'other';
}

// Name plus last 4 digits against every card the user has, archived ones included.
function findCardByNameAndLast4(name, last4) {
  const key = name.toLowerCase();
  return state.cards.find((c) =>
    (cardDisplayName(c).trim().toLowerCase() === key || c.name.trim().toLowerCase() === key) && c.last4 === last4);
}

// Strict decimal number from CSV text, or null.
function parseCoordinate(text, limit) {
  const s = text.trim();
  if (!/^-?\d{1,3}(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  return Number.isFinite(n) && n >= -limit && n <= limit ? n : null;
}

function locationFromCsv(latText, lngText, accText, stamp) {
  const lat = parseCoordinate(latText, 90), lng = parseCoordinate(lngText, 180);
  if (lat === null || lng === null) return null;      // an invalid location is ignored, the row is kept
  const acc = /^\d{1,7}$/.test(accText.trim()) ? parseInt(accText.trim(), 10) : null;
  return cleanLocation({ lat, lng, accuracyM: acc, capturedAt: stamp }, stamp);
}

const isoOrNull = (text) => (text && !Number.isNaN(Date.parse(text)) ? text : null);

// Merges a backup (v1 or v2 columns) into the current state. Never overwrites an existing expense.
function restoreCsv(text) {
  const rows = parseCsv(text);
  if (!rows.length) return { ok: false };
  const header = rows[0].map((h) => h.trim().toLowerCase());
  const col = {};
  CSV_HEADER.forEach((name) => { col[name] = header.indexOf(name); });
  if (col.date < 0 || col.amount < 0 || col.category < 0) return { ok: false };
  const cell = (r, name) => (col[name] >= 0 && r[col[name]] !== undefined ? r[col[name]] : '');
  const ids = new Set(state.expenses.map((e) => e.id));
  const result = { ok: true, restored: 0, already: 0, invalid: 0, newCategories: 0, newCards: 0 };

  rows.slice(1).forEach((r) => {
    const date = cell(r, 'date').trim();
    const cents = parseAmountStrict(cell(r, 'amount'));
    const catName = formulaUnsafe(cell(r, 'category').trim()).trim();
    if (!isValidYmd(date) || cents === null || !catName) { result.invalid += 1; return; }
    const id = cell(r, 'id').trim() || newId();
    if (ids.has(id)) { result.already += 1; return; }
    let cat = findCategoryByName(catName);
    if (!cat) {
      const tag = cell(r, 'tax_tag').trim().toLowerCase();
      cat = createCategory(catName, DEFAULT_EMOJI, TAX_TAGS.indexOf(tag) !== -1 ? tag : null);
      result.newCategories += 1;
    }
    let methodId = paymentFromText(cell(r, 'payment_method'));
    const cardName = formulaUnsafe(cell(r, 'card').trim()).trim();
    let card = null;
    if (cardName) {
      const last4 = cell(r, 'card_last4').trim();
      const tail = isLast4(last4) ? last4 : '';
      card = findCardByNameAndLast4(cardName, tail);
      if (!card) {
        card = createCard({ name: cardName.slice(0, 80), kind: CARD_KINDS.indexOf(methodId) !== -1 ? methodId : 'credit', last4: tail });
        result.newCards += 1;
      }
      if (CARD_KINDS.indexOf(methodId) === -1) methodId = card.kind;
    }
    const created = isoOrNull(cell(r, 'created_at').trim()) || nowIso();
    state.expenses.push({
      id,
      amountCents: cents,
      date,
      categoryId: cat.id,
      paymentMethodId: methodId,
      cardId: card ? card.id : null,
      merchant: formulaUnsafe(cell(r, 'merchant')).slice(0, 60),
      note: formulaUnsafe(cell(r, 'note')).slice(0, 200),
      location: locationFromCsv(cell(r, 'latitude'), cell(r, 'longitude'), cell(r, 'location_accuracy_m'), created),
      createdAt: created,
      updatedAt: isoOrNull(cell(r, 'updated_at').trim()) || created
    });
    ids.add(id);
    result.restored += 1;
  });
  saveState();
  return result;
}

function backupFilename() { return `daily-spend-${todayStr()}.csv`; }

/* =====================================================================
   9. UI state
   ===================================================================== */
const ui = {
  tab: 'add',
  amount: '',                 // typed amount string, e.g. "12.3"
  draft: null,                // see resetDraft()
  capture: null,              // location request in flight for the draft
  locError: '',               // last location error shown in the Details sheet
  locRefresh: null,           // set by an open sheet that shows the draft's location
  month: currentMonth(),      // shared by History and Summary
  filters: emptyFilters(),    // History search and filters
  corruptDismissed: false,
  downloads: null,            // platform capability when embedded
  canDownload: false,
  drawCharts: false,          // play the chart draw animation on the next Summary render
  chipIds: []                 // frozen chip order, see refreshChips()
};

// The chip line-up is frozen for the session so chips never move under the thumb.
// It is ranked at launch and again only when the category list itself changes.
function refreshChips() { ui.chipIds = rankTopCategories().map((c) => c.id); }
function topCategories() {
  return ui.chipIds.map((id) => state.categories.find((c) => c.id === id)).filter((c) => c && !c.hidden);
}

function resetDraft() {
  if (ui.capture) ui.capture.target = null;      // a fix still on its way is no longer wanted
  ui.capture = null;
  ui.locError = '';
  ui.amount = '';
  const pay = defaultPayment();
  // date: null means today
  ui.draft = { date: null, paymentMethodId: pay.methodId, cardId: pay.cardId, merchant: '', note: '', location: null };
}
const draftDate = () => ui.draft.date || todayStr();

const el = {
  app: $('#app'), title: $('#title'), banners: $('#banners'), view: $('#view'),
  tabbar: $('#tabbar'), sheetRoot: $('#sheet-root'), toast: $('#toast-region')
};

/* =====================================================================
   10. Toast
   ===================================================================== */
let toastTimer = null;

function hideToast() {
  clearTimeout(toastTimer);
  el.toast.textContent = '';
}

// options: { ms, onUndo, check }  (check draws a short tick, used for saves)
function showToast(text, options) {
  const opts = options || {};
  hideToast();
  const box = document.createElement('div');
  box.className = 'toast';
  if (opts.check) box.insertAdjacentHTML('beforeend', ICONS.check);
  const span = document.createElement('span');
  span.className = 'toast-text';
  span.textContent = text;
  box.appendChild(span);
  if (opts.onUndo) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'toast-undo';
    btn.textContent = STRINGS.undo;
    btn.addEventListener('click', () => { hideToast(); opts.onUndo(); });
    box.appendChild(btn);
  }
  el.toast.appendChild(box);
  toastTimer = setTimeout(hideToast, opts.ms || 3000);
}
const undoToastShowing = () => !!$('.toast-undo', el.toast);

/* =====================================================================
   11. Sheets (in-page dialogs; no browser dialogs anywhere)
   ===================================================================== */
const sheet = { node: null, opener: null, dismissible: true, onClose: null };

// Keyboard avoidance: while a sheet is open, track how much of the layout viewport the
// on-screen keyboard covers and expose it as --kb-overlap (0px when there is no keyboard).
function setKeyboardOverlap(px) {
  document.documentElement.style.setProperty('--kb-overlap', Math.round(px) + 'px');
}
function measureKeyboard() {
  const vv = window.visualViewport;
  if (!vv) return;
  setKeyboardOverlap(Math.max(0, window.innerHeight - (vv.height + vv.offsetTop)));
}
function revealFocusedField(e) {
  const field = e.target;
  if (!field || !/^(INPUT|TEXTAREA)$/.test(field.tagName) || /^(radio|checkbox|file)$/.test(field.type)) return;
  setTimeout(() => {
    if (sheet.node && sheet.node.contains(field) && document.activeElement === field) {
      try { field.scrollIntoView({ block: 'nearest' }); } catch (err) { /* ignore */ }
    }
  }, 300);
}
let keyboardWatch = false;
function watchKeyboard(on) {
  if (on === keyboardWatch) return;
  keyboardWatch = on;
  const vv = window.visualViewport;
  const method = on ? 'addEventListener' : 'removeEventListener';
  if (vv) { vv[method]('resize', measureKeyboard); vv[method]('scroll', measureKeyboard); }
  el.sheetRoot[method]('focusin', revealFocusedField);
  if (on) measureKeyboard(); else setKeyboardOverlap(0);
}

// options: { dismissible, onClose }. Opening a sheet over another replaces it without
// running the first sheet's onClose.
function openSheet(title, bodyHtml, options) {
  const opts = options || {};
  const opener = sheet.node ? sheet.opener : document.activeElement;
  el.sheetRoot.innerHTML =
    `<div class="backdrop" data-sheet-backdrop></div>
     <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-title" tabindex="-1">
       <div class="sheet-head">
         <h2 id="sheet-title">${esc(title)}</h2>
         <button type="button" class="icon-btn" data-sheet-close aria-label="${esc(STRINGS.close)}">×</button>
       </div>
       <div class="sheet-body">${bodyHtml}</div>
     </div>`;
  el.sheetRoot.hidden = false;
  sheet.node = $('.sheet', el.sheetRoot);
  sheet.opener = opener;
  sheet.dismissible = opts.dismissible !== false;
  sheet.onClose = typeof opts.onClose === 'function' ? opts.onClose : null;
  ui.locRefresh = null;
  el.app.inert = true;
  el.app.setAttribute('aria-hidden', 'true');
  watchKeyboard(true);
  sheet.node.focus({ preventScroll: true });
  return sheet.node;
}

function closeSheet() {
  if (!sheet.node) return;
  const opener = sheet.opener;
  const onClose = sheet.onClose;
  sheet.node = null;
  sheet.opener = null;
  sheet.onClose = null;
  ui.locRefresh = null;
  el.sheetRoot.hidden = true;
  el.sheetRoot.innerHTML = '';
  watchKeyboard(false);
  el.app.inert = false;
  el.app.removeAttribute('aria-hidden');
  if (opener && document.contains(opener) && typeof opener.focus === 'function') {
    try { opener.focus({ preventScroll: true }); } catch (e) { /* ignore */ }
  }
  if (onClose) onClose();
}

el.sheetRoot.addEventListener('click', (e) => {
  if (e.target.closest('[data-sheet-close]')) { closeSheet(); return; }
  if (e.target.closest('[data-sheet-backdrop]') && sheet.dismissible) closeSheet();
});

function focusables(root) {
  return $$('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])', root)
    .filter((n) => !n.disabled && n.offsetParent !== null);
}

function trapFocus(e) {
  const items = focusables(sheet.node);
  if (!items.length) { e.preventDefault(); return; }
  const first = items[0], last = items[items.length - 1], active = document.activeElement;
  if (!sheet.node.contains(active) || active === sheet.node) {
    e.preventDefault(); (e.shiftKey ? last : first).focus();
  } else if (e.shiftKey && active === first) {
    e.preventDefault(); last.focus();
  } else if (!e.shiftKey && active === last) {
    e.preventDefault(); first.focus();
  }
}

/* =====================================================================
   12. Shell: banners, tab bar, render
   ===================================================================== */
const TABS = ['add', 'history', 'summary', 'profile'];
const sw = { reg: null, updateReady: false, reloading: false };   // service worker, see section 20

function renderBanners() {
  const parts = [];
  if (sw.updateReady) {
    parts.push(`<div class="banner" id="banner-update" role="status"><p>${esc(STRINGS.updateReady)}</p>
      <button type="button" class="btn small primary" data-act="update-reload">${esc(STRINGS.reload)}</button></div>`);
  }
  if (store.mode !== 'ok') {
    parts.push(`<div class="banner warn" id="banner-memory" role="status"><p>${esc(STRINGS.storageMemory)}</p></div>`);
  }
  if (store.corrupt && !ui.corruptDismissed) {
    parts.push(`<div class="banner warn" id="banner-corrupt" role="status"><p>${esc(store.corrupt === 'kept' ? STRINGS.corruptKept : STRINGS.corruptLost)}</p>
      <button type="button" class="icon-btn" data-act="dismiss-corrupt" aria-label="${esc(STRINGS.dismiss)}">×</button></div>`);
  }
  if (embedded && store.mode === 'ok' && !state.settings.testNoticeDismissed) {
    parts.push(`<div class="banner" id="banner-test"><p>${esc(STRINGS.testNotice)}</p>
      <button type="button" class="icon-btn" data-act="dismiss-test" aria-label="${esc(STRINGS.dismiss)}">×</button></div>`);
  }
  el.banners.innerHTML = parts.join('');
}

function renderTabbar() {
  el.tabbar.innerHTML = TABS.map((t) =>
    `<button type="button" class="tab" data-act="tab" data-tab="${t}"${ui.tab === t ? ' aria-current="page"' : ''}>
       ${ICONS[t]}<span>${esc(STRINGS.tabs[t])}</span></button>`).join('');
}

const VIEWS = {};

function render() {
  el.title.textContent = STRINGS.titles[ui.tab];
  renderBanners();
  renderTabbar();
  VIEWS[ui.tab]();
}

function switchTab(tab) {
  ui.tab = tab;
  ui.drawCharts = tab === 'summary';
  render();
  el.view.scrollTop = 0;
}

/* =====================================================================
   13. Location (a GPS pin kept on the device; no lookups of any kind)
   ===================================================================== */
const geo = { denied: false };       // once refused, automatic capture stops asking this session

function geoApi() {
  try {
    const api = navigator.geolocation;
    return api && typeof api.getCurrentPosition === 'function' ? api : null;
  } catch (e) { return null; }
}

// Always resolves: { ok: true, location } or { ok: false, reason: 'denied' | 'unavailable' }.
function requestPosition() {
  return new Promise((resolve) => {
    const api = geoApi();
    if (!api) { resolve({ ok: false, reason: 'unavailable' }); return; }
    try {
      api.getCurrentPosition(
        (pos) => {
          const c = pos && pos.coords;
          const location = c ? cleanLocation({ lat: c.latitude, lng: c.longitude, accuracyM: c.accuracy, capturedAt: nowIso() }) : null;
          geo.denied = false;
          resolve(location ? { ok: true, location } : { ok: false, reason: 'unavailable' });
        },
        (err) => {
          const denied = !!err && err.code === 1;
          if (denied) geo.denied = true;
          resolve({ ok: false, reason: denied ? 'denied' : 'unavailable' });
        },
        GEO_OPTIONS);
    } catch (e) { resolve({ ok: false, reason: 'unavailable' }); }
  });
}

const locErrorText = (reason) => (reason === 'denied' ? STRINGS.locDenied : STRINGS.locFailed);
const locAccuracy = (location) => (location.accuracyM !== null ? STRINGS.locAccuracy(location.accuracyM) : '');
const mapsHref = (location) => MAPS_URL + String(location.lat) + ',' + String(location.lng);

function attachLocation(expenseId, location) {
  const expense = state.expenses.find((e) => e.id === expenseId);
  if (!expense || expense.location) return;
  expense.location = location;
  saveState();
  if (ui.tab === 'history' && !sheet.node) renderHistoryBody();
}

function refreshDraftLocationUi() {
  const row = $('#details-row');
  if (row && ui.tab === 'add') row.innerHTML = detailsRowHtml();
  if (ui.locRefresh) ui.locRefresh();
}

// Starts a location request for the expense being entered. `manual` is a tap on the
// button; otherwise it is the automatic capture and failures stay quiet.
function startDraftCapture(manual) {
  if (ui.capture) return;
  if (!manual && geo.denied) return;
  const cap = { target: 'draft', expenseId: null, until: 0 };
  ui.capture = cap;
  ui.locError = '';
  refreshDraftLocationUi();
  requestPosition().then((res) => {
    const target = cap.target;
    if (ui.capture === cap) ui.capture = null;
    if (res.ok) {
      if (target === 'draft') ui.draft.location = res.location;
      else if (target === 'expense' && Date.now() <= cap.until) attachLocation(cap.expenseId, res.location);
    } else if (target === 'draft') {
      if (manual) {
        ui.locError = locErrorText(res.reason);
      } else if (res.reason === 'denied') {
        ui.locError = STRINGS.locDenied;
        if (!undoToastShowing()) showToast(STRINGS.locDenied, { ms: 4000 });
      }
    }
    if (target === 'draft') refreshDraftLocationUi();
  });
}

// Saving never waits. A request still running is pointed at the saved expense instead,
// and its fix is attached if it arrives within 30 seconds.
function handOffCapture(expenseId) {
  const cap = ui.capture;
  if (!cap || cap.target !== 'draft') return;
  cap.target = 'expense';
  cap.expenseId = expenseId;
  cap.until = Date.now() + LATE_FIX_MS;
  ui.capture = null;
}

// Fresh location for an expense that was logged in one tap (Again), when automatic location is on.
function captureForExpense(expenseId) {
  if (!state.settings.autoLocation || geo.denied) return;
  const until = Date.now() + LATE_FIX_MS;
  requestPosition().then((res) => { if (res.ok && Date.now() <= until) attachLocation(expenseId, res.location); });
}

function draftLocationHtml() {
  if (ui.draft.location) {
    return `<div class="loc-line"><span id="d-loc-status" role="status">${esc(STRINGS.locAdded(locAccuracy(ui.draft.location)))}</span>
      <button type="button" class="btn small" id="d-loc-remove">${esc(STRINGS.remove)}</button></div>`;
  }
  if (ui.capture) return `<div class="loc-line"><span id="d-loc-status" role="status">${esc(STRINGS.locFinding)}</span></div>`;
  return `<button type="button" class="btn block" id="d-loc-add">${esc(STRINGS.locAdd)}</button>
    ${ui.locError ? `<p class="error" id="d-loc-error" role="alert">${esc(ui.locError)}</p>` : ''}`;
}

/* =====================================================================
   14. View: Add
   ===================================================================== */
const KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '0', 'back'];

function chipHtml(cat, disabled) {
  return `<button type="button" class="chip" data-act="chip" data-cat="${esc(cat.id)}" aria-disabled="${disabled}"
    aria-label="${esc(STRINGS.chipLabel(cat.name))}">
    <span class="chip-emoji" aria-hidden="true">${esc(cat.emoji)}</span><span class="chip-name">${esc(cat.name)}</span></button>`;
}

function detailsRowHtml() {
  const d = ui.draft;
  const pin = d.location ? STRINGS.sep + STRINGS.pin : ui.capture ? STRINGS.sep + STRINGS.pinFinding : '';
  const main = dayLabel(draftDate()) + STRINGS.sep + paymentLabel(d.paymentMethodId, d.cardId) + pin;
  const sub = [d.merchant, d.note].filter(Boolean).join(STRINGS.sep) || STRINGS.addMerchantOrNote;
  return `<span class="details-text"><span class="details-main">${esc(main)}</span><span class="details-sub">${esc(sub)}</span></span>${ICONS.chev}`;
}

// "Usual: ☕ Dining & coffee" for a merchant seen before. Tapping it saves, like a chip.
function usualPillHtml(disabled) {
  const cat = usualCategoryFor(ui.draft.merchant);
  if (!cat) return '';
  return `<button type="button" class="usual-pill" id="usual-pill" data-act="usual" data-cat="${esc(cat.id)}" aria-disabled="${disabled}"
    aria-label="${esc(STRINGS.usualLabel(cat.name))}"><span>${esc(STRINGS.usual(cat.emoji, cat.name))}</span></button>`;
}
function refreshUsual() {
  const slot = $('#usual-slot');
  if (slot) slot.innerHTML = usualPillHtml(typedToCents(ui.amount) <= 0);
}

VIEWS.add = function renderAdd() {
  const disabled = typedToCents(ui.amount) <= 0;
  const chips = topCategories().map((c) => chipHtml(c, disabled)).join('') +
    `<button type="button" class="chip chip-more" data-act="chip-more" aria-disabled="${disabled}" aria-label="${esc(STRINGS.moreChipLabel)}">
       <span class="chip-emoji" aria-hidden="true">···</span><span class="chip-name">${esc(STRINGS.moreChip)}</span></button>`;
  const keys = KEYS.map((k) => {
    if (k === 'back') {
      return `<button type="button" class="key key-flat" data-key="back" aria-label="${esc(STRINGS.keyLabels.back)}">${ICONS.back}</button>`;
    }
    const label = k === '.' ? ` aria-label="${esc(STRINGS.keyLabels['.'])}"` : '';
    return `<button type="button" class="key" data-key="${k}"${label}>${k}</button>`;
  }).join('');
  const recent = state.expenses.length
    ? `<button type="button" class="recent-btn" id="btn-recent" data-act="recent" aria-label="${esc(STRINGS.recentLabel)}">${ICONS.recent}<span>${esc(STRINGS.recent)}</span></button>`
    : '';
  el.view.innerHTML =
    `<section class="add">
       <div class="amount-wrap">
         <div class="amount" id="amount"></div>
         <div class="amount-hint" id="amount-hint" role="status"></div>
       </div>
       <div class="details-line">
         <button type="button" class="details-row" id="details-row" data-act="details" aria-label="${esc(STRINGS.detailsRowLabel)}">${detailsRowHtml()}</button>
         ${recent}
       </div>
       <div id="usual-slot">${usualPillHtml(disabled)}</div>
       <div class="chips" id="chips">${chips}</div>
       <div class="keypad" id="keypad">${keys}</div>
     </section>`;
  updateAmount();
  bindBackspace($('[data-key="back"]', el.view));
};

function updateAmount() {
  const node = $('#amount');
  if (!node) return;
  const text = fmtTyped(ui.amount);
  const zero = typedToCents(ui.amount) <= 0;
  node.textContent = text;
  node.setAttribute('aria-label', STRINGS.amountLabel(text));
  node.classList.toggle('is-zero', zero);
  $$('#chips .chip, #usual-pill').forEach((chip) => chip.setAttribute('aria-disabled', String(zero)));
}

function shakeAmount() {
  const node = $('#amount');
  if (!node) return;
  node.classList.remove('shake');
  void node.offsetWidth;
  node.classList.add('shake');
}

let hintTimer = null;
function showAmountHint(text) {
  const node = $('#amount-hint');
  if (!node) return;
  node.textContent = text;
  clearTimeout(hintTimer);
  hintTimer = setTimeout(() => { const n = $('#amount-hint'); if (n) n.textContent = ''; }, 2200);
}

function pressKey(key) {
  if (key === 'back') {
    ui.amount = ui.amount.slice(0, -1);
  } else {
    const wasEmpty = ui.amount === '';
    const next = applyKey(ui.amount, key);
    if (next === null) { shakeAmount(); return; }
    ui.amount = next;
    // Automatic location starts with the first key of a new amount, so it has a head start on the save.
    if (wasEmpty && state.settings.autoLocation && !ui.draft.location) startDraftCapture(false);
  }
  updateAmount();
}

// Tap removes one character; holding for half a second clears the amount.
function bindBackspace(btn) {
  let timer = null, longPressed = false;
  const cancel = () => { clearTimeout(timer); timer = null; };
  btn.addEventListener('pointerdown', () => {
    longPressed = false;
    cancel();
    timer = setTimeout(() => { longPressed = true; ui.amount = ''; updateAmount(); }, 500);
  });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach((type) => btn.addEventListener(type, cancel));
  btn.addEventListener('contextmenu', (e) => e.preventDefault());
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (longPressed) { longPressed = false; return; }
    pressKey('back');
  });
}

function nudgeAmount() {
  shakeAmount();
  showAmountHint(STRINGS.enterAmountFirst);
}

// The standard "Saved" toast with Undo, shared by every way of logging an expense.
function announceSaved(expense) {
  const day = expense.date === todayStr() ? '' : dayLabel(expense.date);
  showToast(STRINGS.saved(fmtMoney(expense.amountCents), catById(expense.categoryId).name, day), {
    ms: 5000,
    check: true,
    onUndo: () => { deleteExpense(expense.id); render(); showToast(STRINGS.undone, { ms: 2000 }); }
  });
}

function saveDraftTo(categoryId) {
  const cents = typedToCents(ui.amount);
  if (cents <= 0) { nudgeAmount(); return; }
  const d = ui.draft;
  const expense = addExpense({
    amountCents: cents,
    date: draftDate(),
    categoryId,
    paymentMethodId: d.paymentMethodId,
    cardId: d.cardId,
    merchant: d.merchant.trim(),
    note: d.note.trim(),
    location: d.location
  });
  state.settings.lastPayment = { methodId: d.paymentMethodId, cardId: d.cardId };
  saveState();
  handOffCapture(expense.id);
  resetDraft();
  render();
  announceSaved(expense);
}

// Quick repeat: a copy dated today. The location is never copied.
function repeatExpense(id) {
  const src = state.expenses.find((e) => e.id === id);
  if (!src) return null;
  const expense = addExpense({
    amountCents: src.amountCents,
    date: todayStr(),
    categoryId: src.categoryId,
    paymentMethodId: src.paymentMethodId,
    cardId: cardById(src.cardId) ? src.cardId : null,
    merchant: src.merchant,
    note: src.note,
    location: null
  });
  captureForExpense(expense.id);
  render();
  announceSaved(expense);
  return expense;
}

function tagBadge(cat) {
  return cat.taxTag ? `<span class="badge">${esc(STRINGS.taxTags[cat.taxTag])}</span>` : '';
}

function openAllCategoriesSheet() {
  const rows = visibleCategoriesAlpha().map((c) =>
    `<button type="button" class="row" data-pick="${esc(c.id)}">
       <span class="row-emoji" aria-hidden="true">${esc(c.emoji)}</span>
       <span class="row-text"><span class="row-title">${esc(c.name)}</span></span>${tagBadge(c)}</button>`).join('');
  const node = openSheet(STRINGS.allCategoriesTitle, `<div class="sheet-list" id="all-categories">${rows}</div>`);
  node.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-pick]');
    if (!btn) return;
    closeSheet();
    saveDraftTo(btn.dataset.pick);
  });
}

function openRecentSheet() {
  const rows = recentDistinct(10).map((e) => {
    const cat = catById(e.categoryId);
    const title = fmtMoney(e.amountCents) + STRINGS.sep + cat.name;
    const sub = [e.merchant, paymentLabel(e.paymentMethodId, e.cardId)].filter(Boolean).join(STRINGS.sep);
    return `<div class="row recent-row" data-id="${esc(e.id)}">
       <span class="row-emoji" aria-hidden="true">${esc(cat.emoji)}</span>
       <span class="row-text"><span class="row-title">${esc(title)}</span><span class="row-sub">${esc(sub)}</span></span>
       <button type="button" class="btn small primary" data-again="${esc(e.id)}" aria-label="${esc(STRINGS.againLabel(title))}">${esc(STRINGS.again)}</button></div>`;
  }).join('');
  const node = openSheet(STRINGS.recentTitle,
    `<p class="help">${esc(STRINGS.recentHelp)}</p>
     <div class="sheet-list" id="recent-list">${rows || `<p class="empty">${esc(STRINGS.recentEmpty)}</p>`}</div>`);
  node.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-again]');
    if (!btn) return;
    closeSheet();
    repeatExpense(btn.dataset.again);
  });
}

// Payment picker for the Details sheet: the user's cards first, then the other ways to pay.
function paymentPickerHtml(name, selected) {
  const option = (value, label, colour) =>
    `<label class="option"><input type="radio" name="${name}" value="${esc(value)}"${value === selected ? ' checked' : ''}>
       <span>${colour ? `<i class="card-dot sw-${colour}" aria-hidden="true"></i>` : ''}${esc(label)}</span></label>`;
  const cards = activeCards();
  const others = PAYMENT_METHODS.map((p) => option(payValue(p.id, null), methodLabel(p.id), null)).join('');
  if (!cards.length) return `<div class="options" data-group="other">${others}</div>`;
  return `<p class="group-label">${esc(STRINGS.myCards)}</p>
    <div class="options" data-group="cards">${cards.map((c) => option(payValue(c.kind, c.id), cardShortLabel(c), c.colour)).join('')}</div>
    <p class="group-label">${esc(STRINGS.otherWays)}</p>
    <div class="options" data-group="other">${others}</div>`;
}

// Custom merchant suggestion list (a plain list of buttons, no native data list).
function bindSuggestions(input, box) {
  const show = () => {
    box.innerHTML = merchantSuggestions(input.value).map((name) =>
      `<button type="button" data-suggest="${esc(name)}">${esc(name)}</button>`).join('');
  };
  input.addEventListener('focus', show);
  input.addEventListener('input', show);
  box.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-suggest]');
    if (!btn) return;
    input.value = btn.dataset.suggest;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    box.innerHTML = '';
  });
}

function openDetailsSheet() {
  const d = ui.draft;
  const node = openSheet(STRINGS.detailsTitle,
    `<label class="field"><span class="label">${esc(STRINGS.date)}</span>
       <input class="input" type="date" id="d-date" value="${esc(draftDate())}"></label>
     <fieldset class="field"><legend>${esc(STRINGS.paymentMethod)}</legend>
       <div id="d-pay">${paymentPickerHtml('d-pay', payValue(d.paymentMethodId, d.cardId))}</div></fieldset>
     <label class="field"><span class="label">${esc(STRINGS.merchant)}</span>
       <input class="input" type="text" id="d-merchant" maxlength="60" autocomplete="off" autocapitalize="words"
         placeholder="${esc(STRINGS.merchantPlaceholder)}" value="${esc(d.merchant)}">
       <div class="suggest" id="d-suggest" aria-label="${esc(STRINGS.suggestionsLabel)}"></div></label>
     <label class="field"><span class="label">${esc(STRINGS.note)}</span>
       <input class="input" type="text" id="d-note" maxlength="200" autocomplete="off"
         placeholder="${esc(STRINGS.notePlaceholder)}" value="${esc(d.note)}"></label>
     <div class="field"><span class="label">${esc(STRINGS.location)}</span><div id="d-loc">${draftLocationHtml()}</div></div>
     <button type="button" class="btn primary block" id="d-done">${esc(STRINGS.done)}</button>`);
  const refreshRow = () => { const row = $('#details-row'); if (row) row.innerHTML = detailsRowHtml(); };
  $('#d-date', node).addEventListener('change', (e) => {
    const v = e.target.value;
    d.date = isValidYmd(v) && v !== todayStr() ? v : null;
    refreshRow();
  });
  $('#d-pay', node).addEventListener('change', (e) => {
    const choice = parsePayValue(e.target.value);
    d.paymentMethodId = choice.methodId;
    d.cardId = choice.cardId;
    refreshRow();
  });
  $('#d-merchant', node).addEventListener('input', (e) => { d.merchant = e.target.value; refreshRow(); refreshUsual(); });
  $('#d-note', node).addEventListener('input', (e) => { d.note = e.target.value; refreshRow(); });
  bindSuggestions($('#d-merchant', node), $('#d-suggest', node));
  const locBox = $('#d-loc', node);
  ui.locRefresh = () => {
    const hadFocus = locBox.contains(document.activeElement);
    locBox.innerHTML = draftLocationHtml();
    const next = $('button', locBox);
    if (hadFocus && next) next.focus({ preventScroll: true });
  };
  locBox.addEventListener('click', (e) => {
    if (e.target.closest('#d-loc-add')) startDraftCapture(true);
    else if (e.target.closest('#d-loc-remove')) { ui.draft.location = null; ui.locError = ''; refreshDraftLocationUi(); }
  });
  $('#d-done', node).addEventListener('click', closeSheet);
}

/* =====================================================================
   15. View: History (search, filters, swipe actions, edit)
   ===================================================================== */
function monthSwitchHtml() {
  return `<div class="month-switch">
    <button type="button" class="icon-btn" data-act="month" data-delta="-1" aria-label="${esc(STRINGS.prevMonth)}">‹</button>
    <span class="month-label" id="month-label" aria-live="polite">${esc(monthLabel(ui.month))}</span>
    <button type="button" class="icon-btn" data-act="month" data-delta="1" aria-label="${esc(STRINGS.nextMonth)}">›</button>
  </div>`;
}

// A row sits on top of its two swipe actions: Again (left edge) and Delete (right edge).
function historyRowHtml(e) {
  const cat = catById(e.categoryId);
  const card = cardById(e.cardId);
  const sub = [e.merchant, e.note].filter(Boolean).join(STRINGS.sep);
  const pay = card ? cardDisplayName(card) : payById(e.paymentMethodId).short;
  const pin = e.location ? `<span class="row-pin" role="img" aria-label="${esc(STRINGS.hasLocation)}">${esc(STRINGS.pin)}</span>` : '';
  return `<div class="swipe" data-id="${esc(e.id)}">
    <span class="swipe-bg swipe-again" aria-hidden="true">${esc(STRINGS.again)}</span>
    <button type="button" class="swipe-bg swipe-delete" data-act="swipe-delete" data-id="${esc(e.id)}" tabindex="-1" aria-hidden="true">${esc(STRINGS.del)}</button>
    <button type="button" class="row" data-act="edit" data-id="${esc(e.id)}">
      <span class="row-emoji" aria-hidden="true">${esc(cat.emoji)}</span>
      <span class="row-text"><span class="row-title">${esc(cat.name)}</span>${sub ? `<span class="row-sub">${esc(sub)}</span>` : ''}</span>
      <span class="row-end"><span class="row-amount">${esc(fmtMoney(e.amountCents))}</span>
        <span class="row-pay">${pin}${esc(pay)}</span></span></button></div>`;
}

function daySectionsHtml(list) {
  const days = [];
  list.forEach((e) => {
    const last = days[days.length - 1];
    if (last && last.date === e.date) last.items.push(e); else days.push({ date: e.date, items: [e] });
  });
  return days.map((day) =>
    `<section class="day" data-date="${esc(day.date)}">
       <div class="section-head"><span class="day-label">${esc(dayLabel(day.date))}</span>
         <span class="day-total num">${esc(fmtMoney(sumCents(day.items)))}</span></div>
       <div class="card">${day.items.map(historyRowHtml).join('')}</div>
     </section>`).join('');
}

function filterChipsHtml(active) {
  const f = ui.filters;
  const chip = (id, act, label, on, extra) =>
    `<button type="button" class="fchip" id="${id}" data-act="${act}" aria-pressed="${on}"${extra || ''}>${esc(label)}</button>`;
  let catLabel = STRINGS.filterCategory;
  if (f.cats.length === 1) catLabel = catById(f.cats[0]).name;
  else if (f.cats.length > 1) catLabel = STRINGS.filterCategoryCount(f.cats.length);
  let cardLabel = STRINGS.filterCard;
  if (f.card === NO_CARD) cardLabel = STRINGS.cashAndOther;
  else if (f.card !== null) { const card = cardById(f.card); cardLabel = card ? cardDisplayName(card) : STRINGS.filterCard; }
  const parts = [
    chip('f-category', 'filter-category', catLabel, f.cats.length > 0),
    chip('f-card', 'filter-card', cardLabel, f.card !== null),
    chip('f-loc', 'filter-loc', STRINGS.filterHasLocation, f.hasLocation)
  ];
  if (f.day) parts.push(chip('f-day', 'filter-day-clear', STRINGS.filterRemovable(dayLabel(f.day)), true, ` aria-label="${esc(STRINGS.filterRemove(dayLabel(f.day)))}"`));
  if (f.month) parts.push(chip('f-month', 'filter-month-clear', STRINGS.filterRemovable(monthLabel(f.month)), true, ` aria-label="${esc(STRINGS.filterRemove(monthLabel(f.month)))}"`));
  if (active) parts.push(`<button type="button" class="fchip fchip-clear" id="f-clear" data-act="filter-clear">${esc(STRINGS.clear)}</button>`);
  return `<div class="fchips" id="h-filters">${parts.join('')}</div>`;
}

VIEWS.history = function renderHistory() {
  el.view.innerHTML =
    `<div class="page history">
       <input class="input search" type="search" id="h-search" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search"
         placeholder="${esc(STRINGS.searchPlaceholder)}" aria-label="${esc(STRINGS.searchLabel)}" value="${esc(ui.filters.text)}">
       <div id="h-head"></div>
       <div id="h-body"></div>
     </div>`;
  $('#h-search', el.view).addEventListener('input', (e) => { ui.filters.text = e.target.value; renderHistoryBody(); });
  renderHistoryBody();
};

// Everything under the search box. Kept separate so typing never loses focus.
function renderHistoryBody() {
  const head = $('#h-head'), body = $('#h-body');
  if (!head || !body) return;
  swipe.open = null;
  const active = filtersActive(ui.filters);
  if (!active) {
    const list = expensesInMonth(ui.month).sort(newestFirst);
    head.innerHTML = filterChipsHtml(false) + monthSwitchHtml() +
      `<div class="month-total"><div class="big" id="month-total">${esc(fmtMoney(sumCents(list)))}</div>
         <div class="sub">${esc(STRINGS.monthTotal)}</div></div>`;
    body.innerHTML = list.length ? daySectionsHtml(list)
      : `<div class="empty"><p>${esc(STRINGS.noExpenses(monthLabel(ui.month)))}</p>
           <button type="button" class="btn primary" data-act="tab" data-tab="add">${esc(STRINGS.addExpense)}</button></div>`;
    return;
  }
  // Search or filters: every month, grouped by month and then by day.
  const list = filterExpenses(ui.filters).sort(newestFirst);
  head.innerHTML = filterChipsHtml(true) +
    `<div class="month-total"><div class="big" id="results-total">${esc(fmtMoney(sumCents(list)))}</div>
       <div class="sub" id="results-count">${esc(STRINGS.resultCount(list.length))}</div></div>`;
  if (!list.length) { body.innerHTML = `<div class="empty"><p>${esc(STRINGS.noResults)}</p></div>`; return; }
  const months = [];
  list.forEach((e) => {
    const key = e.date.slice(0, 7);
    const last = months[months.length - 1];
    if (last && last.key === key) last.items.push(e); else months.push({ key, items: [e] });
  });
  body.innerHTML = months.map((m) => {
    const label = monthLabel({ y: Number(m.key.slice(0, 4)), m: Number(m.key.slice(5, 7)) - 1 });
    return `<section class="month-group" data-month="${m.key}">
      <div class="month-head"><span class="month-name">${esc(label)}</span><span class="month-sum num">${esc(fmtMoney(sumCents(m.items)))}</span></div>
      ${daySectionsHtml(m.items)}</section>`;
  }).join('');
}

// Summary taps land here: History with one filter set, limited to a month where given.
function openHistoryFiltered(patch) {
  ui.filters = Object.assign(emptyFilters(), patch);
  switchTab('history');
}

function setFilter(patch) {
  Object.assign(ui.filters, patch);
  renderHistoryBody();
}

function clearFilters() {
  ui.filters = emptyFilters();
  const box = $('#h-search');
  if (box) box.value = '';
  renderHistoryBody();
}

function openCategoryFilterSheet() {
  const picked = new Set(ui.filters.cats);
  const rows = state.categories.slice().sort((a, b) => a.name.localeCompare(b.name, 'en', { sensitivity: 'base' })).map((c) =>
    `<label class="row check-row"><input type="checkbox" value="${esc(c.id)}"${picked.has(c.id) ? ' checked' : ''}>
       <span class="row-emoji" aria-hidden="true">${esc(c.emoji)}</span>
       <span class="row-text"><span class="row-title">${esc(c.name + (c.hidden ? STRINGS.hiddenSuffix : ''))}</span></span></label>`).join('');
  const node = openSheet(STRINGS.filterCategoryTitle,
    `<div class="sheet-list" id="fc-list">${rows}</div>
     <div class="btn-row sticky-actions">
       <button type="button" class="btn" id="fc-none">${esc(STRINGS.clear)}</button>
       <button type="button" class="btn primary" id="fc-done">${esc(STRINGS.done)}</button>
     </div>`);
  const apply = () => setFilter({ cats: $$('#fc-list input:checked', node).map((n) => n.value) });
  $('#fc-list', node).addEventListener('change', apply);
  $('#fc-none', node).addEventListener('click', () => { $$('#fc-list input', node).forEach((n) => { n.checked = false; }); apply(); });
  $('#fc-done', node).addEventListener('click', closeSheet);
}

function openCardFilterSheet() {
  const used = new Set(state.expenses.map((e) => e.cardId).filter(Boolean));
  const cards = activeCards().concat(archivedCards().filter((c) => used.has(c.id)));
  const row = (value, label, sub, colour) =>
    `<button type="button" class="row" data-card="${esc(value)}" aria-pressed="${String(ui.filters.card === (value === '' ? null : value))}">
       ${colour ? `<i class="card-dot sw-${colour}" aria-hidden="true"></i>` : '<i class="card-dot sw-none" aria-hidden="true"></i>'}
       <span class="row-text"><span class="row-title">${esc(label)}</span>${sub ? `<span class="row-sub">${esc(sub)}</span>` : ''}</span></button>`;
  const rows = [row('', STRINGS.filterAllCards, '', null)]
    .concat(cards.map((c) => row(c.id, cardShortLabel(c), c.archived ? STRINGS.archived : '', c.colour)))
    .concat([row(NO_CARD, STRINGS.cashAndOther, STRINGS.cashAndOtherHelp, null)]);
  const node = openSheet(STRINGS.filterCardTitle, `<div class="sheet-list" id="fk-list">${rows.join('')}</div>`);
  node.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-card]');
    if (!btn) return;
    closeSheet();
    setFilter({ card: btn.dataset.card === '' ? null : btn.dataset.card });
  });
}

/* ----- Swipe actions ----- */
// Left: a short swipe reveals Delete, a long one deletes. Right: Again. A gesture counts as
// a swipe only once it has moved 10 px and is clearly more sideways than vertical, so
// scrolling the list never triggers one. Rows also set touch-action: pan-y in the CSS.
const SWIPE = { slop: 10, ratio: 1.5, openWidth: 88, againAt: 72, fullAt: 0.55 };
const swipe = { wrap: null, pointerId: null, x0: 0, y0: 0, base: 0, x: 0, mode: null, open: null, suppressClick: false, suppressTimer: null };

function setSwipeX(wrap, x, animate) {
  const row = $('.row', wrap);
  if (!row) return;
  row.style.transition = animate ? 'transform .18s ease-out' : 'none';
  row.style.transform = x ? `translateX(${x}px)` : '';
  wrap.classList.toggle('show-again', x > 0);
  wrap.classList.toggle('show-delete', x < 0);
}

function closeOpenSwipe() {
  if (swipe.open && swipe.open.isConnected) setSwipeX(swipe.open, 0, true);
  swipe.open = null;
}

// The click that follows a swipe, or the tap that closes an open row, must not also open the Edit sheet.
function suppressNextClick() {
  swipe.suppressClick = true;
  clearTimeout(swipe.suppressTimer);
  swipe.suppressTimer = setTimeout(() => { swipe.suppressClick = false; }, 350);
}

function swipeReset() { swipe.wrap = null; swipe.pointerId = null; swipe.mode = null; }

function swipeDelete(id) {
  const expense = state.expenses.find((e) => e.id === id);
  if (!expense) return;
  deleteExpense(id);
  render();
  showToast(STRINGS.expenseDeleted, { ms: 5000, onUndo: () => { restoreExpense(expense); render(); } });
}

document.addEventListener('pointerdown', (e) => {
  const wrap = ui.tab === 'history' && e.target.closest ? e.target.closest('.swipe') : null;
  if (swipe.open && swipe.open !== wrap) {           // only one row open; a tap elsewhere closes it
    closeOpenSwipe();
    suppressNextClick();
  }
  if (!wrap || sheet.node || e.target.closest('.swipe-delete')) return;
  if (e.pointerType === 'mouse' && e.button !== 0) return;
  swipe.wrap = wrap;
  swipe.pointerId = e.pointerId;
  swipe.x0 = e.clientX;
  swipe.y0 = e.clientY;
  swipe.base = swipe.open === wrap ? -SWIPE.openWidth : 0;
  swipe.x = swipe.base;
  swipe.mode = 'pending';
});

document.addEventListener('pointermove', (e) => {
  if (!swipe.wrap || e.pointerId !== swipe.pointerId) return;
  const dx = e.clientX - swipe.x0, dy = e.clientY - swipe.y0;
  if (swipe.mode === 'pending') {
    const ax = Math.abs(dx), ay = Math.abs(dy);
    if (ay > SWIPE.slop && ay * SWIPE.ratio >= ax) { swipeReset(); return; }      // a scroll, not a swipe
    if (!(ax > SWIPE.slop && ax > ay * SWIPE.ratio)) return;
    swipe.mode = 'swiping';
    try { swipe.wrap.setPointerCapture(e.pointerId); } catch (err) { /* not essential */ }
  }
  const width = swipe.wrap.offsetWidth;
  swipe.x = Math.max(-width, Math.min(width * 0.6, swipe.base + dx));
  setSwipeX(swipe.wrap, swipe.x, false);
});

document.addEventListener('pointerup', (e) => {
  if (!swipe.wrap || e.pointerId !== swipe.pointerId) return;
  const wrap = swipe.wrap, mode = swipe.mode, x = swipe.x;
  swipeReset();
  if (mode !== 'swiping') return;
  suppressNextClick();
  const id = wrap.dataset.id;
  if (x <= -wrap.offsetWidth * SWIPE.fullAt) { swipe.open = null; swipeDelete(id); }
  else if (x <= -SWIPE.openWidth / 2) { setSwipeX(wrap, -SWIPE.openWidth, true); swipe.open = wrap; }
  else if (x >= SWIPE.againAt) { setSwipeX(wrap, 0, true); swipe.open = null; repeatExpense(id); }
  else { setSwipeX(wrap, 0, true); if (swipe.open === wrap) swipe.open = null; }
});

// The browser took the gesture over (it became a scroll): put the row back where it was.
document.addEventListener('pointercancel', (e) => {
  if (!swipe.wrap || e.pointerId !== swipe.pointerId) return;
  const wrap = swipe.wrap, mode = swipe.mode;
  swipeReset();
  if (mode === 'swiping') setSwipeX(wrap, swipe.open === wrap ? -SWIPE.openWidth : 0, true);
});

/* ----- Edit sheet ----- */
function categoryOptionsHtml(selected) {
  return state.categories.slice().sort(byOrder).map((c) =>
    `<option value="${esc(c.id)}"${c.id === selected ? ' selected' : ''}>${esc(c.emoji + ' ' + c.name + (c.hidden ? STRINGS.hiddenSuffix : ''))}</option>`).join('');
}

// A native select with two groups. An archived card stays listed for the expense that uses it.
function paymentSelectHtml(expense) {
  const selected = payValue(expense.paymentMethodId, cardById(expense.cardId) ? expense.cardId : null);
  const option = (value, label) => `<option value="${esc(value)}"${value === selected ? ' selected' : ''}>${esc(label)}</option>`;
  const cards = activeCards();
  const own = cardById(expense.cardId);
  if (own && own.archived) cards.push(own);
  const others = PAYMENT_METHODS.map((p) => option(payValue(p.id, null), methodLabel(p.id))).join('');
  if (!cards.length) return others;
  return `<optgroup label="${esc(STRINGS.myCards)}">${cards.map((c) =>
      option(payValue(c.kind, c.id), cardShortLabel(c) + (c.archived ? STRINGS.archivedSuffix : ''))).join('')}</optgroup>
    <optgroup label="${esc(STRINGS.otherWays)}">${others}</optgroup>`;
}

function openEditSheet(id) {
  const expense = state.expenses.find((e) => e.id === id);
  if (!expense) return;
  let location = expense.location;      // edited locally, written on Save
  let finding = false, locError = '';
  const node = openSheet(STRINGS.editTitle,
    `<label class="field"><span class="label">${esc(STRINGS.amount)}</span>
       <input class="input num" type="text" inputmode="decimal" id="e-amount" autocomplete="off" value="${esc(centsToPlain(expense.amountCents))}"></label>
     <label class="field"><span class="label">${esc(STRINGS.category)}</span>
       <select class="input" id="e-category">${categoryOptionsHtml(expense.categoryId)}</select></label>
     <label class="field"><span class="label">${esc(STRINGS.date)}</span>
       <input class="input" type="date" id="e-date" value="${esc(expense.date)}"></label>
     <label class="field"><span class="label">${esc(STRINGS.paymentMethod)}</span>
       <select class="input" id="e-pay">${paymentSelectHtml(expense)}</select></label>
     <label class="field"><span class="label">${esc(STRINGS.merchant)}</span>
       <input class="input" type="text" id="e-merchant" maxlength="60" autocomplete="off" autocapitalize="words" value="${esc(expense.merchant)}">
       <div class="suggest" id="e-suggest" aria-label="${esc(STRINGS.suggestionsLabel)}"></div></label>
     <label class="field"><span class="label">${esc(STRINGS.note)}</span>
       <input class="input" type="text" id="e-note" maxlength="200" autocomplete="off" value="${esc(expense.note)}"></label>
     <div class="field"><span class="label">${esc(STRINGS.location)}</span><div id="e-loc"></div></div>
     <p class="error" id="e-error" role="alert"></p>
     <div id="e-actions">
       <button type="button" class="btn primary block" id="e-save">${esc(STRINGS.save)}</button>
       <div class="btn-row"><button type="button" class="btn" id="e-again">${esc(STRINGS.logAgainToday)}</button></div>
       <div class="btn-row">
         <button type="button" class="btn" id="e-cancel">${esc(STRINGS.cancel)}</button>
         <button type="button" class="btn ghost-danger" id="e-delete">${esc(STRINGS.del)}</button>
       </div>
     </div>
     <div id="e-confirm" hidden>
       <p class="result" id="e-confirm-text">${esc(STRINGS.deleteConfirm)}</p>
       <div class="btn-row">
         <button type="button" class="btn" id="e-confirm-cancel">${esc(STRINGS.cancel)}</button>
         <button type="button" class="btn danger" id="e-confirm-delete">${esc(STRINGS.del)}</button>
       </div>
     </div>`);

  // Location: a plain link to Google Maps, with a one-time notice before the first use.
  const locBox = $('#e-loc', node);
  const mapLink = (elId, cls, label) =>
    `<a class="btn ${cls}" id="${elId}" href="${esc(mapsHref(location))}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`;
  const renderLoc = () => {
    if (location) {
      locBox.innerHTML =
        `<p class="loc-line"><span id="e-loc-status">${esc(STRINGS.locHas(locAccuracy(location)))}</span></p>
         <div class="btn-row" id="e-loc-actions">${mapLink('e-maps', '', STRINGS.openInMaps)}
           <button type="button" class="btn" id="e-loc-remove">${esc(STRINGS.remove)}</button></div>
         <div id="e-maps-notice" hidden>
           <p class="help" id="e-maps-notice-text">${esc(STRINGS.mapsNotice)}</p>
           <div class="btn-row"><button type="button" class="btn" id="e-maps-cancel">${esc(STRINGS.cancel)}</button>
             ${mapLink('e-maps-continue', 'primary', STRINGS.continue)}</div>
         </div>`;
    } else if (finding) {
      locBox.innerHTML = `<p class="loc-line"><span id="e-loc-status" role="status">${esc(STRINGS.locFinding)}</span></p>`;
    } else {
      locBox.innerHTML =
        `<button type="button" class="btn block" id="e-loc-add">${esc(STRINGS.locAddPlain)}</button>
         <p class="help" id="e-loc-note">${esc(STRINGS.locNowNote)}</p>
         ${locError ? `<p class="error" id="e-loc-error" role="alert">${esc(locError)}</p>` : ''}`;
    }
  };
  renderLoc();
  locBox.addEventListener('click', (e) => {
    const notice = $('#e-maps-notice', locBox);
    if (e.target.closest('#e-maps')) {
      if (!state.settings.mapsNoticeShown) {       // first tap ever: explain, and let them choose
        e.preventDefault();
        state.settings.mapsNoticeShown = true;
        saveState();
        notice.hidden = false;
        $('#e-loc-actions', locBox).hidden = true;
        $('#e-maps-cancel', locBox).focus();
      }
    } else if (e.target.closest('#e-maps-cancel') || e.target.closest('#e-maps-continue')) {
      notice.hidden = true;                        // Continue is itself the link, so it just opens
      $('#e-loc-actions', locBox).hidden = false;
    } else if (e.target.closest('#e-loc-remove')) {
      location = null;
      renderLoc();
      $('#e-loc-add', locBox).focus();
    } else if (e.target.closest('#e-loc-add')) {
      finding = true; locError = '';
      renderLoc();
      requestPosition().then((res) => {
        if (sheet.node !== node) return;           // the sheet was closed meanwhile
        finding = false;
        if (res.ok) location = res.location; else locError = locErrorText(res.reason);
        renderLoc();
      });
    }
  });

  const amount = $('#e-amount', node);
  amount.addEventListener('input', () => {
    const clean = sanitizeAmountText(amount.value);
    if (clean !== amount.value) amount.value = clean;
  });
  bindSuggestions($('#e-merchant', node), $('#e-suggest', node));
  const showConfirm = (on) => {
    $('#e-actions', node).hidden = on;
    $('#e-confirm', node).hidden = !on;
    (on ? $('#e-confirm-cancel', node) : $('#e-delete', node)).focus();
  };
  $('#e-cancel', node).addEventListener('click', closeSheet);
  $('#e-again', node).addEventListener('click', () => { closeSheet(); repeatExpense(id); });
  $('#e-delete', node).addEventListener('click', () => showConfirm(true));
  $('#e-confirm-cancel', node).addEventListener('click', () => showConfirm(false));
  $('#e-confirm-delete', node).addEventListener('click', () => {
    deleteExpense(id);
    closeSheet();
    render();
    showToast(STRINGS.expenseDeleted, { ms: 2000 });
  });
  $('#e-save', node).addEventListener('click', () => {
    const cents = typedToCents(sanitizeAmountText(amount.value));
    const date = $('#e-date', node).value;
    const error = cents <= 0 ? STRINGS.errAmount : !isValidYmd(date) ? STRINGS.errDate : '';
    $('#e-error', node).textContent = error;
    if (error) return;
    const pay = parsePayValue($('#e-pay', node).value);
    updateExpense(id, {
      amountCents: cents,
      date,
      categoryId: $('#e-category', node).value,
      paymentMethodId: pay.methodId,
      cardId: pay.cardId,
      merchant: $('#e-merchant', node).value.trim(),
      note: $('#e-note', node).value.trim(),
      location
    });
    closeSheet();
    render();
    showToast(STRINGS.expenseSaved, { ms: 2000 });
  });
}

/* =====================================================================
   16. View: Summary (charts you can tap, by category, by card, tax time)
   ===================================================================== */
// Whole percentages that add up to exactly 100 (largest remainder method).
function shares(amounts, total) {
  if (total <= 0) return amounts.map(() => 0);
  const exact = amounts.map((a) => (a * 100) / total);
  const out = exact.map(Math.floor);
  let left = 100 - out.reduce((s, n) => s + n, 0);
  const order = exact.map((x, i) => ({ i, frac: x - Math.floor(x) })).sort((a, b) => b.frac - a.frac || a.i - b.i);
  for (let k = 0; left > 0 && k < order.length; k++, left--) out[order[k].i] += 1;
  return out;
}

const DONUT = { size: 200, outer: 94, inner: 60, maxSlices: 8 };

function polar(radius, angle) {
  const c = DONUT.size / 2;
  return (c + radius * Math.cos(angle)).toFixed(2) + ' ' + (c + radius * Math.sin(angle)).toFixed(2);
}

// One ring segment from angle a0 to a1 (radians, clockwise from 12 o'clock).
function ringSegment(a0, a1) {
  const large = a1 - a0 > Math.PI ? 1 : 0;
  const R = DONUT.outer, r = DONUT.inner;
  return `M${polar(R, a0)}A${R} ${R} 0 ${large} 1 ${polar(R, a1)}L${polar(r, a1)}A${r} ${r} 0 ${large} 0 ${polar(r, a0)}Z`;
}

// rows: [{ cat, cents }] sorted highest first. At most 8 slices: the top 7 plus "Other".
function donutSlices(rows) {
  const top = rows.slice(0, DONUT.maxSlices - 1), rest = rows.slice(DONUT.maxSlices - 1);
  const slices = top.map((r) => ({ label: r.cat.name, ids: [r.cat.id], cents: r.cents }));
  if (rest.length === 1) slices.push({ label: rest[0].cat.name, ids: [rest[0].cat.id], cents: rest[0].cents });
  else if (rest.length > 1) slices.push({ label: STRINGS.otherSlice, ids: rest.map((r) => r.cat.id), cents: sumCents(rest.map((r) => ({ amountCents: r.cents }))) });
  return slices;
}

function donutHtml(rows, total) {
  const slices = donutSlices(rows);
  const pcts = shares(slices.map((s) => s.cents), total);
  const start = -Math.PI / 2, full = Math.PI * 2;
  let done = 0;
  const paths = slices.map((s, i) => {
    const a0 = start + (done / total) * full;
    done += s.cents;
    const a1 = start + (done / total) * full;
    // A full circle cannot be drawn as one arc, so a lone slice is two halves.
    const d = slices.length === 1 ? ringSegment(a0, a0 + Math.PI) + ringSegment(a0 + Math.PI, a0 + full) : ringSegment(a0, a1);
    const label = STRINGS.sliceLabel(s.label, fmtMoney(s.cents), pcts[i]);
    return `<path class="slice dc${i}" d="${d}" tabindex="0" role="button" data-act="filter-cats" data-cats="${esc(s.ids.join(','))}"
      data-cents="${s.cents}" aria-label="${esc(label)}"><title>${esc(label)}</title></path>`;
  }).join('');
  const money = fmtMoney(total);
  const c = DONUT.size / 2;
  return `<svg class="donut" id="donut" viewBox="0 0 ${DONUT.size} ${DONUT.size}" role="group" aria-label="${esc(STRINGS.donutLabel)}">
    ${paths}
    <text class="donut-total${money.length > 10 ? ' small' : ''}" id="donut-total" x="${c}" y="${c + 2}" text-anchor="middle" aria-hidden="true">${esc(money)}</text>
    <text class="donut-sub" x="${c}" y="${c + 22}" text-anchor="middle" aria-hidden="true">${esc(STRINGS.months[ui.month.m])}</text>
  </svg>`;
}

// One bar per day of the month; today is marked. Only days with spending are tappable.
function dailyBarsHtml(list) {
  const year = ui.month.y, month = ui.month.m;
  const days = new Date(year, month + 1, 0).getDate();
  const perDay = new Array(days + 1).fill(0);
  list.forEach((e) => { perDay[Number(e.date.slice(8, 10))] += e.amountCents; });
  const max = Math.max.apply(null, perDay);
  const W = 320, H = 96, axis = 18, step = W / days, barW = Math.max(3, step * 0.66);
  const today = todayStr();
  let bars = '';
  for (let d = 1; d <= days; d++) {
    const date = year + '-' + pad2(month + 1) + '-' + pad2(d);
    const x = (d - 1) * step;
    const isToday = date === today;
    if (isToday) bars += `<circle class="today-dot" id="today-dot" cx="${(x + step / 2).toFixed(2)}" cy="${H + 4}" r="2.2"/>`;
    if (!perDay[d]) {
      bars += `<rect class="bar-empty" x="${(x + (step - barW) / 2).toFixed(2)}" y="${H - 1.5}" width="${barW.toFixed(2)}" height="1.5" rx=".75"/>`;
      continue;
    }
    const h = Math.max(3, (perDay[d] / max) * (H - 4));
    const label = STRINGS.barLabel(dayLabel(date), fmtMoney(perDay[d]));
    bars += `<g class="daybar${isToday ? ' today' : ''}" tabindex="0" role="button" data-act="filter-day" data-day="${date}" data-cents="${perDay[d]}" aria-label="${esc(label)}">
      <title>${esc(label)}</title>
      <rect class="hit" x="${x.toFixed(2)}" y="0" width="${step.toFixed(2)}" height="${H + axis}"/>
      <rect class="dbar" x="${(x + (step - barW) / 2).toFixed(2)}" y="${(H - h).toFixed(2)}" width="${barW.toFixed(2)}" height="${h.toFixed(2)}" rx="${Math.min(2.5, barW / 2).toFixed(2)}"/></g>`;
  }
  let ticks = '';
  for (let d = 1; d <= days; d += 7) {
    ticks += `<text class="axis" x="${((d - 0.5) * step).toFixed(2)}" y="${H + axis - 2}" text-anchor="middle" aria-hidden="true">${d}</text>`;
  }
  return `<svg class="daily" id="daily-bars" viewBox="0 0 ${W} ${H + axis}" role="group" aria-label="${esc(STRINGS.dailyLabel)}">${bars}${ticks}</svg>`;
}

function shareRowsHtml(rows, total, act) {
  const pcts = shares(rows.map((r) => r.cents), total);
  return rows.map((r, i) =>
    `<button type="button" class="cat-row" data-act="${act}" data-ref="${esc(r.key)}" aria-label="${esc(STRINGS.sliceLabel(r.name, fmtMoney(r.cents), pcts[i]))}">
       <span class="cat-line">${r.lead}<span class="name">${esc(r.name)}</span>
         <span class="amt">${esc(fmtMoney(r.cents))}</span><span class="pct">${pcts[i]}%</span></span>
       <span class="bar"><i style="width:${(r.cents * 100 / total).toFixed(2)}%"></i></span>
     </button>`).join('');
}

VIEWS.summary = function renderSummary() {
  const list = expensesInMonth(ui.month);
  const total = sumCents(list);
  const perCat = new Map(), perCard = new Map();
  list.forEach((e) => {
    perCat.set(e.categoryId, (perCat.get(e.categoryId) || 0) + e.amountCents);
    const key = cardById(e.cardId) ? e.cardId : NO_CARD;
    perCard.set(key, (perCard.get(key) || 0) + e.amountCents);
  });
  const rows = Array.from(perCat.entries())
    .map(([id, cents]) => ({ cat: catById(id), cents }))
    .sort((a, b) => b.cents - a.cents || a.cat.order - b.cat.order);

  let body;
  if (!rows.length) {
    body = `<div class="empty"><p>${esc(STRINGS.noExpenses(monthLabel(ui.month)))}</p></div>`;
  } else {
    const catRows = rows.map((r) => ({
      key: r.cat.id, name: r.cat.name, cents: r.cents, lead: `<span aria-hidden="true">${esc(r.cat.emoji)}</span>`
    }));
    const cardRows = Array.from(perCard.entries()).map(([key, cents]) => {
      const card = key === NO_CARD ? null : cardById(key);
      return {
        key, cents,
        name: card ? cardShortLabel(card) : STRINGS.cashAndOther,
        lead: `<i class="card-dot sw-${card ? card.colour : 'none'}" aria-hidden="true"></i>`,
        last: key === NO_CARD
      };
    }).sort((a, b) => (a.last - b.last) || b.cents - a.cents);
    body =
      `<div class="card charts${ui.drawCharts ? ' draw' : ''}" id="charts">
         <div class="donut-wrap">${donutHtml(rows, total)}</div>
         <h2 class="chart-title">${esc(STRINGS.dailyTitle)}</h2>
         ${dailyBarsHtml(list)}
         <p class="footnote">${esc(STRINGS.chartHint)}</p>
       </div>
       <div class="section-head"><span>${esc(STRINGS.byCategory)}</span></div>
       <div class="card" id="by-category">${shareRowsHtml(catRows, total, 'filter-cat')}</div>
       ${state.cards.length ? `<div class="section-head"><span>${esc(STRINGS.byCard)}</span></div>
       <div class="card" id="by-card">${shareRowsHtml(cardRows, total, 'filter-card-row')}</div>` : ''}`;
  }
  ui.drawCharts = false;
  const tax = taxTotalsForYear(ui.month.y);
  el.view.innerHTML =
    `<div class="page">${monthSwitchHtml()}
       <div class="month-total"><div class="big" id="summary-total">${esc(fmtMoney(total))}</div>
         <div class="sub" id="summary-count">${esc(STRINGS.expenseCount(list.length))}</div></div>
       ${body}
       <div class="card" id="tax-card">
         <h2 class="card-title">${esc(STRINGS.taxTime(ui.month.y))}</h2>
         ${TAX_TAGS.map((tag) => `<div class="kv" data-tax="${tag}"><span>${esc(STRINGS.taxRows[tag])}</span><span class="v">${esc(fmtMoney(tax[tag]))}</span></div>`).join('')}
         <p class="footnote">${esc(STRINGS.taxFootnote)}</p>
       </div>
     </div>`;
};

/* =====================================================================
   17. Cards (Profile → My cards; only names are stored, never card numbers)
   ===================================================================== */
// The built-in Canadian card list: one of the site's own files, loaded when first needed
// and kept offline by the service worker. Adding a card by hand works without it.
const catalogue = { status: 'idle', cards: [], pending: null };

function parseCatalogue(data) {
  const issuers = new Map();
  (Array.isArray(data && data.issuers) ? data.issuers : []).forEach((i) => {
    if (i && typeof i.id === 'string' && typeof i.name === 'string') issuers.set(i.id, i.name.trim());
  });
  const seen = new Set();
  const cards = [];
  (Array.isArray(data && data.cards) ? data.cards : []).forEach((c) => {
    if (!c || typeof c.id !== 'string' || !c.id || seen.has(c.id)) return;
    if (typeof c.name !== 'string' || !c.name.trim() || CARD_KINDS.indexOf(c.kind) === -1) return;
    seen.add(c.id);
    cards.push({
      id: c.id,
      issuer: issuers.get(c.issuerId) || '',
      name: c.name.trim().slice(0, 80),
      kind: c.kind,
      networks: (Array.isArray(c.networks) ? c.networks : []).filter((n) => CARD_NETWORKS.indexOf(n) !== -1)
    });
  });
  if (!cards.length) throw new Error('empty card list');
  const cmp = (a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' });
  return cards.sort((a, b) => cmp(a.issuer, b.issuer) || cmp(a.name, b.name));
}

// Resolves true when the list is ready, false when it could not be loaded. Never rejects.
function loadCatalogue() {
  if (catalogue.status === 'ok') return Promise.resolve(true);
  if (catalogue.pending) return catalogue.pending;
  catalogue.status = 'loading';
  let request;
  try {
    request = fetch(CARDS_URL, { credentials: 'same-origin' }).then((res) => {
      if (!res.ok) throw new Error('card list not available');
      return res.json();
    });
  } catch (e) { request = Promise.reject(e); }
  catalogue.pending = request
    .then((data) => { catalogue.cards = parseCatalogue(data); catalogue.status = 'ok'; return true; })
    .catch(() => { catalogue.status = 'failed'; return false; })
    .then((ok) => { catalogue.pending = null; return ok; });
  return catalogue.pending;
}

function searchCatalogue(query, kind) {
  const words = fold(query).split(/\s+/).filter(Boolean);
  return catalogue.cards.filter((c) => {
    if (kind !== 'all' && c.kind !== kind) return false;
    const hay = fold(c.issuer + ' ' + c.name);
    return words.every((w) => hay.indexOf(w) !== -1);
  });
}

// "Issuer · Credit · Visa · •••• 1234". The card's own name is added when a nickname hides it,
// and a part that only repeats an earlier one (an issuer that is also the network) is left out.
function cardMetaLine(card) {
  const parts = [card.nickname ? card.name : '', card.issuer, STRINGS.cardKinds[card.kind], card.networks.join(' / '),
    card.last4 ? STRINGS.last4Dots(card.last4) : ''].filter(Boolean);
  return parts.filter((part, i) => parts.findIndex((other) => other.toLowerCase() === part.toLowerCase()) === i).join(STRINGS.sep);
}

// Results grouped by issuer. mode 'pick': one tap opens the confirmation. mode 'check': multi-select.
function catalogueListHtml(items, mode, picked) {
  if (!items.length) return `<p class="list-note" id="card-no-match">${esc(STRINGS.cardNoMatch)}</p>`;
  const owned = new Set(state.cards.map((c) => c.catalogueId).filter(Boolean));
  let html = '', issuer = null;
  items.forEach((c) => {
    if (c.issuer !== issuer) {
      issuer = c.issuer;
      html += `<p class="group-head">${esc(issuer || STRINGS.otherIssuer)}</p>`;
    }
    const sub = [STRINGS.cardKinds[c.kind], c.networks.join(' / ')].filter(Boolean).join(STRINGS.sep);
    const text = `<span class="row-text"><span class="row-title">${esc(c.name)}</span><span class="row-sub">${esc(sub)}</span></span>`;
    const added = owned.has(c.id) ? `<span class="badge muted">${esc(STRINGS.cardAdded)}</span>` : '';
    html += mode === 'check'
      ? `<label class="row check-row" data-cat-id="${esc(c.id)}"><input type="checkbox" value="${esc(c.id)}"${owned.has(c.id) ? ' checked disabled' : picked.has(c.id) ? ' checked' : ''}>${text}${added}</label>`
      : `<button type="button" class="row" data-cat-id="${esc(c.id)}">${text}${added}${ICONS.chev}</button>`;
  });
  return html;
}

function catalogueStatusHtml(failedText) {
  return `<p class="list-note" id="card-list-status" role="status">${esc(catalogue.status === 'failed' ? failedText : STRINGS.cardListLoading)}</p>`;
}

function openAddCardSheet() {
  let kind = 'all';
  const kinds = ['all'].concat(CARD_KINDS).map((k) =>
    `<button type="button" class="fchip" data-kind="${k}" aria-pressed="${k === kind}">${esc(STRINGS.cardKindFilters[k])}</button>`).join('');
  const node = openSheet(STRINGS.addCard,
    `<p class="help" id="ac-note">${esc(STRINGS.cardNumberNote)}</p>
     <input class="input search" type="search" id="ac-search" autocomplete="off" autocapitalize="off" spellcheck="false"
       placeholder="${esc(STRINGS.cardSearchPlaceholder)}" aria-label="${esc(STRINGS.cardSearchLabel)}">
     <div class="fchips" id="ac-kinds" role="group" aria-label="${esc(STRINGS.cardKindLabel)}">${kinds}</div>
     <div class="sheet-list scroll-list" id="ac-results"></div>
     <button type="button" class="btn block" id="ac-manual">${esc(STRINGS.cardManual)}</button>`);
  const results = $('#ac-results', node), search = $('#ac-search', node);
  const show = () => {
    results.innerHTML = catalogue.status === 'ok'
      ? catalogueListHtml(searchCatalogue(search.value, kind), 'pick')
      : catalogueStatusHtml(STRINGS.cardListFailed);
  };
  show();
  loadCatalogue().then(() => { if (sheet.node === node) show(); });
  search.addEventListener('input', show);
  $('#ac-kinds', node).addEventListener('click', (e) => {
    const btn = e.target.closest('[data-kind]');
    if (!btn) return;
    kind = btn.dataset.kind;
    $$('[data-kind]', node).forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    show();
  });
  results.addEventListener('click', (e) => {
    const row = e.target.closest('[data-cat-id]');
    const item = row && catalogue.cards.find((c) => c.id === row.dataset.catId);
    if (item) openCardForm({ mode: 'catalogue', item });
  });
  $('#ac-manual', node).addEventListener('click', () => openCardForm({ mode: 'manual' }));
}

function colourPickerHtml(selected) {
  return `<fieldset class="field"><legend>${esc(STRINGS.cardColour)}</legend><div class="swatches" id="cf-colours">${CARD_COLOURS.map((c) =>
    `<label class="swatch"><input type="radio" name="cf-colour" value="${c}"${c === selected ? ' checked' : ''} aria-label="${esc(STRINGS.colourNames[c])}"><span class="sw-${c}"></span></label>`).join('')}</div></fieldset>`;
}

// Anything that looks like a long run of digits is refused: card numbers do not belong here.
const looksLikeCardNumber = (text) => /\d{8,}/.test(String(text).replace(/[\s-]/g, ''));

// opts: { mode: 'catalogue', item } | { mode: 'manual' } | { mode: 'edit', card }
function openCardForm(opts) {
  const manual = opts.mode === 'manual', edit = opts.mode === 'edit';
  const card = edit ? opts.card : null;
  const shown = edit ? card : opts.item;
  const used = edit ? state.expenses.filter((e) => e.cardId === card.id).length : 0;
  const summary = manual ? '' :
    `<div class="card-summary" id="cf-summary"><p class="row-title">${esc(shown.name)}</p>
       <p class="row-sub">${esc([shown.issuer, STRINGS.cardKinds[shown.kind], shown.networks.join(' / ')].filter(Boolean).join(STRINGS.sep))}</p></div>`;
  const manualFields = !manual ? '' :
    `<label class="field"><span class="label">${esc(STRINGS.cardIssuer)}</span>
       <input class="input" type="text" id="cf-issuer" maxlength="60" autocomplete="off" autocapitalize="words" placeholder="${esc(STRINGS.cardIssuerPlaceholder)}"></label>
     <label class="field"><span class="label">${esc(STRINGS.cardName)}</span>
       <input class="input" type="text" id="cf-name" maxlength="80" autocomplete="off" autocapitalize="words" placeholder="${esc(STRINGS.cardNamePlaceholder)}"></label>
     <fieldset class="field"><legend>${esc(STRINGS.cardKind)}</legend><div class="options three" id="cf-kinds">${CARD_KINDS.map((k, i) =>
       `<label class="option"><input type="radio" name="cf-kind" value="${k}"${i === 0 ? ' checked' : ''}><span>${esc(STRINGS.cardKinds[k])}</span></label>`).join('')}</div></fieldset>
     <label class="field"><span class="label">${esc(STRINGS.cardNetwork)}</span>
       <select class="input" id="cf-network"><option value="">${esc(STRINGS.cardNetworkNone)}</option>${CARD_NETWORKS.map((n) =>
         `<option value="${esc(n)}">${esc(n)}</option>`).join('')}</select></label>`;
  const node = openSheet(edit ? STRINGS.editCard : STRINGS.addCard,
    `${summary}
     <p class="help" id="cf-note">${esc(STRINGS.cardNumberNote)}</p>
     ${manualFields}
     <label class="field"><span class="label">${esc(STRINGS.cardNickname)}</span>
       <input class="input" type="text" id="cf-nick" maxlength="24" autocomplete="off" autocapitalize="words"
         placeholder="${esc(STRINGS.optional)}" value="${esc(card ? card.nickname : '')}"></label>
     <label class="field"><span class="label">${esc(STRINGS.cardLast4)}</span>
       <input class="input num" type="text" id="cf-last4" inputmode="numeric" maxlength="4" autocomplete="off"
         placeholder="${esc(STRINGS.optional)}" value="${esc(card ? card.last4 : '')}"></label>
     ${colourPickerHtml(card ? card.colour : nextCardColour())}
     <p class="error" id="cf-error" role="alert"></p>
     <div id="cf-actions">
       <div class="btn-row">
         <button type="button" class="btn" id="cf-cancel">${esc(edit ? STRINGS.cancel : STRINGS.back)}</button>
         <button type="button" class="btn primary" id="cf-save">${esc(edit ? STRINGS.save : STRINGS.addCard)}</button>
       </div>
       ${edit ? `<div class="btn-row"><button type="button" class="btn ghost-danger" id="cf-remove">${esc(STRINGS.removeCard)}</button></div>` : ''}
     </div>
     <div id="cf-confirm" hidden>
       <p class="result" id="cf-confirm-text">${esc(used ? STRINGS.archiveCardConfirm(used) : STRINGS.removeCardConfirm)}</p>
       <div class="btn-row">
         <button type="button" class="btn" id="cf-confirm-cancel">${esc(STRINGS.cancel)}</button>
         <button type="button" class="btn danger" id="cf-confirm-remove">${esc(STRINGS.removeCard)}</button>
       </div>
     </div>`);
  const last4 = $('#cf-last4', node);
  last4.addEventListener('input', () => {
    const digits = last4.value.replace(/\D/g, '').slice(0, 4);
    if (digits !== last4.value) last4.value = digits;
  });
  $('#cf-cancel', node).addEventListener('click', () => { if (edit) closeSheet(); else openAddCardSheet(); });
  if (edit) {
    const showConfirm = (on) => { $('#cf-actions', node).hidden = on; $('#cf-confirm', node).hidden = !on; };
    $('#cf-remove', node).addEventListener('click', () => { showConfirm(true); $('#cf-confirm-cancel', node).focus(); });
    $('#cf-confirm-cancel', node).addEventListener('click', () => { showConfirm(false); $('#cf-remove', node).focus(); });
    $('#cf-confirm-remove', node).addEventListener('click', () => {
      const outcome = removeCard(card.id);
      if (ui.draft.cardId === card.id) ui.draft.cardId = null;
      if (outcome === 'deleted' && ui.filters.card === card.id) ui.filters.card = null;
      closeSheet();
      render();
      showToast(outcome === 'archived' ? STRINGS.cardArchived : STRINGS.cardRemoved, { ms: 2500 });
    });
  }
  $('#cf-save', node).addEventListener('click', () => {
    const nickname = $('#cf-nick', node).value.trim().slice(0, 24);
    const tail = last4.value.trim();
    const issuer = manual ? $('#cf-issuer', node).value.trim().slice(0, 60) : '';
    const name = manual ? $('#cf-name', node).value.trim().slice(0, 80) : '';
    const error = manual && !name ? STRINGS.errCardName
      : [issuer, name, nickname].some(looksLikeCardNumber) ? STRINGS.errCardNumber
      : tail && !isLast4(tail) ? STRINGS.errLast4 : '';
    $('#cf-error', node).textContent = error;
    if (error) return;
    const picked = $('input[name="cf-colour"]:checked', node);
    const colour = picked ? picked.value : CARD_COLOURS[0];
    if (edit) {
      Object.assign(card, { nickname, last4: tail, colour });
    } else if (manual) {
      const kind = $('input[name="cf-kind"]:checked', node);
      const network = $('#cf-network', node).value;
      createCard({ issuer, name, kind: kind ? kind.value : 'credit', networks: network ? [network] : [], nickname, last4: tail, colour });
    } else {
      const item = opts.item;
      createCard({ catalogueId: item.id, issuer: item.issuer, name: item.name, kind: item.kind, networks: item.networks.slice(), nickname, last4: tail, colour });
    }
    saveState();
    closeSheet();
    render();
    showToast(edit ? STRINGS.cardSaved : STRINGS.cardAddedToast, { ms: 2000 });
  });
}

function restoreCard(id) {
  const card = cardById(id);
  if (!card) return;
  card.archived = false;
  saveState();
  render();
  showToast(STRINGS.cardRestored, { ms: 2000 });
}

/* =====================================================================
   18. View: Profile
   ===================================================================== */
function storageStatusText() {
  if (store.mode !== 'ok') return STRINGS.storageMemory;
  return embedded ? STRINGS.storageEmbedded : STRINGS.storageStandalone;
}

// Turning automatic location on asks the browser for permission straight away.
function setAutoLocation(on, after) {
  state.settings.autoLocation = on;
  saveState();
  if (!on) { if (after) after(null); return; }
  requestPosition().then((res) => {
    if (!res.ok && res.reason === 'denied') { state.settings.autoLocation = false; saveState(); }
    if (after) after(res);
  });
}

let autoLocError = '';

VIEWS.profile = function renderProfile() {
  const swatch = (c) => `<i class="card-swatch sw-${c.colour}" aria-hidden="true"></i>`;
  const cardText = (c) => `<span class="row-text"><span class="row-title">${esc(cardDisplayName(c))}</span><span class="row-sub">${esc(cardMetaLine(c))}</span></span>`;
  const active = activeCards(), archived = archivedCards();
  const tiles = active.map((c) =>
    `<button type="button" class="row card-tile" data-act="card-edit" data-id="${esc(c.id)}">${swatch(c)}${cardText(c)}${ICONS.chev}</button>`).join('');
  const archivedHtml = !archived.length ? '' :
    `<div class="section-head"><span>${esc(STRINGS.archived)}</span></div>
     <div class="card" id="archived-cards">${archived.map((c) =>
       `<div class="row card-tile archived" data-id="${esc(c.id)}">${swatch(c)}${cardText(c)}
          <button type="button" class="btn small" data-act="card-restore" data-id="${esc(c.id)}" aria-label="${esc(STRINGS.restoreCardLabel(cardDisplayName(c)))}">${esc(STRINGS.restoreCard)}</button></div>`).join('')}</div>`;
  const cats = state.categories.slice().sort(byOrder).map((c) =>
    `<button type="button" class="row" data-act="cat-edit" data-id="${esc(c.id)}">
       <span class="row-emoji" aria-hidden="true">${esc(c.emoji)}</span>
       <span class="row-text"><span class="row-title">${esc(c.name)}</span></span>
       ${tagBadge(c)}${c.hidden ? `<span class="badge muted">${esc(STRINGS.hidden)}</span>` : ''}${ICONS.chev}</button>`).join('');
  el.view.innerHTML =
    `<div class="page">
       <div class="section-head"><span>${esc(STRINGS.myCards)}</span></div>
       <div class="card" id="card-list">
         ${tiles || `<p class="status-line muted" id="no-cards">${esc(STRINGS.noCards)}</p>`}
         <button type="button" class="row plain row-action" id="btn-add-card" data-act="card-add">${esc(STRINGS.addCard)}</button>
       </div>
       ${archivedHtml}

       <div class="section-head"><span>${esc(STRINGS.location)}</span></div>
       <div class="card" id="location-settings">
         <label class="row plain switch-row"><span class="row-text"><span class="row-title">${esc(STRINGS.autoLocation)}</span>
           <span class="row-sub wrap">${esc(STRINGS.autoLocationHelp)}</span></span>
           <input type="checkbox" role="switch" id="set-auto-loc"${state.settings.autoLocation ? ' checked' : ''}></label>
         ${autoLocError ? `<p class="error pad" id="auto-loc-error" role="alert">${esc(autoLocError)}</p>` : ''}
       </div>

       <div class="section-head"><span>${esc(STRINGS.categories)}</span></div>
       <div class="card" id="category-list">${cats}
         <button type="button" class="row plain row-action" id="btn-add-category" data-act="cat-add">${esc(STRINGS.addCategory)}</button>
       </div>

       <div class="section-head"><span>${esc(STRINGS.backup)}</span></div>
       <div class="card">
         <p class="status-line${store.mode !== 'ok' ? ' warn' : ''}" id="storage-status">${esc(storageStatusText())}</p>
         <button type="button" class="row plain row-action" id="btn-copy" data-act="copy-backup">${esc(STRINGS.copyBackup)}</button>
         <button type="button" class="row plain row-action" id="btn-download" data-act="download"${ui.canDownload ? '' : ' hidden'}>${esc(STRINGS.downloadCsv)}</button>
         <button type="button" class="row plain row-action" id="btn-restore" data-act="restore">${esc(STRINGS.restore)}</button>
       </div>

       <div class="card">
         <button type="button" class="row plain row-action danger" id="btn-delete-all" data-act="delete-all">${esc(STRINGS.deleteAll)}</button>
       </div>

       <div class="section-head"><span>${esc(STRINGS.about)}</span></div>
       <div class="card">
         <div class="about">
           <p class="name">${esc(STRINGS.appName)}</p>
           <p class="ver" id="app-version">${esc(STRINGS.versionLabel(STRINGS.version))}</p>
           <p class="privacy" id="privacy">${esc(STRINGS.privacy)}</p>
         </div>
         <button type="button" class="row plain row-action" id="btn-setup-again" data-act="setup-again">${esc(STRINGS.runSetupAgain)}</button>
       </div>
     </div>`;
};

function onAutoLocationToggle(input) {
  autoLocError = '';
  setAutoLocation(input.checked, (res) => {
    if (res && !res.ok && res.reason === 'denied') autoLocError = STRINGS.locDenied;
    if (ui.tab === 'profile' && !sheet.node) VIEWS.profile();
  });
}

/* ----- Backup ----- */
function openCopyFallback(csv) {
  const node = openSheet(STRINGS.copyFallbackTitle,
    `<p class="help">${esc(STRINGS.copyFallbackHelp)}</p>
     <textarea class="input" id="copy-fallback" readonly rows="8" aria-label="${esc(STRINGS.backupText)}"></textarea>
     <div class="btn-row">
       <button type="button" class="btn primary" id="copy-select">${esc(STRINGS.selectAll)}</button>
       <button type="button" class="btn" data-sheet-close>${esc(STRINGS.done)}</button>
     </div>`);
  const area = $('#copy-fallback', node);
  area.value = csv;
  const selectAll = () => { area.focus(); area.select(); try { area.setSelectionRange(0, area.value.length); } catch (e) { /* ignore */ } };
  $('#copy-select', node).addEventListener('click', selectAll);
}

// Called straight from the click handler so the clipboard call keeps its user gesture.
function copyBackup() {
  const csv = buildCsv();
  const count = state.expenses.length;
  let attempt;
  try {
    attempt = navigator.clipboard.writeText(csv);
  } catch (e) {
    openCopyFallback(csv);
    return;
  }
  Promise.resolve(attempt).then(
    () => showToast(STRINGS.copied(count)),
    () => openCopyFallback(csv)
  );
}

function hideDownload() {
  ui.canDownload = false;
  const btn = $('#btn-download');
  if (btn) btn.hidden = true;
}

async function downloadBackup() {
  const filename = backupFilename();
  const data = BOM + buildCsv();
  if (!embedded) {
    try {
      const url = URL.createObjectURL(new Blob([data], { type: 'text/csv;charset=utf-8' }));
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
    } catch (e) {
      hideDownload();
      showToast(STRINGS.downloadUnavailable, { ms: 4000 });
    }
    return;
  }
  try {
    await ui.downloads.save({ filename, data });
    showToast(STRINGS.downloaded);
  } catch (err) {
    const code = err && err.code;
    if (code === 'declined') return;
    if (code === 'rate_limited') { showToast(STRINGS.rateLimited); return; }
    hideDownload();
    showToast(STRINGS.downloadUnavailable, { ms: 4000 });
  }
}

// Standalone: downloads work. Embedded: ask the platform for its downloads capability.
async function probeDownloads() {
  if (!embedded) { ui.canDownload = true; return; }
  try {
    if (window.claude && typeof window.claude.use === 'function') {
      const downloads = await window.claude.use('downloads');
      if (downloads) {
        ui.downloads = downloads;
        ui.canDownload = true;
        const btn = $('#btn-download');
        if (btn) btn.hidden = false;
      }
    }
  } catch (e) { /* stays hidden */ }
}

function openRestoreSheet() {
  const node = openSheet(STRINGS.restoreTitle,
    `<p class="help">${esc(STRINGS.restoreHelp)}</p>
     <label class="field"><span class="label">${esc(STRINGS.chooseFile)}</span>
       <input class="input" type="file" id="r-file" accept=".csv,text/csv,text/plain"></label>
     <label class="field"><span class="label">${esc(STRINGS.orPaste)}</span>
       <textarea class="input" id="r-text" rows="5" autocomplete="off" autocapitalize="off" spellcheck="false"></textarea></label>
     <p class="result" id="r-result" role="status"></p>
     <p class="error" id="r-error" role="alert"></p>
     <div class="btn-row">
       <button type="button" class="btn" data-sheet-close>${esc(STRINGS.close)}</button>
       <button type="button" class="btn primary" id="r-go">${esc(STRINGS.restoreBtn)}</button>
     </div>`);
  const result = $('#r-result', node), error = $('#r-error', node);
  const run = (text) => {
    result.textContent = '';
    error.textContent = '';
    if (!text.trim()) { error.textContent = STRINGS.restoreEmpty; return; }
    const catsBefore = state.categories.length;
    const r = restoreCsv(text);
    if (state.categories.length !== catsBefore) refreshChips();
    if (r.ok && r.newCards && !ui.amount) resetDraft();
    if (!r.ok) { error.textContent = STRINGS.restoreBadHeader; return; }
    result.textContent = STRINGS.restoreResult(r.restored, r.already, r.invalid);
    $('#r-text', node).value = '';
    VIEWS[ui.tab]();
  };
  $('#r-go', node).addEventListener('click', () => run($('#r-text', node).value));
  $('#r-file', node).addEventListener('change', (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => { run(String(reader.result || '')); e.target.value = ''; };
    reader.onerror = () => { result.textContent = ''; error.textContent = STRINGS.restoreReadError; };
    reader.readAsText(file);
  });
}

/* ----- Categories ----- */
function openCategorySheet(id) {
  const cat = id ? state.categories.find((c) => c.id === id) : null;
  if (id && !cat) return;
  const tag = cat ? cat.taxTag || 'none' : 'none';
  const used = cat ? state.expenses.filter((e) => e.categoryId === cat.id).length : 0;
  const tagOptions = ['none'].concat(TAX_TAGS).map((t) =>
    `<label class="option"><input type="radio" name="c-tag" value="${t}"${t === tag ? ' checked' : ''}><span>${esc(STRINGS.taxTags[t])}</span></label>`).join('');
  const custom = cat && !cat.builtIn;
  const node = openSheet(cat ? STRINGS.editCategory : STRINGS.addCategory,
    `<label class="field"><span class="label">${esc(STRINGS.catName)}</span>
       <input class="input" type="text" id="c-name" maxlength="24" autocomplete="off" autocapitalize="sentences" value="${esc(cat ? cat.name : '')}"></label>
     <label class="field"><span class="label">${esc(STRINGS.catEmoji)}</span>
       <input class="input" type="text" id="c-emoji" maxlength="16" autocomplete="off" value="${esc(cat ? cat.emoji : DEFAULT_EMOJI)}"></label>
     <fieldset class="field"><legend>${esc(STRINGS.catTaxTag)}</legend><div class="options" id="c-tags">${tagOptions}</div></fieldset>
     ${cat ? `<label class="toggle"><input type="checkbox" id="c-hidden"${cat.hidden ? ' checked' : ''}><span>${esc(STRINGS.catHide)}</span></label>` : ''}
     <p class="error" id="c-error" role="alert"></p>
     <div id="c-actions">
       <div class="btn-row">
         <button type="button" class="btn" data-sheet-close>${esc(STRINGS.cancel)}</button>
         <button type="button" class="btn primary" id="c-save">${esc(STRINGS.save)}</button>
       </div>
       ${custom && used === 0 ? `<div class="btn-row"><button type="button" class="btn ghost-danger" id="c-delete">${esc(STRINGS.deleteCategory)}</button></div>` : ''}
       ${custom && used > 0 ? `<p class="help" style="margin-top:12px">${esc(STRINGS.catInUse(used))}</p>` : ''}
     </div>
     <div id="c-confirm" hidden>
       <p class="result">${esc(STRINGS.deleteCategoryConfirm)}</p>
       <div class="btn-row">
         <button type="button" class="btn" id="c-confirm-cancel">${esc(STRINGS.cancel)}</button>
         <button type="button" class="btn danger" id="c-confirm-delete">${esc(STRINGS.del)}</button>
       </div>
     </div>`);
  const showConfirm = (on) => { $('#c-actions', node).hidden = on; $('#c-confirm', node).hidden = !on; };
  const del = $('#c-delete', node);
  if (del) {
    del.addEventListener('click', () => { showConfirm(true); $('#c-confirm-cancel', node).focus(); });
    $('#c-confirm-cancel', node).addEventListener('click', () => { showConfirm(false); del.focus(); });
    $('#c-confirm-delete', node).addEventListener('click', () => {
      if (state.expenses.some((e) => e.categoryId === cat.id)) return;
      state.categories = state.categories.filter((c) => c.id !== cat.id);
      saveState();
      refreshChips();
      closeSheet();
      render();
      showToast(STRINGS.catDeleted, { ms: 2000 });
    });
  }
  $('#c-save', node).addEventListener('click', () => {
    const name = $('#c-name', node).value.trim().slice(0, 24);
    const emoji = $('#c-emoji', node).value.trim() || DEFAULT_EMOJI;
    const picked = $('input[name="c-tag"]:checked', node);
    const taxTag = picked && picked.value !== 'none' ? picked.value : null;
    const clash = name && state.categories.some((c) => c !== cat && c.name.trim().toLowerCase() === name.toLowerCase());
    const count = graphemeCount(emoji);
    const error = !name ? STRINGS.errCatName : clash ? STRINGS.errCatDup : (count < 1 || count > 2) ? STRINGS.errCatEmoji : '';
    $('#c-error', node).textContent = error;
    if (error) return;
    if (cat) {
      cat.name = name; cat.emoji = emoji; cat.taxTag = taxTag; cat.hidden = $('#c-hidden', node).checked;
    } else {
      createCategory(name, emoji, taxTag);
    }
    saveState();
    refreshChips();
    closeSheet();
    render();
    showToast(STRINGS.catSaved, { ms: 2000 });
  });
}

/* ----- Delete all ----- */
function openDeleteAllSheet() {
  const node = openSheet(STRINGS.deleteAll,
    `<p class="help">${esc(STRINGS.deleteAllHelp)}</p>
     <label class="field"><span class="label">${esc(STRINGS.deleteAllInput)}</span>
       <input class="input" type="text" id="da-input" autocomplete="off" autocapitalize="characters" autocorrect="off" spellcheck="false"></label>
     <div class="btn-row">
       <button type="button" class="btn" data-sheet-close>${esc(STRINGS.cancel)}</button>
       <button type="button" class="btn danger" id="da-go" disabled>${esc(STRINGS.deleteAll)}</button>
     </div>`, { dismissible: false });
  const input = $('#da-input', node), go = $('#da-go', node);
  input.addEventListener('input', () => { go.disabled = input.value !== STRINGS.deleteAllWord; });
  go.addEventListener('click', () => {
    if (input.value !== STRINGS.deleteAllWord) return;
    state = defaultState();
    removeLeftovers();
    store.corrupt = null;
    saveState();
    refreshChips();
    resetDraft();
    ui.month = currentMonth();
    ui.filters = emptyFilters();
    autoLocError = '';
    closeSheet();
    render();
    showToast(STRINGS.deleteAllDone);
  });
}

/* =====================================================================
   19. First-run setup (three steps; can be skipped at any step)
   ===================================================================== */
function openWelcome() {
  const ob = { step: 1, picked: new Set(), query: '' };
  // However the sheet goes away (Skip, Done, ×, backdrop, Escape), setup is not shown again.
  const finished = () => {
    if (!state.settings.onboarded) { state.settings.onboarded = true; saveState(); }
  };
  const buttons = (last) =>
    `<div class="btn-row"><button type="button" class="btn" id="ob-skip">${esc(STRINGS.skip)}</button>
       <button type="button" class="btn primary" id="${last ? 'ob-done' : 'ob-next'}">${esc(last ? STRINGS.done : STRINGS.next)}</button></div>`;
  const stepLine = () => `<p class="ob-step" id="ob-step">${esc(STRINGS.obStep(ob.step, 3))}</p>`;

  function addPickedCards() {
    const owned = new Set(state.cards.map((c) => c.catalogueId).filter(Boolean));
    let added = 0;
    catalogue.cards.forEach((item) => {
      if (!ob.picked.has(item.id) || owned.has(item.id)) return;
      createCard({ catalogueId: item.id, issuer: item.issuer, name: item.name, kind: item.kind, networks: item.networks.slice() });
      added += 1;
    });
    ob.picked.clear();
    if (added) { saveState(); if (!ui.amount) resetDraft(); }
  }

  function show() {
    let node;
    if (ob.step === 1) {
      node = openSheet(STRINGS.obTitle1,
        `${stepLine()}<p class="ob-lead">${esc(STRINGS.obBody1)}</p>
         <p class="help" id="ob-privacy">${esc(STRINGS.privacy)}</p>${buttons(false)}`, { onClose: finished });
    } else if (ob.step === 2) {
      node = openSheet(STRINGS.obTitle2,
        `${stepLine()}<p class="help">${esc(STRINGS.obBody2)} ${esc(STRINGS.cardNumberNote)}</p>
         <input class="input search" type="search" id="ob-search" autocomplete="off" autocapitalize="off" spellcheck="false"
           placeholder="${esc(STRINGS.cardSearchPlaceholder)}" aria-label="${esc(STRINGS.cardSearchLabel)}" value="${esc(ob.query)}">
         <div class="sheet-list scroll-list" id="ob-cards"></div>${buttons(false)}`, { onClose: finished });
      const list = $('#ob-cards', node), search = $('#ob-search', node);
      const fill = () => {
        list.innerHTML = catalogue.status === 'ok'
          ? catalogueListHtml(searchCatalogue(ob.query, 'all'), 'check', ob.picked)
          : catalogueStatusHtml(STRINGS.obCardListFailed);
      };
      fill();
      loadCatalogue().then(() => { if (sheet.node === node) fill(); });
      search.addEventListener('input', () => { ob.query = search.value; fill(); });
      list.addEventListener('change', (e) => {
        if (!e.target.value) return;
        if (e.target.checked) ob.picked.add(e.target.value); else ob.picked.delete(e.target.value);
      });
    } else {
      node = openSheet(STRINGS.obTitle3,
        `${stepLine()}<p class="ob-lead">${esc(STRINGS.obBody3)}</p>
         <label class="row plain switch-row boxed"><span class="row-text"><span class="row-title">${esc(STRINGS.autoLocation)}</span>
           <span class="row-sub wrap">${esc(STRINGS.offByDefault)}</span></span>
           <input type="checkbox" role="switch" id="ob-auto"${state.settings.autoLocation ? ' checked' : ''}></label>
         <p class="error" id="ob-loc-error" role="alert"></p>${buttons(true)}`, { onClose: finished });
      const toggle = $('#ob-auto', node);
      toggle.addEventListener('change', () => {
        $('#ob-loc-error', node).textContent = '';
        setAutoLocation(toggle.checked, (res) => {
          if (sheet.node !== node || !res || res.ok || res.reason !== 'denied') return;
          toggle.checked = false;
          $('#ob-loc-error', node).textContent = STRINGS.locDenied;
        });
      });
    }
    $('#ob-skip', node).addEventListener('click', closeSheet);
    const next = $('#ob-next', node);
    if (next) next.addEventListener('click', () => {
      if (ob.step === 2) addPickedCards();     // cards chosen here are kept even if step 3 is skipped
      ob.step += 1;
      show();
    });
    const done = $('#ob-done', node);
    if (done) done.addEventListener('click', () => { closeSheet(); switchTab('add'); });
  }
  loadCatalogue();
  show();
}

/* =====================================================================
   20. Offline: service worker registration and the "Update ready" banner
   ===================================================================== */
function registerServiceWorker() {
  if (embedded) return;
  let container = null;
  try { container = navigator.serviceWorker; } catch (e) { return; }
  if (!container || typeof container.register !== 'function') return;
  // A new version is "ready" only when an older one is still running this page.
  const flag = () => { if (container.controller) { sw.updateReady = true; renderBanners(); } };
  const watch = (worker) => {
    if (!worker) return;
    worker.addEventListener('statechange', () => { if (worker.state === 'installed') flag(); });
  };
  container.addEventListener('controllerchange', () => { if (sw.reloading) window.location.reload(); });
  try {
    container.register('sw.js').then((reg) => {
      sw.reg = reg;
      if (reg.waiting) flag();
      watch(reg.installing);
      reg.addEventListener('updatefound', () => watch(reg.installing));
    }).catch(() => { /* offline support is a bonus; the app works without it */ });
  } catch (e) { /* same */ }
}

// "Reload" on the banner: let the waiting version take over, then reload once it has.
function applyUpdate() {
  const waiting = sw.reg && sw.reg.waiting;
  if (!waiting) { window.location.reload(); return; }
  sw.reloading = true;
  waiting.postMessage({ type: 'SKIP_WAITING' });
}

// An installed app can stay open for days: look for a new version when it comes back into view.
function checkForUpdate() {
  try {
    if (sw.reg && navigator.onLine !== false) sw.reg.update().catch(() => {});
  } catch (e) { /* ignore */ }
}

/* =====================================================================
   21. Events
   ===================================================================== */
const monthCopy = () => ({ y: ui.month.y, m: ui.month.m });

const ACTIONS = {
  tab: (t) => switchTab(t.dataset.tab),
  chip: (t) => saveDraftTo(t.dataset.cat),
  usual: (t) => saveDraftTo(t.dataset.cat),
  'chip-more': () => { if (typedToCents(ui.amount) <= 0) nudgeAmount(); else openAllCategoriesSheet(); },
  details: openDetailsSheet,
  recent: openRecentSheet,
  month: (t) => { ui.month = shiftMonth(ui.month, Number(t.dataset.delta)); if (ui.tab === 'history') renderHistoryBody(); else VIEWS[ui.tab](); },
  edit: (t) => { if (swipe.open) { closeOpenSwipe(); return; } openEditSheet(t.dataset.id); },
  'swipe-delete': (t) => swipeDelete(t.dataset.id),
  'filter-category': openCategoryFilterSheet,
  'filter-card': openCardFilterSheet,
  'filter-loc': () => setFilter({ hasLocation: !ui.filters.hasLocation }),
  'filter-day-clear': () => setFilter({ day: null }),
  'filter-month-clear': () => setFilter({ month: null }),
  'filter-clear': clearFilters,
  // Summary taps: History with that filter, for the month on screen (a day needs no month).
  'filter-cats': (t) => openHistoryFiltered({ cats: t.dataset.cats.split(',').filter(Boolean), month: monthCopy() }),
  'filter-cat': (t) => openHistoryFiltered({ cats: [t.dataset.ref], month: monthCopy() }),
  'filter-card-row': (t) => openHistoryFiltered({ card: t.dataset.ref, month: monthCopy() }),
  'filter-day': (t) => openHistoryFiltered({ day: t.dataset.day }),
  'card-add': openAddCardSheet,
  'card-edit': (t) => { const card = cardById(t.dataset.id); if (card) openCardForm({ mode: 'edit', card }); },
  'card-restore': (t) => restoreCard(t.dataset.id),
  'copy-backup': copyBackup,
  download: downloadBackup,
  restore: openRestoreSheet,
  'cat-add': () => openCategorySheet(null),
  'cat-edit': (t) => openCategorySheet(t.dataset.id),
  'delete-all': openDeleteAllSheet,
  'setup-again': openWelcome,
  'update-reload': applyUpdate,
  'dismiss-test': () => { state.settings.testNoticeDismissed = true; saveState(); renderBanners(); },
  'dismiss-corrupt': () => { ui.corruptDismissed = true; renderBanners(); }
};

el.app.addEventListener('click', (e) => {
  if (swipe.suppressClick) { swipe.suppressClick = false; return; }
  const key = e.target.closest('[data-key]');
  if (key) { pressKey(key.dataset.key); return; }
  const target = e.target.closest('[data-act]');
  if (target && ACTIONS[target.dataset.act]) ACTIONS[target.dataset.act](target);
});

el.app.addEventListener('change', (e) => {
  if (e.target.id === 'set-auto-loc') onAutoLocationToggle(e.target);
});

document.addEventListener('keydown', (e) => {
  if (sheet.node) {
    if (e.key === 'Escape') { e.preventDefault(); closeSheet(); }
    else if (e.key === 'Tab') trapFocus(e);
    return;
  }
  // Chart slices and bars are focusable shapes, not buttons: give them Enter and Space.
  const t = e.target;
  if ((e.key === 'Enter' || e.key === ' ') && t && t.matches && t.matches('[role="button"][data-act]') && t.tagName !== 'BUTTON') {
    e.preventDefault();
    if (ACTIONS[t.dataset.act]) ACTIONS[t.dataset.act](t);
    return;
  }
  // Desktop convenience: type the amount on a hardware keyboard.
  if (ui.tab !== 'add' || e.metaKey || e.ctrlKey || e.altKey) return;
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName || '')) return;
  if (/^\d$/.test(e.key) || e.key === '.') { e.preventDefault(); pressKey(e.key); }
  else if (e.key === 'Backspace') { e.preventDefault(); pressKey('back'); }
});

// Another tab changed the data: reload it.
window.addEventListener('storage', (e) => {
  if (e.key !== null && e.key !== STORAGE_KEY) return;
  if (store.mode !== 'ok') return;
  loadState();
  refreshChips();
  closeSheet();
  if (ui.draft.cardId && !cardById(ui.draft.cardId)) ui.draft.cardId = null;
  if (ui.filters.card && ui.filters.card !== NO_CARD && !cardById(ui.filters.card)) ui.filters.card = null;
  render();
});

// Keep "Today" correct when the app is reopened on a later day, and look for a new version.
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState !== 'visible') return;
  checkForUpdate();
  if (sheet.node) return;
  if (ui.tab === 'history' && document.activeElement && document.activeElement.id === 'h-search') renderHistoryBody();
  else render();
});

/* =====================================================================
   22. Start
   ===================================================================== */
loadState();
refreshChips();
resetDraft();
setKeyboardOverlap(0);
render();
probeDownloads().then(() => { if (ui.tab === 'profile' && !sheet.node) { const b = $('#btn-download'); if (b) b.hidden = !ui.canDownload; } });
registerServiceWorker();
// First launch with nothing saved yet: the three-step welcome.
if (!state.settings.onboarded && state.expenses.length === 0) openWelcome();

})();
