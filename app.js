(function () {
'use strict';

/* =====================================================================
   1. Strings (every user-visible text; English only)
   ===================================================================== */
const STRINGS = {
  appName: 'Daily Spend',
  version: '0.2.4',
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
  saveExpense: 'Save expense',
  missingBoth: 'Enter an amount and choose a category',
  missingAmount: 'Enter an amount',
  missingCategory: 'Choose a category',
  moreChip: 'More',
  moreChipLabel: 'More categories',
  chipLabel: (name) => name,
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
  byGroup: 'By group',
  rangeLabel: 'Time range',
  ranges: { month: 'Month', 3: '3 months', 12: '12 months' },
  monthsCount: (n) => `${n} months`,
  rangeAverage: (amount) => `${amount} a month on average · includes this month so far`,
  monthlyTitle: 'Month by month',
  monthlyLabel: 'Spending by month. Each bar opens that month.',
  soFar: 'so far',
  chartHintRange: 'Tap a slice to open a group, or a bar to see that month.',
  allGroups: '‹ All groups',
  groupShare: (pct, month) => `${pct}% of ${month}`,
  groupItems: (name) => `In ${name}`,
  taxTime: (year) => `Tax time ${year}`,
  taxRows: { medical: 'Medical', donation: 'Donations', childcare: 'Childcare' },
  taxFootnote: "Totals of tagged categories. Only private health plan premiums count; provincial plan premiums don't.",
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
  catGroup: 'Group',
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
  ok: 'OK',
  groupsNoticeTitle: 'Categories updated',
  groupsNotice: 'Categories are now arranged in 8 budget groups. Your entries were moved; nothing was deleted.',
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
  usualLabel: (name) => `${name}, the usual category for this merchant`,
  // History: search and filters
  searchPlaceholder: 'Search merchant or note',
  searchLabel: 'Search expenses by merchant or note',
  filterCategory: 'Category',
  filterCategoryCount: (n) => `Category · ${n}`,
  filterCategoryTitle: 'Filter by category',
  filterWholeGroup: (name) => `Everything in ${name}`,
  filterWholeGroupHint: 'Select the whole group',
  filterCard: 'Card',
  filterCardTitle: 'Card or institution',
  filterWholeInstitution: (name) => `All cards at ${name}`,
  otherCards: 'Other cards',
  selectedCount: (n) => `${n} selected`,
  filterHasLocation: '📍 Has location',
  filterRemovable: (label) => `${label} ×`,
  filterRemove: (label) => `Remove filter: ${label}`,
  cashAndOther: 'Cash & other',
  cashAndOtherHelp: 'Expenses not paid with one of your cards',
  resultCount: (n) => `${n} ${n === 1 ? 'result' : 'results'} across all months`,
  noResults: 'No matching expenses.',
  // Summary: charts and cards
  byCard: 'By card',
  sliceLabel: (name, amount, pct) => `${name}, ${amount}, ${pct}%`,
  barLabel: (day, amount) => `${day}, ${amount}`,
  wholeDollars: (n) => `$${n}`,
  // Pay and "How do you compare?"
  compareButton: '📊 How do you compare?',
  reportTitle: 'How do you compare?',
  paySection: 'Pay',
  payRow: 'Pay for comparison',
  payNotSet: 'Not set',
  payOwn: (amount) => `Your take-home: ${amount} a month`,
  payAbout: (amount) => `about ${amount} a month`,
  payTwoEarners: '2 earners',
  payTitle: 'Your pay',
  payIntro: 'Compare your spending with a typical Canadian budget. Your pay stays on this phone.',
  payGross: 'Your annual pay before tax',
  payGrossSecond: "Second earner's annual pay before tax",
  payAddEarner: 'Add a second earner',
  payRemoveSecond: 'Remove the second earner',
  payProvince: 'Province or territory',
  payChoose: 'Choose…',
  payEstimated: (amount) => `Estimated take-home: ${amount} a month`,
  payUsing: (amount) => `Using your take-home: ${amount} a month`,
  payEstimateHint: 'Enter your pay and province for an estimate.',
  payNoEstimate: "Couldn't estimate here. Enter your monthly take-home instead.",
  payEdit: 'Edit',
  payUseEstimate: 'Use estimate',
  payTakeHome: 'Monthly take-home',
  payError: 'Enter an amount up to $2,000,000',
  payFootnote: 'Estimate for salary at 2026 rates, as on a pay cheque. Ignores RRSP, pension plans, benefits, other income and credits claimed at tax time. Not included in backups.',
  paySeeReport: 'See my report',
  paySkip: 'Skip, compare spending split',
  payRemove: 'Remove pay',
  paySaved: 'Pay saved',
  payRemoved: 'Pay removed',
  rpSlide: (n, of) => `${n} of ${of}`,
  rpBoss: 'Budget boss!',
  rpSharp: 'Looking sharp',
  rpBalanced: 'Nicely balanced',
  rpGrow: 'Room to grow',
  rpScore: (wins, groups) => `At or under typical in ${wins} of ${groups} ${groups === 1 ? 'group' : 'groups'}`,
  rpMonthlyAverage: 'monthly average',
  rpTakeHome: (amount) => `Take-home about ${amount} a month`,
  rpSplitMode: 'Comparing how your spending splits',
  rpAddPay: 'Add your pay',
  rpEditPay: 'Edit pay',
  rpSoFar: 'Includes this month so far.',
  rpNotOver: "The month isn't over yet, so some groups may look low.",
  rpFew: 'Log spending in a few more groups to compare.',
  rpYouLabel: 'You',
  rpTypicalLabel: 'Typical',
  rpYou: (amount, pct) => `You: ${amount} a month (${pct} of take-home)`,
  rpTypical: (amount, pct) => `Typical: ${amount} (${pct})`,
  rpYouShare: (pct, amount) => `You: ${pct}% of your spending (${amount} a month)`,
  rpTypicalShare: (pct) => `Typical: ${pct}%`,
  rpLess: (amount) => `🎉 ${amount} less than typical`,
  rpAtTypical: '🎉 Right at typical',
  rpAtTypicalShare: '🎉 Right at the typical share',
  rpYear: (amount) => `That's about ${amount} a year in your pocket.`,
  rpPointsUnder: (points) => `🎉 ${points} points under the typical share`,
  rpOver: (amount) => `${amount} over typical`,
  rpJustOver: (amount) => `Just over typical, by ${amount}`,
  rpPointsOver: (points) => `${points} points over the typical share`,
  rpTrim: (month, year) => `Trim it by 10% and keep about ${month} a month (${year} a year)`,
  rpSavingsTitle: 'Savings',
  rpLeft: (amount, rate) => `Left after logged spending: ${amount} a month (${rate})`,
  rpTypicalSaves: 'A typical budget saves 8%',
  rpSavingsWin: "Nice work. You're keeping more than a typical budget does.",
  rpSavingsTarget: (amount) => `Saving 8% would mean ${amount} a month`,
  rpSpentMore: (amount) => `You spent ${amount} more than your take-home`,
  rpStartBiggest: 'Start with your biggest group over typical',
  rpOnlyLogged: "Only counts spending you've logged.",
  rpNotLogged: 'Not logged yet',
  rpNotLoggedHint: 'If you pay for these, log them to see the full picture.',
  rpWrapTitle: 'The wrap-up',
  rpBest: (group, line) => `Biggest win: ${group}, ${line.replace('🎉 ', '')}`,
  rpOpp: (group, line) => `Biggest opportunity: ${group}, ${line}`,
  rpFootnote: "Typical shares come from a popular Canadian budgeting template. They're a rough guide, not official statistics.",
  tips: {
    housing: 'Housing is hard to change quickly. Check utility plans and insurance at renewal, and plan ahead for your next move or mortgage renewal.',
    debt: 'Pay the highest-rate balance first, and ask your bank about a lower rate or consolidating.',
    communications: "Phone and internet prices drop often. Ask your provider about a cheaper plan, and cancel subscriptions you don't use.",
    food: 'Plan meals around grocery flyers, and swap one takeout meal a week for cooking at home.',
    transportation: 'Combine errands, keep your tires inflated, and compare car insurance quotes at renewal.',
    recreation: 'Set a monthly fun budget, and look for free local events and library passes.',
    misc: 'Wait 48 hours before non-essential buys, and review recurring fees.',
    insurance: 'Review your coverage once a year, and ask about bundling policies.'
  },
  donutLabel: 'Spending by group. Each slice opens that group.',
  dailyTitle: 'Day by day',
  dailyLabel: 'Spending by day. Each bar opens that day.',
  chartHint: 'Tap a slice to open a group, or a bar to see that day.',
  // Cards
  myCards: 'My cards',
  otherWays: 'Other ways',
  noCards: 'Add the cards you use to see spending by card.',
  addACard: 'Add a card',
  addCardSave: 'Add card',
  confirmCard: 'Confirm card',
  addOwnCard: 'Add your own card',
  editCard: 'Edit card',
  archived: 'Archived',
  archivedSuffix: ' (archived)',
  restoreCard: 'Restore',
  restoreCardLabel: (name) => `Restore ${name}`,
  cardNumberNote: "Only the card's name is stored. Never enter your full card number.",
  cardSearchPlaceholder: 'Search a bank or card',
  cardSearchLabel: 'Search the card list',
  cardKinds: { credit: 'Credit', debit: 'Debit', prepaid: 'Prepaid' },
  cardListLoading: 'Loading the card list…',
  cardListFailed: "The card list couldn't be loaded. You can still add your card yourself.",
  cardNoMatch: 'Nothing matches. You can add your card yourself below.',
  cardNotListed: "My bank or card isn't listed",
  cardNotListedAt: (name) => `Card not listed at ${name}`,
  cardCount: (n) => `${n} ${n === 1 ? 'card' : 'cards'}`,
  cardKindPlural: { credit: 'Credit cards', debit: 'Debit cards', prepaid: 'Other cards' },
  cardsGroup: 'Cards',
  yourInstitutions: 'Your institutions',
  popularInstitutions: 'Popular',
  allInstitutions: 'All institutions',
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
  cardAddedNamed: (name) => `Added ${name}`,
  cardSaved: 'Card saved',
  cardArchived: 'Card archived',
  cardRemoved: 'Card removed',
  cardRestored: 'Card restored',
  // First-run setup
  obStep: (n, of) => `Step ${n} of ${of}`,
  obTitle1: 'Track spending in seconds',
  obBody1: 'Type the amount, tap a category, and it is saved. Everything else is optional.',
  obTitle3: 'Add location to expenses?',
  obBody3: 'Daily Spend can save a pin of where you were with each expense. Turning this on asks for permission.',
  runSetupAgain: 'Run setup again'
};

/* =====================================================================
   2. Constants
   ===================================================================== */
const STORAGE_KEY = 'dailyspend.state';
const V2_BACKUP_KEY = STORAGE_KEY + '.v2-backup';   // the state as it was before the move to budget groups
const LEGACY_KEY = 'dailyspend.v1';          // the v1 test page; read once and migrated
const SCHEMA_VERSION = 3;
const MAX_CENTS = 9999999;
const BOM = '﻿';
const CSV_HEADER = ['id', 'date', 'amount', 'category_group', 'category', 'payment_method', 'card', 'card_last4', 'merchant', 'note', 'tax_tag',
  'latitude', 'longitude', 'location_accuracy_m', 'created_at', 'updated_at'];
const TAX_TAGS = ['medical', 'donation', 'childcare'];
const DEFAULT_EMOJI = '📦';

// The only addresses in the app. The card list and the tax figures are the site's own files.
// The maps address is only ever used as the href of a link the user taps.
const CARDS_URL = 'data/cards-ca.json';
const TAX_DATA_URL = 'data/tax-ca-2026.json';
const TAX_YEAR = 2026;
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

// Categories have two levels. The eight groups are fixed; the items inside them are what
// the user picks. Built-in item ids are "<group id>.<slug of the name>", e.g. food.groceries.
const GROUPS = [
  { id: 'housing', name: 'Housing', emoji: '🏠' },
  { id: 'debt', name: 'Debt Payments', emoji: '💳' },
  { id: 'communications', name: 'Communications', emoji: '📱' },
  { id: 'food', name: 'Food', emoji: '🍽️' },
  { id: 'transportation', name: 'Transportation', emoji: '🚗' },
  { id: 'recreation', name: 'Recreation', emoji: '🎟️' },
  { id: 'misc', name: 'Miscellaneous', emoji: '🧩' },
  { id: 'insurance', name: 'Insurance', emoji: '🛡️' }
];
const DEFAULT_GROUP = 'misc';                 // where custom and unknown items go
const FALLBACK_CATEGORY = 'misc.other';

// [group id, name, emoji, tax tag]
const DEFAULT_ITEMS = [
  ['housing', 'Mortgage / Rent', '🏠', null],
  ['housing', 'Property Taxes', '🏛️', null],
  ['housing', 'Water & Sewage', '🚰', null],
  ['housing', 'Gas & Hydro', '💡', null],
  ['housing', 'Property / Tenant Insurance', '🛡️', null],
  ['housing', 'Home maintenance', '🔧', null],
  ['housing', 'Condo fees', '🏢', null],
  ['housing', 'Other housing', '🏠', null],
  ['debt', 'Card interest & fees', '💳', null],
  ['debt', 'Line of Credit', '🏦', null],
  ['debt', 'Personal Loan', '🤝', null],
  ['debt', 'Student Loan', '🎓', null],
  ['debt', 'Other debt', '💳', null],
  ['communications', 'Cell / Telephone', '📱', null],
  ['communications', 'Television', '📺', null],
  ['communications', 'Internet', '🌐', null],
  ['communications', 'Subscriptions', '🔁', null],
  ['food', 'Groceries', '🛒', null],
  ['food', 'Restaurant / Take-Out', '🍔', null],
  ['transportation', 'Car Loan / Lease Payments', '🚗', null],
  ['transportation', 'Car Insurance', '🛡️', null],
  ['transportation', 'Gas / Diesel', '⛽', null],
  ['transportation', 'Car maintenance', '🔧', null],
  ['transportation', 'Parking', '🅿️', null],
  ['transportation', 'Transit', '🚇', null],
  ['recreation', 'Travel / Vacation', '✈️', null],
  ['recreation', 'Concerts / Sport Events', '🎟️', null],
  ['recreation', 'Club Memberships', '🏋️', null],
  ['recreation', 'Other Entertainment', '🎮', null],
  ['misc', 'Education', '📚', null],
  ['misc', 'Medical', '🩺', 'medical'],
  ['misc', 'Clothing', '👕', null],
  ['misc', 'Gifts', '🎁', null],
  ['misc', 'Donations', '🎗️', 'donation'],
  ['misc', 'Childcare', '🧸', 'childcare'],
  ['misc', 'Shopping', '🛍️', null],
  ['misc', 'Personal Care', '💇', null],
  ['misc', 'Pets', '🐾', null],
  ['misc', 'Fees', '🧾', null],
  ['misc', 'Other', '📦', null],
  ['insurance', 'Life Insurance', '❤️', null],
  ['insurance', 'Disability Insurance', '♿', null],
  ['insurance', 'Critical Illness Insurance', '🏥', null],
  ['insurance', 'Health / Dental Insurance', '🦷', 'medical'],
  ['insurance', 'Other insurance', '🛡️', null]
];
const slugOf = (name) => name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
const CAT_NAME_MAX = 32;

// Chips a new user sees, in order, before any usage.
const DEFAULT_CHIP_IDS = ['food.groceries', 'food.restaurant-take-out', 'transportation.gas-diesel', 'misc.shopping',
  'transportation.transit', 'misc.personal-care', 'misc.medical'];

// The 20 built-in categories of versions 0.1 and 0.2, and the item each one became:
// [old id, old name, old tax tag, new item id]. Used by the migration and by CSV restore.
const OLD_CATEGORIES = [
  ['groceries', 'Groceries', null, 'food.groceries'],
  ['dining', 'Dining & coffee', null, 'food.restaurant-take-out'],
  ['gas', 'Gas & parking', null, 'transportation.gas-diesel'],
  ['transit', 'Transit', null, 'transportation.transit'],
  ['shopping', 'Shopping', null, 'misc.shopping'],
  ['phone', 'Phone & internet', null, 'communications.cell-telephone'],
  ['utilities', 'Hydro & utilities', null, 'housing.gas-hydro'],
  ['housing', 'Rent or mortgage', null, 'housing.mortgage-rent'],
  ['condo', 'Condo fees', null, 'housing.condo-fees'],
  ['propertytax', 'Property tax', null, 'housing.property-taxes'],
  ['car', 'Car costs', null, 'transportation.car-maintenance'],
  ['medical', 'Medical & dental', 'medical', 'misc.medical'],
  ['childcare', 'Childcare', 'childcare', 'misc.childcare'],
  ['donations', 'Donations', 'donation', 'misc.donations'],
  ['subscriptions', 'Subscriptions', null, 'communications.subscriptions'],
  ['entertainment', 'Entertainment', null, 'recreation.other-entertainment'],
  ['travel', 'Travel', null, 'recreation.travel-vacation'],
  ['personalcare', 'Personal care', null, 'misc.personal-care'],
  ['gifts', 'Gifts', null, 'misc.gifts'],
  ['other', 'Other', null, 'misc.other']
];

const PROVINCES = {
  AB: 'Alberta', BC: 'British Columbia', MB: 'Manitoba', NB: 'New Brunswick', NL: 'Newfoundland and Labrador', NS: 'Nova Scotia',
  NT: 'Northwest Territories', NU: 'Nunavut', ON: 'Ontario', PE: 'Prince Edward Island', QC: 'Quebec', SK: 'Saskatchewan', YT: 'Yukon'
};
const PROVINCE_CODES = Object.keys(PROVINCES);

// Institutions listed first in the card picker, by their id in the card list.
const POPULAR_ISSUER_IDS = ['rbc', 'td', 'scotiabank', 'bmo', 'cibc', 'national-bank', 'desjardins', 'amex'];
const BADGE_COLOURS = 12;                     // .ib-0 to .ib-11 in styles.css

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

// "Delete all" means all: unreadable copies, the old v1 key and the pre-groups backup go too.
function removeLeftovers() {
  try {
    const ls = storageHandle();
    const doomed = [];
    for (let i = 0; i < ls.length; i++) {
      const k = ls.key(i);
      if (k && (k.indexOf(STORAGE_KEY + '.corrupt.') === 0 || k.indexOf(LEGACY_KEY) === 0 || k === V2_BACKUP_KEY)) doomed.push(k);
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
  return DEFAULT_ITEMS.map((c, i) => ({
    id: c[0] + '.' + slugOf(c[1]), groupId: c[0], name: c[1], emoji: c[2], taxTag: c[3], hidden: false, builtIn: true, order: i + 1
  }));
}

function defaultSettings() {
  return {
    lastPayment: { methodId: DEFAULT_PAYMENT, cardId: null },
    testNoticeDismissed: false,
    autoLocation: false,
    mapsNoticeShown: false,
    onboarded: false,
    groupsNotice: false,            // true until the one-time "categories were rearranged" notice has been seen
    pay: null,                      // pay for "How do you compare?"; see cleanPay(). Never in the CSV backup
    paySkipped: false               // the user chose to compare the spending split instead
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

// Version 2 to 3: the 20 flat categories become items in 8 budget groups. Every expense keeps
// its amount, date and details; only its category id changes, by the table in OLD_CATEGORIES.
MIGRATIONS[2] = (old) => {
  const items = defaultCategories();
  const byId = new Map(items.map((c) => [c.id, c]));
  const table = new Map(OLD_CATEGORIES.map((o) => [o[0], o]));
  const sameName = (a, b) => a.trim().toLowerCase() === b.trim().toLowerCase();
  const idMap = new Map(OLD_CATEGORIES.map((o) => [o[0], o[3]]));
  const custom = [];
  const oldCats = (Array.isArray(old.categories) ? old.categories : []).filter((c) => c && typeof c.id === 'string');
  // Built-ins first: a hidden one stays hidden, a renamed one keeps the user's name, a changed tax tag is kept.
  oldCats.forEach((raw) => {
    const was = table.get(raw.id);
    if (!was) return;
    const item = byId.get(was[3]);
    if (raw.hidden === true) item.hidden = true;
    const tag = TAX_TAGS.indexOf(raw.taxTag) !== -1 ? raw.taxTag : null;
    if (tag !== was[2]) item.taxTag = tag;
    const name = typeof raw.name === 'string' ? raw.name.trim() : '';
    if (name && name !== was[1] && !items.some((c) => c !== item && sameName(c.name, name))) item.name = name;
  });
  // The user's own categories move to Miscellaneous. One whose name is now a built-in item merges into it.
  oldCats.forEach((raw) => {
    if (table.has(raw.id) || typeof raw.name !== 'string' || !raw.name.trim()) return;
    const twin = items.concat(custom).find((c) => sameName(c.name, raw.name));
    if (twin) {
      idMap.set(raw.id, twin.id);
      if (!twin.taxTag && TAX_TAGS.indexOf(raw.taxTag) !== -1) twin.taxTag = raw.taxTag;
      return;
    }
    custom.push(Object.assign({}, raw, { groupId: DEFAULT_GROUP, builtIn: false }));
  });
  const expenses = (Array.isArray(old.expenses) ? old.expenses : []).map((e) =>
    (e && typeof e === 'object' && idMap.has(e.categoryId) ? Object.assign({}, e, { categoryId: idMap.get(e.categoryId) }) : e));
  const settings = Object.assign({}, old.settings && typeof old.settings === 'object' ? old.settings : {}, { groupsNotice: expenses.length > 0 });
  return { schemaVersion: 3, expenses, categories: items.concat(custom), cards: old.cards, settings };
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

const isGroupId = (id) => GROUPS.some((g) => g.id === id);
const isPaymentId = (id) => PAYMENT_METHODS.some((p) => p.id === id);
const str = (v, max) => (typeof v === 'string' ? v.slice(0, max) : '');
const round5 = (n) => Math.round(n * 1e5) / 1e5;
const isLast4 = (v) => typeof v === 'string' && /^\d{4}$/.test(v);

// settings.pay: gross pay in cents for one or two earners plus a province, and/or the user's own
// monthly take-home. Anything invalid is dropped; with nothing usable left the result is null.
function cleanPay(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const ok = (c) => Number.isInteger(c) && c >= 100 && c <= 200000000;
  const province = PROVINCE_CODES.indexOf(raw.province) !== -1 ? raw.province : null;
  let earners = (Array.isArray(raw.earners) ? raw.earners : []).filter(ok).slice(0, 2);
  if (!province) earners = [];
  const override = ok(raw.takeHomeOverrideCents) ? raw.takeHomeOverrideCents : null;
  if (!earners.length && override === null) return null;
  return {
    earners,
    province: earners.length ? province : null,
    takeHomeOverrideCents: override,
    taxYear: Number.isInteger(raw.taxYear) ? raw.taxYear : TAX_YEAR,
    updatedAt: typeof raw.updatedAt === 'string' ? raw.updatedAt : nowIso()
  };
}

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
      if (isGroupId(raw.groupId)) known.groupId = raw.groupId;
    } else {
      order += 1;
      const cat = { id: raw.id, groupId: isGroupId(raw.groupId) ? raw.groupId : DEFAULT_GROUP, name: raw.name, emoji, taxTag: tag,
        hidden: raw.hidden === true, builtIn: false, order };
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
      categoryId: ids.has(raw.categoryId) ? raw.categoryId : FALLBACK_CATEGORY,
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
      onboarded: s.onboarded === true,
      groupsNotice: s.groupsNotice === true,
      pay: cleanPay(s.pay),
      paySkipped: s.paySkipped === true
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
  let parsed = null, upgraded = false;
  try {
    const data = JSON.parse(raw);
    if (data && typeof data === 'object' && !Array.isArray(data)) {
      upgraded = data.schemaVersion !== SCHEMA_VERSION;
      // Before categories are regrouped, keep the version 2 state exactly as it was.
      if (data.schemaVersion === 2 && !fromLegacy) {
        try { storageHandle().setItem(V2_BACKUP_KEY, raw); } catch (e) { /* the migration still goes ahead */ }
      }
      parsed = migrate(data);
    }
  } catch (e) { parsed = null; }
  if (!parsed) {
    store.corrupt = keepCorruptCopy(raw) ? 'kept' : 'lost';
    state = defaultState();
    saveState();
    return;
  }
  state = validateState(parsed);
  if (fromLegacy || upgraded) saveState();   // the old v1 key is left untouched as a safety copy
}

const catById = (id) => state.categories.find((c) => c.id === id) ||
  { id, groupId: DEFAULT_GROUP, name: 'Other', emoji: DEFAULT_EMOJI, taxTag: null, hidden: true, builtIn: false, order: 9999 };
const groupById = (id) => GROUPS.find((g) => g.id === id) || GROUPS.find((g) => g.id === DEFAULT_GROUP);
const groupOfCat = (cat) => groupById(cat.groupId);
// [{ group, items }] in group order, items in their own order; groups with nothing to show are left out.
function itemsByGroup(includeHidden) {
  return GROUPS.map((group) => ({
    group,
    items: state.categories.filter((c) => c.groupId === group.id && (includeHidden || !c.hidden)).sort((a, b) => a.order - b.order)
  })).filter((g) => g.items.length);
}
const payById = (id) => PAYMENT_METHODS.find((p) => p.id === id) || PAYMENT_METHODS[PAYMENT_METHODS.length - 1];
const sumCents = (list) => list.reduce((total, e) => total + e.amountCents, 0);
const expensesInMonth = (m) => { const p = monthPrefix(m); return state.expenses.filter((e) => e.date.slice(0, 7) === p); };
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

// Seven most used visible items over the last 90 days. Ties, and a new user's chips, follow
// DEFAULT_CHIP_IDS first and then the item order.
function rankTopCategories() {
  const since = daysAgoStr(90);
  const counts = new Map();
  state.expenses.forEach((e) => { if (e.date >= since) counts.set(e.categoryId, (counts.get(e.categoryId) || 0) + 1); });
  const pref = (c) => { const i = DEFAULT_CHIP_IDS.indexOf(c.id); return i === -1 ? 1000 + c.order : i; };
  return state.categories
    .filter((c) => !c.hidden)
    .sort((a, b) => (counts.get(b.id) || 0) - (counts.get(a.id) || 0) || pref(a) - pref(b))
    .slice(0, 7);
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
// cards: card ids and/or NO_CARD. range: { from: 'YYYY-MM', to: 'YYYY-MM' }, set from Summary's 3 and 12 month views.
function emptyFilters() { return { text: '', cats: [], cards: [], hasLocation: false, day: null, month: null, range: null }; }

function filtersActive(f) {
  return !!(f.text.trim() || f.cats.length || f.cards.length || f.hasLocation || f.day || f.month || f.range);
}

function filterExpenses(f) {
  const q = fold(f.text.trim());
  const cats = new Set(f.cats);
  const cards = new Set(f.cards);
  const month = f.month ? monthPrefix(f.month) : null;
  return state.expenses.filter((e) => {
    if (q && fold(e.merchant + ' ' + e.note).indexOf(q) === -1) return false;
    if (cats.size && !cats.has(e.categoryId)) return false;
    if (cards.size && !cards.has(e.cardId || NO_CARD)) return false;
    if (f.range && (e.date.slice(0, 7) < f.range.from || e.date.slice(0, 7) > f.range.to)) return false;
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
      e.id, e.date, centsToPlain(e.amountCents), formulaSafe(groupOfCat(cat).name), formulaSafe(cat.name), payById(e.paymentMethodId).label,
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

// Finds the item a backup row means, trying in order: group plus name, name alone, then the
// old default names of versions 0.1 and 0.2 ("Dining & coffee" is now Restaurant / Take-Out).
function findCategoryForCsv(groupName, name) {
  const key = name.trim().toLowerCase(), group = groupName.trim().toLowerCase();
  const named = state.categories.filter((c) => c.name.trim().toLowerCase() === key);
  if (group) {
    const exact = named.find((c) => groupOfCat(c).name.toLowerCase() === group);
    if (exact) return exact;
  }
  if (named.length) return named[0];
  const old = OLD_CATEGORIES.find((o) => o[1].toLowerCase() === key);
  return (old && state.categories.find((c) => c.id === old[3])) || null;
}

function createCategory(name, emoji, taxTag, groupId) {
  const order = state.categories.reduce((max, c) => Math.max(max, c.order), 0) + 1;
  const cat = { id: 'c_' + newId(), groupId: isGroupId(groupId) ? groupId : DEFAULT_GROUP, name, emoji, taxTag, hidden: false, builtIn: false, order };
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

// Merges a backup (v1, v2 or v3 columns) into the current state. Never overwrites an existing expense.
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
    let cat = findCategoryForCsv(formulaUnsafe(cell(r, 'category_group').trim()), catName);
    if (!cat) {
      const tag = cell(r, 'tax_tag').trim().toLowerCase();
      // A new item goes to the group the backup names, or to Miscellaneous when it names none we know.
      const groupName = formulaUnsafe(cell(r, 'category_group').trim()).trim().toLowerCase();
      const group = GROUPS.find((g) => g.name.toLowerCase() === groupName);
      cat = createCategory(catName, DEFAULT_EMOJI, TAX_TAGS.indexOf(tag) !== -1 ? tag : null, group ? group.id : DEFAULT_GROUP);
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
  range: 'month',             // Summary time range: 'month', '3' or '12'; lasts for the session
  summaryGroup: null,         // group opened inside Summary, or null for the overview
  openGroups: new Set(),      // groups expanded in the By group list
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
  ui.draft = { date: null, categoryId: null, paymentMethodId: pay.methodId, cardId: pay.cardId, merchant: '', note: '', location: null };
}
const draftDate = () => ui.draft.date || todayStr();

const el = {
  app: $('#app'), title: $('#title'), banners: $('#banners'), view: $('#view'),
  tabbar: $('#tabbar'), sheetRoot: $('#sheet-root'), reportRoot: $('#report-root'), fx: $('#fx-layer'), toast: $('#toast-region')
};

/* =====================================================================
   10. Toast
   ===================================================================== */
/* Motion never delays a state change and never blocks input. Anything on its way out, and every
   burst or confetti, is a non-interactive node in #fx-layer. All of it is skipped when the
   person has asked for reduced motion (checked at the moment the motion would start). */
function motionOK() {
  try { return !window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; }
}
function fxAdd(node, ms) {
  el.fx.appendChild(node);
  setTimeout(() => node.remove(), ms);
  return node;
}
function fxClear() { el.fx.textContent = ''; }

let toastTimer = null, toastOutTimer = null;

// Removes the toast at once (Undo, or a newer toast taking its place).
function hideToast() {
  clearTimeout(toastTimer);
  clearTimeout(toastOutTimer);
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
  const ms = opts.ms || 3000;
  toastTimer = setTimeout(hideToast, ms);
  // It slides up and fades over its last 160 ms, so it is gone exactly when its time is up.
  if (motionOK()) toastOutTimer = setTimeout(() => box.classList.add('out'), ms - 160);
}
const undoToastShowing = () => !!$('.toast-undo', el.toast);

/* =====================================================================
   11. Sheets (in-page dialogs; no browser dialogs anywhere)
   ===================================================================== */
const sheet = { node: null, opener: null, dismissible: true, onClose: null, back: null };

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

// A constructed copy of the app's stylesheet, for the closed shadow root that draws a closing sheet.
let exitStyles = null;
function exitStyleSheet() {
  if (exitStyles !== null) return exitStyles;
  exitStyles = false;
  try {
    const own = Array.from(document.styleSheets).find((sh) => sh.href && /styles\.css(\?|$)/.test(sh.href));
    const copy = new CSSStyleSheet();
    copy.replaceSync(Array.from(own.cssRules).map((rule) => rule.cssText).join('\n'));
    exitStyles = copy;
  } catch (e) { /* no exit animation in this browser; closing is simply instant */ }
  return exitStyles;
}

// Draws the sheet that is closing: a copy in #fx-layer that slides down and fades. The copy sits
// in a closed shadow root, so it can never be focused, clicked or found by id, and it is removed
// when its animation ends, or at once when another sheet or the report opens.
function drawSheetExit() {
  if (!motionOK()) return;
  const styles = exitStyleSheet();
  if (!styles) return;
  try {
    const host = document.createElement('div');
    host.className = 'fx-ghost';
    const root = host.attachShadow({ mode: 'closed' });
    root.adoptedStyleSheets = [styles];
    const copy = el.sheetRoot.cloneNode(true);
    copy.classList.add('exit');
    root.appendChild(copy);
    const from = $('.sheet-body', el.sheetRoot), to = copy.querySelector('.sheet-body');
    fxAdd(host, 200);
    if (from && to) to.scrollTop = from.scrollTop;
  } catch (e) { /* purely decorative */ }
}

// options: { dismissible, onClose, back, slide, cls, bodyCls, focusTitle }.
// Opening a sheet over another replaces it in place (no second rise, and without running the
// first sheet's onClose). `back` adds a back arrow and makes Escape go up a level;
// `slide` ('fwd' or 'back') slides the new content in.
function openSheet(title, bodyHtml, options) {
  const opts = options || {};
  fxClear();                                   // a sheet still sliding away makes room at once
  const replacing = !!sheet.node;
  const opener = replacing ? sheet.opener : document.activeElement;
  const back = typeof opts.back === 'function' ? opts.back : null;
  const still = replacing ? ' still' : '';
  el.sheetRoot.innerHTML =
    `<div class="backdrop${still}" data-sheet-backdrop></div>
     <div class="sheet${still}${opts.cls ? ' ' + opts.cls : ''}" role="dialog" aria-modal="true" aria-labelledby="sheet-title" tabindex="-1">
       <div class="sheet-head${back ? ' has-back' : ''}">
         ${back ? `<button type="button" class="icon-btn back-btn" data-sheet-back aria-label="${esc(STRINGS.back)}">‹</button>` : ''}
         <h2 id="sheet-title" tabindex="-1">${esc(title)}</h2>
         <button type="button" class="icon-btn" data-sheet-close aria-label="${esc(STRINGS.close)}">×</button>
       </div>
       <div class="sheet-body${opts.bodyCls ? ' ' + opts.bodyCls : ''}${opts.slide ? ' slide-' + opts.slide : ''}">${bodyHtml}</div>
     </div>`;
  el.sheetRoot.hidden = false;
  sheet.node = $('.sheet', el.sheetRoot);
  sheet.opener = opener;
  sheet.dismissible = opts.dismissible !== false;
  sheet.onClose = typeof opts.onClose === 'function' ? opts.onClose : null;
  sheet.back = back;
  ui.locRefresh = null;
  el.app.inert = true;
  el.app.setAttribute('aria-hidden', 'true');
  watchKeyboard(true);
  (opts.focusTitle ? $('#sheet-title', sheet.node) : sheet.node).focus({ preventScroll: true });
  return sheet.node;
}

function closeSheet() {
  if (!sheet.node) return;
  const opener = sheet.opener;
  const onClose = sheet.onClose;
  sheet.node = null;
  sheet.opener = null;
  sheet.onClose = null;
  sheet.back = null;
  ui.locRefresh = null;
  drawSheetExit();                             // decoration only: everything below happens at once
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
  if (e.target.closest('[data-sheet-back]')) { if (sheet.back) sheet.back(); return; }
  if (e.target.closest('[data-sheet-close]')) { closeSheet(); return; }
  if (e.target.closest('[data-sheet-backdrop]') && sheet.dismissible) closeSheet();
});

function focusables(root) {
  return $$('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])', root)
    .filter((n) => !n.disabled && n.offsetParent !== null);
}

function trapFocus(e) { trapFocusIn(sheet.node, e); }
function trapFocusIn(box, e) {
  const items = focusables(box);
  if (!items.length) { e.preventDefault(); return; }
  const first = items[0], last = items[items.length - 1], active = document.activeElement;
  if (!box.contains(active) || active === box || items.indexOf(active) === -1) {
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
const sw = { reg: null, updateReady: false, reloading: false };   // service worker, see section 21

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
  ui.summaryGroup = null;
  ui.drawCharts = tab === 'summary';
  render();
  el.view.scrollTop = 0;
  el.view.classList.remove('view-in');         // the new view fades in with a small lift
  void el.view.offsetWidth;
  el.view.classList.add('view-in');
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

// A chip shows the item's emoji and name, and selects that category (it does not save).
// `caption` adds the group in small text, for chips that could be mistaken for each other.
function chipHtml(cat, selected, caption) {
  return `<button type="button" class="chip${caption ? ' has-caption' : ''}${selected ? ' selected' : ''}" data-act="chip" data-cat="${esc(cat.id)}" aria-pressed="${selected}"
    aria-label="${esc(STRINGS.chipLabel(caption ? cat.name + ', ' + caption : cat.name))}">
    <span class="chip-emoji" aria-hidden="true">${esc(cat.emoji)}</span><span class="chip-name">${esc(cat.name)}</span>${
    caption ? `<span class="chip-group">${esc(caption)}</span>` : ''}${selected ? '<span class="chip-check" aria-hidden="true">✓</span>' : ''}</button>`;
}

// Two visible chips can be confused when their names start with the same word but they sit in
// different groups ("Gas / Diesel" and "Gas & Hydro"). Those chips get their group as a caption.
function chipCaptions(cats) {
  const first = (c) => fold(c.name).split(/[^a-z0-9]+/).filter(Boolean)[0] || '';
  const out = new Map();
  cats.forEach((c) => {
    if (cats.some((o) => o !== c && o.groupId !== c.groupId && first(o) === first(c))) out.set(c.id, groupOfCat(c).name);
  });
  return out;
}

function detailsRowHtml() {
  const d = ui.draft;
  const pin = d.location ? STRINGS.sep + STRINGS.pin : ui.capture ? STRINGS.sep + STRINGS.pinFinding : '';
  const main = dayLabel(draftDate()) + STRINGS.sep + paymentLabel(d.paymentMethodId, d.cardId) + pin;
  const sub = [d.merchant, d.note].filter(Boolean).join(STRINGS.sep) || STRINGS.addMerchantOrNote;
  return `<span class="details-text"><span class="details-main">${esc(main)}</span><span class="details-sub">${esc(sub)}</span></span>${ICONS.chev}`;
}

// "Usual: 🍔 Restaurant / Take-Out" for a merchant seen before. Tapping it selects, like a chip.
function usualPillHtml() {
  const cat = usualCategoryFor(ui.draft.merchant);
  if (!cat) return '';
  return `<button type="button" class="usual-pill" id="usual-pill" data-act="usual" data-cat="${esc(cat.id)}" aria-pressed="${cat.id === ui.draft.categoryId}"
    aria-label="${esc(STRINGS.usualLabel(cat.name))}"><span>${esc(STRINGS.usual(cat.emoji, cat.name))}</span></button>`;
}
function refreshUsual() {
  const slot = $('#usual-slot');
  if (slot) slot.innerHTML = usualPillHtml();
}

// The seven chips of this session. A category picked elsewhere (More, Usual) that is not among
// them borrows the seventh slot for this entry only; the frozen order returns afterwards.
function visibleChips() {
  const top = topCategories();
  const picked = ui.draft.categoryId ? state.categories.find((c) => c.id === ui.draft.categoryId && !c.hidden) : null;
  if (picked && !top.some((c) => c.id === picked.id)) {
    if (top.length >= 7) top[6] = picked; else top.push(picked);
  }
  return top;
}

function chipsHtml() {
  const top = visibleChips(), captions = chipCaptions(top);
  return top.map((c) => chipHtml(c, c.id === ui.draft.categoryId, captions.get(c.id))).join('') +
    `<button type="button" class="chip chip-more" data-act="chip-more" aria-label="${esc(STRINGS.moreChipLabel)}">
       <span class="chip-emoji" aria-hidden="true">···</span><span class="chip-name">${esc(STRINGS.moreChip)}</span></button>`;
}

VIEWS.add = function renderAdd() {
  // a selected category that has since been hidden or removed is dropped
  if (ui.draft.categoryId && !state.categories.some((c) => c.id === ui.draft.categoryId && !c.hidden)) ui.draft.categoryId = null;
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
       </div>
       <div class="details-line">
         <button type="button" class="details-row" id="details-row" data-act="details" aria-label="${esc(STRINGS.detailsRowLabel)}">${detailsRowHtml()}</button>
         ${recent}
       </div>
       <div id="usual-slot">${usualPillHtml()}</div>
       <div class="chips" id="chips">${chipsHtml()}</div>
       <div class="keypad" id="keypad">${keys}</div>
       <p class="save-hint" id="save-hint" role="status"></p>
       <button type="button" class="save-btn" id="btn-save" data-act="save" aria-disabled="true">${esc(STRINGS.saveExpense)}</button>
     </section>`;
  updateAmount();
  bindBackspace($('[data-key="back"]', el.view));
};

// The two required fields. Everything else on the Add screen is optional.
function missingFields() {
  return { amount: typedToCents(ui.amount) <= 0, category: !ui.draft.categoryId };
}

// Red outlines on what is missing, the hint line, and the Save button: grey until ready, then green.
function updateSaveState() {
  const missing = missingFields();
  const amount = $('#amount'), chips = $('#chips'), btn = $('#btn-save'), hint = $('#save-hint');
  if (!amount || !chips || !btn || !hint) return;
  amount.classList.toggle('missing', missing.amount);
  chips.classList.toggle('missing', missing.category);
  const ready = !missing.amount && !missing.category;
  const was = btn.classList.contains('ready');
  btn.setAttribute('aria-disabled', String(!ready));
  btn.classList.toggle('ready', ready);
  btn.classList.toggle('pop', ready && (!was || btn.classList.contains('pop')));      // a small pop when it turns ready
  hint.textContent = ready ? '' : missing.amount && missing.category ? STRINGS.missingBoth
    : missing.amount ? STRINGS.missingAmount : STRINGS.missingCategory;
}

// Chips and the Usual pill toggle; the More sheet always sets.
function selectCategory(id, toggle) {
  ui.draft.categoryId = toggle && ui.draft.categoryId === id ? null : id;
  const chips = $('#chips');
  if (chips) chips.innerHTML = chipsHtml();
  const picked = $('#chips .chip.selected');
  if (picked) picked.classList.add('pop');
  refreshUsual();
  updateSaveState();
}

// A ring and a few dots from the Save button, drawn in #fx-layer. The form has already reset.
function saveBurst() {
  const btn = $('#btn-save');
  if (!btn || !motionOK()) return;
  const box = btn.getBoundingClientRect();
  const burst = document.createElement('div');
  burst.className = 'fx-burst';
  burst.style.left = (box.left + box.width / 2) + 'px';
  burst.style.top = (box.top + box.height / 2) + 'px';
  let dots = '<b></b>';
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    dots += `<i style="--dx:${Math.round(Math.cos(a) * 70)}px;--dy:${Math.round(Math.sin(a) * 34)}px"></i>`;
  }
  burst.innerHTML = dots;
  fxAdd(burst, 420);
}

function updateAmount() {
  const node = $('#amount');
  if (!node) return;
  const text = fmtTyped(ui.amount);
  const zero = typedToCents(ui.amount) <= 0;
  node.textContent = text;
  node.setAttribute('aria-label', STRINGS.amountLabel(text));
  node.classList.toggle('is-zero', zero);
  updateSaveState();
}

function shake(node) {
  if (!node) return;
  node.classList.remove('shake');
  void node.offsetWidth;
  node.classList.add('shake');
}
const shakeAmount = () => shake($('#amount'));

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

// The standard "Saved" toast with Undo, shared by every way of logging an expense.
function announceSaved(expense) {
  const day = expense.date === todayStr() ? '' : dayLabel(expense.date);
  showToast(STRINGS.saved(fmtMoney(expense.amountCents), catById(expense.categoryId).name, day), {
    ms: 5000,
    check: true,
    onUndo: () => { deleteExpense(expense.id); render(); showToast(STRINGS.undone, { ms: 2000 }); }
  });
}

// The Save button. Not ready: the missing fields shake and nothing is saved. Ready: the expense
// is saved, the toast offers Undo, and the form starts again (the payment choice stays).
function saveDraft() {
  const missing = missingFields();
  if (missing.amount || missing.category) {
    $$('#amount, #chips').forEach((n) => n.classList.remove('shake'));     // only what is missing now shakes
    if (missing.amount) shakeAmount();
    if (missing.category) shake($('#chips'));
    return;
  }
  const d = ui.draft;
  const expense = addExpense({
    amountCents: typedToCents(ui.amount),
    date: draftDate(),
    categoryId: d.categoryId,
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
  saveBurst();
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

const groupHeadHtml = (group) =>
  `<p class="group-head" data-group="${group.id}"><span aria-hidden="true">${esc(group.emoji)}</span> ${esc(group.name)}</p>`;

// The More sheet: every visible item under its group heading. Picking one selects it and closes the sheet.
function openAllCategoriesSheet() {
  const rows = itemsByGroup(false).map(({ group, items }) => groupHeadHtml(group) + items.map((c) =>
    `<button type="button" class="row" data-pick="${esc(c.id)}" aria-pressed="${c.id === ui.draft.categoryId}">
       <span class="row-emoji" aria-hidden="true">${esc(c.emoji)}</span>
       <span class="row-text"><span class="row-title">${esc(c.name)}</span></span>${tagBadge(c)}</button>`).join('')).join('');
  const node = openSheet(STRINGS.allCategoriesTitle, `<div class="sheet-list" id="all-categories">${rows}</div>`);
  node.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-pick]');
    if (!btn) return;
    closeSheet();
    selectCategory(btn.dataset.pick, false);       // selects; the Save button saves
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
  const option = (value, label, card) =>
    `<label class="option"><input type="radio" name="${name}" value="${esc(value)}"${value === selected ? ' checked' : ''}>
       <span>${card ? cardBadgeHtml(card) : ''}${esc(label)}</span></label>`;
  const cards = activeCards();
  const others = PAYMENT_METHODS.map((p) => option(payValue(p.id, null), methodLabel(p.id), null)).join('');
  if (!cards.length) return `<div class="options" data-group="other">${others}</div>`;
  return `<p class="group-label">${esc(STRINGS.myCards)}</p>
    <div class="options" data-group="cards">${cards.map((c) => option(payValue(c.kind, c.id), cardShortLabel(c), c)).join('')}</div>
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
  const sub = [e.merchant, e.note].filter(Boolean).join(STRINGS.sep) || groupOfCat(cat).name;   // the group, where there is room
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
  else if (f.cats.length > 1) {
    // a whole group, and nothing else, reads as the group's name
    const whole = GROUPS.find((g) => {
      const ids = state.categories.filter((c) => c.groupId === g.id).map((c) => c.id);
      return ids.length === f.cats.length && ids.every((id) => f.cats.indexOf(id) !== -1);
    });
    catLabel = whole ? whole.name : STRINGS.filterCategoryCount(f.cats.length);
  }
  const cardLabel = cardFilterLabel(f.cards);
  const parts = [
    chip('f-category', 'filter-category', catLabel, f.cats.length > 0),
    chip('f-card', 'filter-card', cardLabel, f.cards.length > 0),
    chip('f-loc', 'filter-loc', STRINGS.filterHasLocation, f.hasLocation)
  ];
  if (f.day) parts.push(chip('f-day', 'filter-day-clear', STRINGS.filterRemovable(dayLabel(f.day)), true, ` aria-label="${esc(STRINGS.filterRemove(dayLabel(f.day)))}"`));
  if (f.month) parts.push(chip('f-month', 'filter-month-clear', STRINGS.filterRemovable(monthLabel(f.month)), true, ` aria-label="${esc(STRINGS.filterRemove(monthLabel(f.month)))}"`));
  if (f.range) {
    const label = rangeLabelOf(f.range.from, f.range.to);
    parts.push(chip('f-range', 'filter-range-clear', STRINGS.filterRemovable(label), true, ` aria-label="${esc(STRINGS.filterRemove(label))}"`));
  }
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

// A filter chip was added or removed: the first rows slide in. (Not while typing in search.)
function slideRowsIn() {
  $$('#h-body .swipe').slice(0, 12).forEach((row, i) => {
    row.style.animationDelay = (i * 20) + 'ms';
    row.classList.add('row-in');
  });
}

function setFilter(patch) {
  Object.assign(ui.filters, patch);
  renderHistoryBody();
  slideRowsIn();
}

function clearFilters() {
  ui.filters = emptyFilters();
  const box = $('#h-search');
  if (box) box.value = '';
  renderHistoryBody();
  slideRowsIn();
}

// Multi-select, grouped. Each group heading has a box that selects or clears the whole group.
function openCategoryFilterSheet() {
  const picked = new Set(ui.filters.cats);
  const rows = itemsByGroup(true).map(({ group, items }) =>
    `<label class="row check-row group-check"><input type="checkbox" data-group="${group.id}" aria-label="${esc(STRINGS.filterWholeGroup(group.name))}">
       <span class="row-text"><span class="row-title"><span aria-hidden="true">${esc(group.emoji)}</span> ${esc(group.name)}</span>
         <span class="row-sub">${esc(STRINGS.filterWholeGroupHint)}</span></span></label>` +
    items.map((c) =>
      `<label class="row check-row item-check"><input type="checkbox" data-item="${group.id}" value="${esc(c.id)}"${picked.has(c.id) ? ' checked' : ''}>
         <span class="row-emoji" aria-hidden="true">${esc(c.emoji)}</span>
         <span class="row-text"><span class="row-title">${esc(c.name + (c.hidden ? STRINGS.hiddenSuffix : ''))}</span></span></label>`).join('')).join('');
  const node = openSheet(STRINGS.filterCategoryTitle,
    `<div class="sheet-list" id="fc-list">${rows}</div>
     <div class="btn-row sticky-actions">
       <button type="button" class="btn" id="fc-none">${esc(STRINGS.clear)}</button>
       <button type="button" class="btn primary" id="fc-done">${esc(STRINGS.done)}</button>
     </div>`);
  const syncGroups = () => $$('#fc-list input[data-group]', node).forEach((box) => {
    const items = $$(`#fc-list input[data-item="${box.dataset.group}"]`, node);
    const on = items.filter((n) => n.checked).length;
    box.checked = on > 0 && on === items.length;
    box.indeterminate = on > 0 && on < items.length;
  });
  const apply = () => { syncGroups(); setFilter({ cats: $$('#fc-list input[data-item]:checked', node).map((n) => n.value) }); };
  syncGroups();
  $('#fc-list', node).addEventListener('change', (e) => {
    const group = e.target.dataset.group;
    if (group) $$(`#fc-list input[data-item="${group}"]`, node).forEach((n) => { n.checked = e.target.checked; });
    apply();
  });
  $('#fc-none', node).addEventListener('click', () => { $$('#fc-list input', node).forEach((n) => { n.checked = false; }); apply(); });
  $('#fc-done', node).addEventListener('click', closeSheet);
}

// The user's cards grouped by institution: [{ key, name, cards }]. Cards added by hand group under
// the issuer as typed (case ignored); cards with no issuer go under "Other cards", listed last.
function userInstitutions() {
  const byKey = new Map();
  state.cards.forEach((c) => {
    const typed = c.issuer.trim();
    const key = typed ? fold(typed) : '';
    if (!byKey.has(key)) byKey.set(key, { key, name: typed || STRINGS.otherCards, cards: [] });
    byKey.get(key).cards.push(c);
  });
  const cmp = (a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' });
  const list = Array.from(byKey.values()).sort((a, b) => (a.key === '') - (b.key === '') || cmp(a.name, b.name));
  list.forEach((inst) => inst.cards.sort((a, b) => (a.archived - b.archived) || cmp(cardDisplayName(a), cardDisplayName(b))));
  return list;
}

// One institution (two or more cards, all selected) reads as its name; one card as the card's
// name; cash alone as "Cash & other"; anything more as "3 selected".
function cardFilterLabel(selected) {
  if (!selected.length) return STRINGS.filterCard;
  if (selected.length === 1) {
    if (selected[0] === NO_CARD) return STRINGS.cashAndOther;
    const card = cardById(selected[0]);
    return card ? cardDisplayName(card) : STRINGS.filterCard;
  }
  const whole = userInstitutions().find((inst) =>
    inst.cards.length === selected.length && inst.cards.every((c) => selected.indexOf(c.id) !== -1));
  return whole ? whole.name : STRINGS.selectedCount(selected.length);
}

// Card or institution: multi-select. An institution's box selects all of its cards (archived
// ones too); single cards narrow it; "Cash & other" is every expense with no card.
function openCardFilterSheet() {
  const picked = new Set(ui.filters.cards);
  const rows = userInstitutions().map((inst) =>
    `<label class="row check-row group-check"><input type="checkbox" data-inst="${esc(inst.key)}" aria-label="${esc(STRINGS.filterWholeInstitution(inst.name))}">
       ${cardBadgeHtml(inst.cards[0])}<span class="row-text"><span class="row-title">${esc(inst.name)}</span>
         <span class="row-sub">${esc(STRINGS.cardCount(inst.cards.length))}</span></span></label>` +
    inst.cards.map((c) =>
      `<label class="row check-row item-check"><input type="checkbox" data-card="${esc(inst.key)}" value="${esc(c.id)}"${picked.has(c.id) ? ' checked' : ''}>
         <i class="card-dot sw-${c.colour}" aria-hidden="true"></i>
         <span class="row-text"><span class="row-title">${esc(cardShortLabel(c))}</span>${c.archived ? `<span class="row-sub">${esc(STRINGS.archived)}</span>` : ''}</span></label>`).join('')).join('') +
    `<label class="row check-row cash-check"><input type="checkbox" data-cash value="${NO_CARD}"${picked.has(NO_CARD) ? ' checked' : ''}>
       <i class="card-dot sw-none" aria-hidden="true"></i>
       <span class="row-text"><span class="row-title">${esc(STRINGS.cashAndOther)}</span><span class="row-sub">${esc(STRINGS.cashAndOtherHelp)}</span></span></label>`;
  const node = openSheet(STRINGS.filterCardTitle,
    `<div class="sheet-list" id="fk-list">${rows}</div>
     <div class="btn-row sticky-actions">
       <button type="button" class="btn" id="fk-none">${esc(STRINGS.clear)}</button>
       <button type="button" class="btn primary" id="fk-done">${esc(STRINGS.done)}</button>
     </div>`);
  const cardsOf = (key) => $$('#fk-list input[data-card]', node).filter((n) => n.dataset.card === key);
  const sync = () => $$('#fk-list input[data-inst]', node).forEach((box) => {
    const items = cardsOf(box.dataset.inst);
    const on = items.filter((n) => n.checked).length;
    box.checked = on > 0 && on === items.length;
    box.indeterminate = on > 0 && on < items.length;
  });
  const apply = () => { sync(); setFilter({ cards: $$('#fk-list input[value]:checked', node).map((n) => n.value) }); };
  sync();
  $('#fk-list', node).addEventListener('change', (e) => {
    if (e.target.dataset.inst !== undefined) cardsOf(e.target.dataset.inst).forEach((n) => { n.checked = e.target.checked; });
    apply();
  });
  $('#fk-none', node).addEventListener('click', () => { $$('#fk-list input', node).forEach((n) => { n.checked = false; }); apply(); });
  $('#fk-done', node).addEventListener('click', closeSheet);
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
  return itemsByGroup(true).map(({ group, items }) =>
    `<optgroup label="${esc(group.name)}">${items.map((c) =>
      `<option value="${esc(c.id)}"${c.id === selected ? ' selected' : ''}>${esc(c.emoji + ' ' + c.name + (c.hidden ? STRINGS.hiddenSuffix : ''))}</option>`).join('')}</optgroup>`).join('');
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
   16. View: Summary (time range, group donut, group view, by group, by card, tax time)
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

const DONUT = { size: 200, outer: 94, inner: 60 };

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

// One slice per group that has spending (at most 8). A group keeps its colour from month to month.
// groups: [{ group, index, cents }] sorted highest first.
function donutHtml(groups, total, caption) {
  const pcts = shares(groups.map((g) => g.cents), total);
  const start = -Math.PI / 2, full = Math.PI * 2;
  let done = 0;
  const paths = groups.map((g, i) => {
    const a0 = start + (done / total) * full;
    done += g.cents;
    const a1 = start + (done / total) * full;
    // A full circle cannot be drawn as one arc, so a lone slice is two halves.
    const d = groups.length === 1 ? ringSegment(a0, a0 + Math.PI) + ringSegment(a0 + Math.PI, a0 + full) : ringSegment(a0, a1);
    const label = STRINGS.sliceLabel(g.group.name, fmtMoney(g.cents), pcts[i]);
    return `<path class="slice gc${g.index}" style="--i:${i}" d="${d}" tabindex="0" role="button" data-act="open-group" data-group="${g.group.id}"
      data-cents="${g.cents}" aria-label="${esc(label)}"><title>${esc(label)}</title></path>`;
  }).join('');
  const money = fmtMoney(total);
  const c = DONUT.size / 2;
  return `<svg class="donut" id="donut" viewBox="0 0 ${DONUT.size} ${DONUT.size}" role="group" aria-label="${esc(STRINGS.donutLabel)}">
    ${paths}
    <text class="donut-total${money.length > 10 ? ' small' : ''}" id="donut-total" x="${c}" y="${c + 2}" text-anchor="middle" aria-hidden="true">${esc(money)}</text>
    <text class="donut-sub" x="${c}" y="${c + 22}" text-anchor="middle" aria-hidden="true">${esc(caption)}</text>
  </svg>`;
}

// The tallest bar the chart draws: 1.2 times the second-highest day, so one big day (rent, say)
// cannot flatten the rest. With a single day of spending, that day sets the scale.
function dailyCap(perDay) {
  const sorted = perDay.filter((c) => c > 0).sort((a, b) => b - a);
  if (!sorted.length) return 0;
  return sorted.length === 1 ? sorted[0] : Math.round(sorted[1] * 1.2);
}

// One bar per day of the month; today is marked. Only days with spending are tappable.
// A day above the cap is drawn at full height with a break mark and its amount above it.
function dailyBarsHtml(list) {
  const year = ui.month.y, month = ui.month.m;
  const days = new Date(year, month + 1, 0).getDate();
  const perDay = new Array(days + 1).fill(0);
  list.forEach((e) => { perDay[Number(e.date.slice(8, 10))] += e.amountCents; });
  const cap = dailyCap(perDay);
  const W = 320, top = 14, plot = 92, H = top + plot, axis = 18, step = W / days, barW = Math.max(3, step * 0.66);
  const today = todayStr();
  let bars = '';
  for (let d = 1; d <= days; d++) {
    const date = year + '-' + pad2(month + 1) + '-' + pad2(d);
    const x = (d - 1) * step, bx = x + (step - barW) / 2, mid = x + step / 2;
    const isToday = date === today;
    if (isToday) bars += `<circle class="today-dot" id="today-dot" cx="${mid.toFixed(2)}" cy="${H + 4}" r="2.2"/>`;
    if (!perDay[d]) {
      bars += `<rect class="bar-empty" x="${bx.toFixed(2)}" y="${H - 1.5}" width="${barW.toFixed(2)}" height="1.5" rx=".75"/>`;
      continue;
    }
    const over = perDay[d] > cap;
    const h = Math.max(3, Math.min(1, perDay[d] / cap) * plot);
    const label = STRINGS.barLabel(dayLabel(date), fmtMoney(perDay[d]));
    let extra = '';
    if (over) {
      // two short diagonal lines across the bar, and the amount in whole dollars above it
      const y = H - h + 7, l = (bx - 1.5).toFixed(2), r = (bx + barW + 1.5).toFixed(2);
      const anchor = mid < 26 ? 'start' : mid > W - 26 ? 'end' : 'middle';
      const tx = anchor === 'start' ? Math.max(0, bx - 1) : anchor === 'end' ? Math.min(W, bx + barW + 1) : mid;
      extra = `<path class="break" d="M${l} ${(y + 2.2).toFixed(2)}L${r} ${(y - 2.2).toFixed(2)}M${l} ${(y + 6.2).toFixed(2)}L${r} ${(y + 1.8).toFixed(2)}"/>
        <text class="over-label" x="${tx.toFixed(2)}" y="${top - 4}" text-anchor="${anchor}" aria-hidden="true">${esc(STRINGS.wholeDollars(intFmt.format(Math.round(perDay[d] / 100))))}</text>`;
    }
    bars += `<g class="daybar${isToday ? ' today' : ''}${over ? ' capped' : ''}" tabindex="0" role="button" data-act="filter-day" data-day="${date}" data-cents="${perDay[d]}" aria-label="${esc(label)}">
      <title>${esc(label)}</title>
      <rect class="hit" x="${x.toFixed(2)}" y="0" width="${step.toFixed(2)}" height="${H + axis}"/>
      <rect class="dbar" x="${bx.toFixed(2)}" y="${(H - h).toFixed(2)}" width="${barW.toFixed(2)}" height="${h.toFixed(2)}" rx="${Math.min(2.5, barW / 2).toFixed(2)}"/>${extra}</g>`;
  }
  let ticks = '';
  for (let d = 1; d <= days; d += 7) {
    ticks += `<text class="axis" x="${((d - 0.5) * step).toFixed(2)}" y="${H + axis - 2}" text-anchor="middle" aria-hidden="true">${d}</text>`;
  }
  return `<svg class="daily" id="daily-bars" viewBox="0 0 ${W} ${H + axis}" data-cap="${cap}" role="group" aria-label="${esc(STRINGS.dailyLabel)}">${bars}${ticks}</svg>`;
}

// Rows with amount, share and bar. `extra` is an optional class for the row.
function shareRowsHtml(rows, total, act, extra) {
  const pcts = shares(rows.map((r) => r.cents), total);
  return rows.map((r, i) =>
    `<button type="button" class="cat-row${extra ? ' ' + extra : ''}" data-act="${act}" data-ref="${esc(r.key)}" aria-label="${esc(STRINGS.sliceLabel(r.name, fmtMoney(r.cents), pcts[i]))}">
       <span class="cat-line">${r.lead}<span class="name">${esc(r.name)}</span>
         <span class="amt">${esc(fmtMoney(r.cents))}</span><span class="pct">${pcts[i]}%</span></span>
       <span class="bar"><i style="width:${(r.cents * 100 / total).toFixed(2)}%"></i></span>
     </button>`).join('');
}

const emojiLead = (emoji) => `<span aria-hidden="true">${esc(emoji)}</span>`;
const itemRowsOf = (g) => g.items.map((r) => ({ key: r.cat.id, name: r.cat.name, cents: r.cents, lead: emojiLead(r.cat.emoji) }));

// The month's spending by group: [{ group, index, cents, items: [{ cat, cents }] }], highest first.
function groupTotals(list) {
  const perItem = new Map();
  list.forEach((e) => perItem.set(e.categoryId, (perItem.get(e.categoryId) || 0) + e.amountCents));
  return GROUPS.map((group, index) => {
    const items = Array.from(perItem.entries()).map(([id, cents]) => ({ cat: catById(id), cents }))
      .filter((r) => groupOfCat(r.cat).id === group.id)
      .sort((a, b) => b.cents - a.cents || a.cat.order - b.cat.order);
    return { group, index, items, cents: items.reduce((sum, r) => sum + r.cents, 0) };
  }).filter((g) => g.cents > 0).sort((a, b) => b.cents - a.cents || a.index - b.index);
}

// One group, opened from the donut: its items with totals, shares of the group and bars,
// for the month or range on screen. The header accent and the bars use the group's colour.
function groupViewHtml(groups, total, scope) {
  const group = groupById(ui.summaryGroup);
  const index = GROUPS.indexOf(group);
  const g = groups.find((x) => x.group.id === group.id);
  const head =
    `<div class="card gc${index}" id="group-view" data-group="${group.id}">
       <button type="button" class="row plain row-action" id="group-back" data-act="close-group">${esc(STRINGS.allGroups)}</button>
       <div class="month-total"><h2 class="group-name" id="group-name"><span aria-hidden="true">${esc(group.emoji)}</span> ${esc(group.name)}</h2>
         <div class="big" id="group-total">${esc(fmtMoney(g ? g.cents : 0))}</div>
         <div class="sub" id="group-share">${esc(g ? STRINGS.groupShare(Math.round(g.cents * 100 / total), scope.label) : STRINGS.noExpenses(scope.label))}</div></div>
     </div>`;
  if (!g) return head;
  return head + `<div class="section-head"><span>${esc(STRINGS.groupItems(group.name))}</span></div>
     <div class="card gc${index}" id="group-items">${shareRowsHtml(itemRowsOf(g), g.cents, 'filter-cat')}</div>`;
}

// By group: one row per group, each opening to its items (shares are of the whole month or range).
// Each group's bar has the colour of its donut slice.
function byGroupHtml(groups, total) {
  const pcts = shares(groups.map((g) => g.cents), total);
  return groups.map((g, i) => {
    const open = ui.openGroups.has(g.group.id);
    const label = STRINGS.sliceLabel(g.group.name, fmtMoney(g.cents), pcts[i]);
    return `<div class="grp gc${g.index}" data-group="${g.group.id}">
      <button type="button" class="cat-row grp-row" data-act="toggle-group" data-ref="${g.group.id}" aria-expanded="${open}" aria-label="${esc(label)}">
        <span class="cat-line">${emojiLead(g.group.emoji)}<span class="name">${esc(g.group.name)}</span>
          <span class="amt">${esc(fmtMoney(g.cents))}</span><span class="pct">${pcts[i]}%</span>${ICONS.chev}</span>
        <span class="bar"><i style="width:${(g.cents * 100 / total).toFixed(2)}%"></i></span>
      </button>
      ${open ? `<div class="sub-rows">${shareRowsHtml(itemRowsOf(g), total, 'filter-cat', 'item-row')}</div>` : ''}
    </div>`;
  }).join('');
}

/* ----- Time range: this month's view, or a rolling 3 or 12 calendar months ending with the current one ----- */
const RANGES = ['month', '3', '12'];

function rangeMonths(count) {
  const now = currentMonth();
  return Array.from({ length: count }, (_, i) => shiftMonth(now, i - (count - 1)));
}

// "Sep – Nov 2026", or "Dec 2025 – Nov 2026" across a year end. Takes 'YYYY-MM' strings.
function rangeLabelOf(from, to) {
  const part = (ym) => ({ y: Number(ym.slice(0, 4)), name: STRINGS.monthsShort[Number(ym.slice(5, 7)) - 1] });
  const a = part(from), b = part(to);
  return a.y === b.y ? `${a.name} – ${b.name} ${b.y}` : `${a.name} ${a.y} – ${b.name} ${b.y}`;
}

// What Summary is showing: the expenses, a label, and the History filter that matches it.
function summaryScope() {
  if (ui.range === 'month') {
    return { range: false, label: monthLabel(ui.month), list: expensesInMonth(ui.month), filter: { month: monthCopy() } };
  }
  const months = rangeMonths(Number(ui.range));
  const from = monthPrefix(months[0]), to = monthPrefix(months[months.length - 1]);
  const list = state.expenses.filter((e) => e.date.slice(0, 7) >= from && e.date.slice(0, 7) <= to);
  return { range: true, months, label: rangeLabelOf(from, to), list, filter: { range: { from, to } } };
}

// One bar per month of the range; the current month is marked "so far". Tapping a bar opens that month.
function monthlyBarsHtml(months, list) {
  const totals = new Map(months.map((m) => [monthPrefix(m), 0]));
  list.forEach((e) => { const key = e.date.slice(0, 7); totals.set(key, totals.get(key) + e.amountCents); });
  const max = Math.max.apply(null, Array.from(totals.values()));
  const W = 320, top = 6, plot = 92, H = top + plot, axis = 28, step = W / months.length, barW = Math.min(36, step * 0.62);
  const current = monthPrefix(currentMonth());
  const bars = months.map((m, i) => {
    const key = monthPrefix(m), cents = totals.get(key), now = key === current;
    const x = i * step, bx = x + (step - barW) / 2, mid = (x + step / 2).toFixed(2);
    const h = max > 0 ? (cents / max) * plot : 0;
    const label = STRINGS.barLabel(monthLabel(m), fmtMoney(cents));
    return `<g class="monthbar${now ? ' current' : ''}" tabindex="0" role="button" data-act="open-month" data-month="${key}" data-cents="${cents}" aria-label="${esc(label)}">
      <title>${esc(label)}</title>
      <rect class="hit" x="${x.toFixed(2)}" y="0" width="${step.toFixed(2)}" height="${H + axis}"/>
      <rect class="bar-empty" x="${bx.toFixed(2)}" y="${H - 1.5}" width="${barW.toFixed(2)}" height="1.5" rx=".75"/>
      <rect class="mbar" x="${bx.toFixed(2)}" y="${(H - h).toFixed(2)}" width="${barW.toFixed(2)}" height="${h.toFixed(2)}" rx="${Math.min(3, h / 2).toFixed(2)}"/>
      <text class="axis" x="${mid}" y="${H + 12}" text-anchor="middle" aria-hidden="true">${esc(STRINGS.monthsShort[m.m])}</text>
      ${now ? `<text class="axis so-far" x="${mid}" y="${H + 22}" text-anchor="middle" aria-hidden="true">${esc(STRINGS.soFar)}</text>` : ''}</g>`;
  }).join('');
  return `<svg class="daily monthly" id="monthly-bars" viewBox="0 0 ${W} ${H + axis}" role="group" aria-label="${esc(STRINGS.monthlyLabel)}">${bars}</svg>`;
}

function rangeSelectorHtml() {
  return `<div class="seg" id="range-seg" role="group" aria-label="${esc(STRINGS.rangeLabel)}">${RANGES.map((r) =>
    `<button type="button" class="seg-btn" data-act="set-range" data-range="${r}" aria-pressed="${ui.range === r}">${esc(STRINGS.ranges[r])}</button>`).join('')}</div>`;
}

VIEWS.summary = function renderSummary() {
  const scope = summaryScope();
  const list = scope.list;
  const total = sumCents(list);
  const groups = groupTotals(list);
  const perCard = new Map();
  list.forEach((e) => {
    const key = cardById(e.cardId) ? e.cardId : NO_CARD;
    perCard.set(key, (perCard.get(key) || 0) + e.amountCents);
  });

  let body;
  if (ui.summaryGroup) {
    body = groupViewHtml(groups, total, scope);
  } else if (!groups.length) {
    body = `<div class="empty"><p>${esc(STRINGS.noExpenses(scope.label))}</p></div>`;
  } else {
    const cardRows = Array.from(perCard.entries()).map(([key, cents]) => {
      const card = key === NO_CARD ? null : cardById(key);
      return {
        key, cents,
        name: card ? cardShortLabel(card) : STRINGS.cashAndOther,
        lead: card ? cardBadgeHtml(card) : '<i class="card-dot sw-none" aria-hidden="true"></i>',
        last: key === NO_CARD
      };
    }).sort((a, b) => (a.last - b.last) || b.cents - a.cents);
    // Month view: the day-by-day chart. Range views: one bar per month instead.
    const chart = scope.range
      ? `<h2 class="chart-title">${esc(STRINGS.monthlyTitle)}</h2>${monthlyBarsHtml(scope.months, list)}
         <p class="footnote">${esc(STRINGS.chartHintRange)}</p>`
      : `<h2 class="chart-title">${esc(STRINGS.dailyTitle)}</h2>${dailyBarsHtml(list)}
         <p class="footnote">${esc(STRINGS.chartHint)}</p>`;
    body =
      `<button type="button" class="btn primary compare-btn" id="btn-compare" data-act="compare">${esc(STRINGS.compareButton)}</button>
       <div class="card charts${ui.drawCharts ? ' draw' : ''}" id="charts">
         <div class="donut-wrap">${donutHtml(groups, total, scope.range ? STRINGS.monthsCount(scope.months.length) : STRINGS.months[ui.month.m])}</div>
         ${chart}
       </div>
       <div class="section-head"><span>${esc(STRINGS.byGroup)}</span></div>
       <div class="card" id="by-group">${byGroupHtml(groups, total)}</div>
       ${state.cards.length ? `<div class="section-head"><span>${esc(STRINGS.byCard)}</span></div>
       <div class="card" id="by-card">${shareRowsHtml(cardRows, total, 'filter-card-row')}</div>` : ''}`;
  }
  const drawing = ui.drawCharts;
  ui.drawCharts = false;
  const head = scope.range
    ? `<div class="range-head"><span class="month-label" id="range-label">${esc(scope.label)}</span></div>
       <div class="month-total"><div class="total-wrap"><div class="big" id="summary-total">${esc(fmtMoney(total))}</div></div>
         <div class="sub" id="summary-count">${esc(STRINGS.expenseCount(list.length))}</div>
         <div class="sub" id="range-avg">${esc(STRINGS.rangeAverage(fmtMoney(Math.round(total / scope.months.length))))}</div></div>`
    : `${monthSwitchHtml()}
       <div class="month-total"><div class="total-wrap"><div class="big" id="summary-total">${esc(fmtMoney(total))}</div></div>
         <div class="sub" id="summary-count">${esc(STRINGS.expenseCount(list.length))}</div></div>`;
  // Tax time is by calendar year, so it belongs to the Month view only.
  const tax = scope.range || ui.summaryGroup ? null : taxTotalsForYear(ui.month.y);
  el.view.innerHTML =
    `<div class="page${drawing ? ' summary-in' : ''}">${rangeSelectorHtml()}${head}
       ${body}
       ${tax ? `<div class="card" id="tax-card">
         <h2 class="card-title">${esc(STRINGS.taxTime(ui.month.y))}</h2>
         ${TAX_TAGS.map((tag) => `<div class="kv" data-tax="${tag}"><span>${esc(STRINGS.taxRows[tag])}</span><span class="v">${esc(fmtMoney(tax[tag]))}</span></div>`).join('')}
         <p class="footnote" id="tax-footnote">${esc(STRINGS.taxFootnote)}</p>
       </div>` : ''}
     </div>`;
  if (drawing) countUp($('#summary-total'), total);
};

// The total counts up in an aria-hidden layer drawn over #summary-total, whose own text is the
// final value from the start (and is what tests and screen readers read).
function countUp(node, cents) {
  if (!node || cents <= 0 || !motionOK()) return;
  const layer = document.createElement('div');
  layer.className = 'big count-layer';
  layer.setAttribute('aria-hidden', 'true');
  layer.textContent = fmtMoney(0);
  node.classList.add('counting');
  node.parentNode.appendChild(layer);
  const started = performance.now(), length = 450;
  const finish = () => { layer.remove(); node.classList.remove('counting'); };
  const step = (now) => {
    if (!layer.isConnected) return;
    const k = Math.min(1, (now - started) / length);
    layer.textContent = fmtMoney(Math.round(cents * (1 - Math.pow(1 - k, 3))));
    if (k < 1) requestAnimationFrame(step); else finish();
  };
  requestAnimationFrame(step);
  setTimeout(finish, length + 150);          // in case frames are not being drawn
}

/* =====================================================================
   17. Cards (Profile → My cards; only names are stored, never card numbers)
   ===================================================================== */
// The built-in Canadian card list: one of the site's own files, loaded when first needed
// and kept offline by the service worker. Adding a card by hand works without it.
const catalogue = { status: 'idle', cards: [], issuers: [], pending: null };

// Returns { cards, issuers }. Issuers are A to Z (a leading "The" is ignored); each has the short
// name for its badge and a colour index taken from its place in that order, so neighbours differ.
function parseCatalogue(data) {
  const known = new Map();
  (Array.isArray(data && data.issuers) ? data.issuers : []).forEach((i) => {
    if (!i || typeof i.id !== 'string' || typeof i.name !== 'string' || !i.name.trim()) return;
    const short = typeof i.short === 'string' ? i.short.trim() : '';
    known.set(i.id, { id: i.id, name: i.name.trim(), short: short.length >= 2 && short.length <= 6 ? short : '' });
  });
  const seen = new Set();
  const cards = [];
  (Array.isArray(data && data.cards) ? data.cards : []).forEach((c) => {
    if (!c || typeof c.id !== 'string' || !c.id || seen.has(c.id)) return;
    if (typeof c.name !== 'string' || !c.name.trim() || CARD_KINDS.indexOf(c.kind) === -1) return;
    seen.add(c.id);
    const issuer = known.get(c.issuerId);
    cards.push({
      id: c.id,
      issuerId: issuer ? issuer.id : '',
      issuer: issuer ? issuer.name : '',
      name: c.name.trim().slice(0, 80),
      kind: c.kind,
      networks: (Array.isArray(c.networks) ? c.networks : []).filter((n) => CARD_NETWORKS.indexOf(n) !== -1)
    });
  });
  if (!cards.length) throw new Error('empty card list');
  const cmp = (a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' });
  cards.sort((a, b) => cmp(a.issuer, b.issuer) || cmp(a.name, b.name));
  const byName = new Map();
  cards.forEach((c) => {
    const name = c.issuer || STRINGS.otherIssuer;
    if (!byName.has(name)) {
      const info = known.get(c.issuerId);
      byName.set(name, { id: c.issuerId, name, short: (info && info.short) || monogram(name), cards: [] });   // no short name: initials
    }
    byName.get(name).cards.push(c);
  });
  const key = (name) => fold(name).replace(/^the\s+/, '');
  const issuers = Array.from(byName.values()).sort((a, b) => cmp(key(a.name), key(b.name)));
  issuers.forEach((issuer, index) => { issuer.colour = index % BADGE_COLOURS; });
  return { cards, issuers };
}

// The app's only network call: a JSON file that is part of the site itself (the card list, the
// tax figures). Rejects when the file cannot be fetched or read.
function fetchJson(url) {
  try {
    return fetch(url, { credentials: 'same-origin' }).then((res) => {
      if (!res.ok) throw new Error('not available');
      return res.json();
    });
  } catch (e) { return Promise.reject(e); }
}

// Resolves true when the list is ready, false when it could not be loaded. Never rejects.
function loadCatalogue() {
  if (catalogue.status === 'ok') return Promise.resolve(true);
  if (catalogue.pending) return catalogue.pending;
  catalogue.status = 'loading';
  catalogue.pending = fetchJson(CARDS_URL)
    .then((data) => { const list = parseCatalogue(data); catalogue.cards = list.cards; catalogue.issuers = list.issuers; catalogue.status = 'ok'; return true; })
    .catch(() => { catalogue.status = 'failed'; return false; })
    .then((ok) => { catalogue.pending = null; return ok; });
  return catalogue.pending;
}

// "Issuer · Credit · Visa · •••• 1234". The card's own name is added when a nickname hides it,
// and a part that only repeats an earlier one (an issuer that is also the network) is left out.
function cardMetaLine(card) {
  const parts = [card.nickname ? card.name : '', card.issuer, STRINGS.cardKinds[card.kind], card.networks.join(' / '),
    card.last4 ? STRINGS.last4Dots(card.last4) : ''].filter(Boolean);
  return parts.filter((part, i) => parts.findIndex((other) => other.toLowerCase() === part.toLowerCase()) === i).join(STRINGS.sep);
}

// Institution badge: short text on a rounded rectangle. The colour is one of 12 from the app's own
// palette (null means neutral grey). Never a logo, never a bank's brand colour. The text is drawn
// by CSS from data-t, so it is decoration and stays out of the row's readable text.
const badgeHtml = (text, colour) =>
  `<span class="ibadge ${colour === null ? 'ib-n' : 'ib-' + colour}" data-t="${esc(text)}" aria-hidden="true"></span>`;

// A card from the list gets its institution's badge. A card added by hand gets initials on grey.
function cardBadgeHtml(card) {
  const issuer = card.catalogueId && catalogue.status === 'ok' ? catalogue.issuers.find((i) => i.name === card.issuer) : null;
  return issuer ? badgeHtml(issuer.short, issuer.colour) : badgeHtml(monogram(card.issuer || card.name), null);
}

// Badges for the user's cards need the card list. It is loaded only when the user has such cards.
function loadBadges() {
  if (catalogue.status === 'ok' || !state.cards.some((c) => c.catalogueId)) return;
  loadCatalogue().then((ok) => { if (ok && !sheet.node && ui.tab !== 'history') render(); });
}

// One or two letters where an institution has no short name, or a card was added by hand: "RBC Royal Bank" gives RB,
// "American Express" gives AE, "Tangerine" gives T.
function monogram(name) {
  const words = String(name).replace(/^the\s+/i, '').split(/[^0-9A-Za-zÀ-ɏ]+/).filter(Boolean);
  if (!words.length) return '?';
  if (/^[A-Z0-9]{2,}$/.test(words[0])) return words[0].slice(0, 2);
  if (words.length === 1) return words[0].charAt(0).toUpperCase();
  return (words[0].charAt(0) + words[1].charAt(0)).toUpperCase();
}

function catalogueStatusHtml() {
  return `<p class="list-note" id="card-list-status" role="status">${esc(catalogue.status === 'failed' ? STRINGS.cardListFailed : STRINGS.cardListLoading)}</p>`;
}

// Add a card: institution, then card type, then card, then the confirmation, all in one sheet.
// One card at a time. The back arrow and Escape go up one level; closing discards everything,
// and every opening starts again at the institutions with the search cleared.
function openAddCardSheet() {
  const pick = { query: '' };
  const level = { cls: 'picker', bodyCls: 'pick-body', focusTitle: true };
  const kindsAt = (issuer) => CARD_KINDS.filter((k) => issuer.cards.some((c) => c.kind === k));
  const ofKind = (issuer, kind) => issuer.cards.filter((c) => c.kind === kind);
  const footer = (id, text) => `<button type="button" class="row plain row-action pick-foot" id="${id}">${esc(text)}</button>`;
  const addedBadge = (owned, c) => (owned.has(c.id) ? `<span class="badge muted">${esc(STRINGS.cardAdded)}</span>` : '');
  const ownedIds = () => new Set(state.cards.map((c) => c.catalogueId).filter(Boolean));
  const byHand = (issuerName, back) => openCardForm({ mode: 'manual', issuer: issuerName, back, slide: 'fwd' });
  const confirmCard = (item, back) => openCardForm({ mode: 'catalogue', item, back, slide: 'fwd' });

  // Level 1: institutions, with a search that also finds cards by name.
  function institutions(slide) {
    const node = openSheet(STRINGS.addACard,
      `<input class="input search" type="search" id="ac-search" autocomplete="off" autocapitalize="off" spellcheck="false"
         placeholder="${esc(STRINGS.cardSearchPlaceholder)}" aria-label="${esc(STRINGS.cardSearchLabel)}" value="${esc(pick.query)}">
       <div class="sheet-list pick-list" id="ac-list"></div>
       ${footer('ac-manual', STRINGS.cardNotListed)}`, Object.assign({ slide }, level));
    const list = $('#ac-list', node), search = $('#ac-search', node);
    const show = () => {
      if (catalogue.status !== 'ok') { list.innerHTML = catalogueStatusHtml(); return; }
      const words = fold(pick.query).split(/\s+/).filter(Boolean);
      const hit = (text) => { const hay = fold(text); return words.every((w) => hay.indexOf(w) !== -1); };
      const row = (i) =>
        `<button type="button" class="row" data-issuer="${esc(i.name)}">${badgeHtml(i.short, i.colour)}
           <span class="row-text"><span class="row-title">${esc(i.name)}</span><span class="row-sub">${esc(STRINGS.cardCount(i.cards.length))}</span></span>${ICONS.chev}</button>`;
      const section = (id, title, rows) => (rows.length ? `<p class="group-head" id="${id}">${esc(title)}</p>` + rows.map(row).join('') : '');
      const issuers = catalogue.issuers.filter((i) => hit(i.name));
      let html;
      if (words.length) {
        html = issuers.map(row).join('');          // searching: one flat list of matches
      } else {
        // Your institutions, then the popular ones, then everything else A to Z.
        const mine = new Set(state.cards.filter((c) => c.catalogueId && !c.archived).map((c) => c.issuer));
        const yours = issuers.filter((i) => mine.has(i.name));
        const popular = POPULAR_ISSUER_IDS.map((id) => issuers.find((i) => i.id === id)).filter((i) => i && !mine.has(i.name));
        const rest = issuers.filter((i) => !mine.has(i.name) && popular.indexOf(i) === -1);
        html = section('ac-yours', STRINGS.yourInstitutions, yours) + section('ac-popular', STRINGS.popularInstitutions, popular) +
          section('ac-all', STRINGS.allInstitutions, rest);
      }
      if (words.length) {
        const owned = ownedIds();
        const cards = catalogue.cards.filter((c) => hit(c.name));
        if (cards.length) {
          html += `<p class="group-head" id="ac-cards-head">${esc(STRINGS.cardsGroup)}</p>` + cards.map((c) =>
            `<button type="button" class="row" data-cat-id="${esc(c.id)}"><span class="row-text"><span class="row-title">${esc(c.name)}</span>
               <span class="row-sub">${esc([c.issuer, STRINGS.cardKinds[c.kind]].filter(Boolean).join(STRINGS.sep))}</span></span>${addedBadge(owned, c)}${ICONS.chev}</button>`).join('');
        }
        if (!issuers.length && !cards.length) html = `<p class="list-note" id="card-no-match">${esc(STRINGS.cardNoMatch)}</p>`;
      }
      list.innerHTML = html;
    };
    show();
    loadCatalogue().then(() => { if (sheet.node === node) show(); });
    search.addEventListener('input', () => { pick.query = search.value; show(); });
    list.addEventListener('click', (e) => {
      const row = e.target.closest('[data-issuer], [data-cat-id]');
      if (!row) return;
      if (row.dataset.issuer !== undefined) {
        const issuer = catalogue.issuers.find((i) => i.name === row.dataset.issuer);
        if (issuer) openIssuer(issuer);
      } else {
        const item = catalogue.cards.find((c) => c.id === row.dataset.catId);
        if (item) confirmCard(item, () => institutions('back'));       // a card result goes straight to the confirmation
      }
    });
    $('#ac-manual', node).addEventListener('click', () => byHand('', () => institutions('back')));
  }

  // An institution with one type of card skips the type level; back then returns to the institutions.
  function openIssuer(issuer) {
    const kinds = kindsAt(issuer);
    if (kinds.length === 1) cards(issuer, kinds[0], () => institutions('back'), 'fwd');
    else types(issuer, 'fwd');
  }

  // Level 2: the card types this institution has.
  function types(issuer, slide) {
    const up = () => institutions('back');
    const node = openSheet(issuer.name,
      `<div class="sheet-list pick-list" id="ac-types">${kindsAt(issuer).map((k) =>
         `<button type="button" class="row" data-kind="${k}"><span class="row-text"><span class="row-title">${esc(STRINGS.cardKindPlural[k])}</span>
            <span class="row-sub">${esc(STRINGS.cardCount(ofKind(issuer, k).length))}</span></span>${ICONS.chev}</button>`).join('')}</div>
       ${footer('ac-manual-here', STRINGS.cardNotListedAt(issuer.name))}`, Object.assign({ slide, back: up }, level));
    $('#ac-types', node).addEventListener('click', (e) => {
      const row = e.target.closest('[data-kind]');
      if (row) cards(issuer, row.dataset.kind, () => types(issuer, 'back'), 'fwd');
    });
    $('#ac-manual-here', node).addEventListener('click', () => byHand(issuer.name, () => types(issuer, 'back')));
  }

  // Level 3: the cards of one type at one institution.
  function cards(issuer, kind, up, slide) {
    const owned = ownedIds();
    const here = () => cards(issuer, kind, up, 'back');
    const node = openSheet(issuer.name + STRINGS.sep + STRINGS.cardKindPlural[kind],
      `<div class="sheet-list pick-list" id="ac-cards">${ofKind(issuer, kind).map((c) =>
         `<button type="button" class="row" data-cat-id="${esc(c.id)}"><span class="row-text"><span class="row-title">${esc(c.name)}</span>
            ${c.networks.length ? `<span class="row-sub">${esc(c.networks.join(' / '))}</span>` : ''}</span>${addedBadge(owned, c)}${ICONS.chev}</button>`).join('')}</div>
       ${footer('ac-manual-here', STRINGS.cardNotListedAt(issuer.name))}`, Object.assign({ slide, back: up }, level));
    $('#ac-cards', node).addEventListener('click', (e) => {
      const row = e.target.closest('[data-cat-id]');
      const item = row && catalogue.cards.find((c) => c.id === row.dataset.catId);
      if (item) confirmCard(item, here);
    });
    $('#ac-manual-here', node).addEventListener('click', () => byHand(issuer.name, here));
  }

  institutions(null);
}

function colourPickerHtml(selected) {
  return `<fieldset class="field"><legend>${esc(STRINGS.cardColour)}</legend><div class="swatches" id="cf-colours">${CARD_COLOURS.map((c) =>
    `<label class="swatch"><input type="radio" name="cf-colour" value="${c}"${c === selected ? ' checked' : ''} aria-label="${esc(STRINGS.colourNames[c])}"><span class="sw-${c}"></span></label>`).join('')}</div></fieldset>`;
}

// Anything that looks like a long run of digits is refused: card numbers do not belong here.
const looksLikeCardNumber = (text) => /\d{8,}/.test(String(text).replace(/[\s-]/g, ''));

// opts: { mode: 'catalogue', item } | { mode: 'manual', issuer } | { mode: 'edit', card }
// From the picker it also gets `back` (up one level) and `slide`, and stays in the same sheet.
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
       <input class="input" type="text" id="cf-issuer" maxlength="60" autocomplete="off" autocapitalize="words" placeholder="${esc(STRINGS.cardIssuerPlaceholder)}" value="${esc(opts.issuer || '')}"></label>
     <label class="field"><span class="label">${esc(STRINGS.cardName)}</span>
       <input class="input" type="text" id="cf-name" maxlength="80" autocomplete="off" autocapitalize="words" placeholder="${esc(STRINGS.cardNamePlaceholder)}"></label>
     <fieldset class="field"><legend>${esc(STRINGS.cardKind)}</legend><div class="options three" id="cf-kinds">${CARD_KINDS.map((k, i) =>
       `<label class="option"><input type="radio" name="cf-kind" value="${k}"${i === 0 ? ' checked' : ''}><span>${esc(STRINGS.cardKinds[k])}</span></label>`).join('')}</div></fieldset>
     <label class="field"><span class="label">${esc(STRINGS.cardNetwork)}</span>
       <select class="input" id="cf-network"><option value="">${esc(STRINGS.cardNetworkNone)}</option>${CARD_NETWORKS.map((n) =>
         `<option value="${esc(n)}">${esc(n)}</option>`).join('')}</select></label>`;
  const node = openSheet(edit ? STRINGS.editCard : manual ? STRINGS.addOwnCard : STRINGS.confirmCard,
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
         <button type="button" class="btn primary" id="cf-save">${esc(edit ? STRINGS.save : STRINGS.addCardSave)}</button>
       </div>
       ${edit ? `<div class="btn-row"><button type="button" class="btn ghost-danger" id="cf-remove">${esc(STRINGS.removeCard)}</button></div>` : ''}
     </div>
     <div id="cf-confirm" hidden>
       <p class="result" id="cf-confirm-text">${esc(used ? STRINGS.archiveCardConfirm(used) : STRINGS.removeCardConfirm)}</p>
       <div class="btn-row">
         <button type="button" class="btn" id="cf-confirm-cancel">${esc(STRINGS.cancel)}</button>
         <button type="button" class="btn danger" id="cf-confirm-remove">${esc(STRINGS.removeCard)}</button>
       </div>
     </div>`, edit ? {} : { cls: 'picker', back: opts.back, slide: opts.slide, focusTitle: !!opts.back });
  const last4 = $('#cf-last4', node);
  last4.addEventListener('input', () => {
    const digits = last4.value.replace(/\D/g, '').slice(0, 4);
    if (digits !== last4.value) last4.value = digits;
  });
  $('#cf-cancel', node).addEventListener('click', () => { if (!edit && opts.back) opts.back(); else closeSheet(); });
  if (edit) {
    const showConfirm = (on) => { $('#cf-actions', node).hidden = on; $('#cf-confirm', node).hidden = !on; };
    $('#cf-remove', node).addEventListener('click', () => { showConfirm(true); $('#cf-confirm-cancel', node).focus(); });
    $('#cf-confirm-cancel', node).addEventListener('click', () => { showConfirm(false); $('#cf-remove', node).focus(); });
    $('#cf-confirm-remove', node).addEventListener('click', () => {
      const outcome = removeCard(card.id);
      if (ui.draft.cardId === card.id) ui.draft.cardId = null;
      if (outcome === 'deleted') ui.filters.cards = ui.filters.cards.filter((id) => id !== card.id);
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
    showToast(edit ? STRINGS.cardSaved : STRINGS.cardAddedNamed(manual ? name : opts.item.name), { ms: 2500 });
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
  loadPayEstimate();
  const swatch = (c) => `<i class="card-swatch sw-${c.colour}" aria-hidden="true"></i>`;
  const cardText = (c) => `<span class="row-text"><span class="row-title">${esc(cardDisplayName(c))}</span><span class="row-sub">${esc(cardMetaLine(c))}</span></span>`;
  const active = activeCards(), archived = archivedCards();
  const tiles = active.map((c) =>
    `<button type="button" class="row card-tile" data-act="card-edit" data-id="${esc(c.id)}">${swatch(c)}${cardBadgeHtml(c)}${cardText(c)}${ICONS.chev}</button>`).join('');
  const archivedHtml = !archived.length ? '' :
    `<div class="section-head"><span>${esc(STRINGS.archived)}</span></div>
     <div class="card" id="archived-cards">${archived.map((c) =>
       `<div class="row card-tile archived" data-id="${esc(c.id)}">${swatch(c)}${cardBadgeHtml(c)}${cardText(c)}
          <button type="button" class="btn small" data-act="card-restore" data-id="${esc(c.id)}" aria-label="${esc(STRINGS.restoreCardLabel(cardDisplayName(c)))}">${esc(STRINGS.restoreCard)}</button></div>`).join('')}</div>`;
  const cats = itemsByGroup(true).map(({ group, items }) => groupHeadHtml(group) + items.map((c) =>
    `<button type="button" class="row" data-act="cat-edit" data-id="${esc(c.id)}">
       <span class="row-emoji" aria-hidden="true">${esc(c.emoji)}</span>
       <span class="row-text"><span class="row-title">${esc(c.name)}</span></span>
       ${tagBadge(c)}${c.hidden ? `<span class="badge muted">${esc(STRINGS.hidden)}</span>` : ''}${ICONS.chev}</button>`).join('')).join('');
  el.view.innerHTML =
    `<div class="page">
       <div class="section-head"><span>${esc(STRINGS.myCards)}</span></div>
       <div class="card" id="card-list">
         ${tiles
           ? `${tiles}<button type="button" class="row plain row-action" id="btn-add-card" data-act="card-add">${esc(STRINGS.addACard)}</button>`
           : `<div class="empty-cards"><p id="no-cards">${esc(STRINGS.noCards)}</p>
                <button type="button" class="btn primary" id="btn-add-card" data-act="card-add">${esc(STRINGS.addACard)}</button></div>`}
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

       <div class="section-head"><span>${esc(STRINGS.paySection)}</span></div>
       <div class="card" id="pay-settings">
         <button type="button" class="row" id="btn-pay" data-act="pay-edit">
           <span class="row-text"><span class="row-title">${esc(STRINGS.payRow)}</span>
             <span class="row-sub wrap" id="pay-summary">${esc(paySummaryText())}</span></span>${ICONS.chev}</button>
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

// The Pay row shows an estimate, which needs the tax figures; they are loaded only when pay is saved.
function loadPayEstimate() {
  const pay = state.settings.pay;
  if (!pay || pay.takeHomeOverrideCents !== null || taxData.status !== 'idle') return;
  loadTaxData().then((ok) => { if (ok && ui.tab === 'profile' && !sheet.node && !report.node) VIEWS.profile(); });
}

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
       <input class="input" type="text" id="c-name" maxlength="${CAT_NAME_MAX}" autocomplete="off" autocapitalize="sentences" value="${esc(cat ? cat.name : '')}"></label>
     <label class="field"><span class="label">${esc(STRINGS.catGroup)}</span>
       <select class="input" id="c-group">${GROUPS.map((g) =>
         `<option value="${g.id}"${g.id === (cat ? cat.groupId : DEFAULT_GROUP) ? ' selected' : ''}>${esc(g.emoji + ' ' + g.name)}</option>`).join('')}</select></label>
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
    const name = $('#c-name', node).value.trim().slice(0, CAT_NAME_MAX);
    const groupId = $('#c-group', node).value;
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
      if (isGroupId(groupId)) cat.groupId = groupId;
    } else {
      createCategory(name, emoji, taxTag, groupId);
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
   19. Pay and "How do you compare?" (take-home estimate, typical Canadian budget, report)
   ===================================================================== */
// Typical share of monthly take-home pay, by budget group. Typical savings: 8%.
const TYPICAL = { housing: .30, debt: .07, communications: .04, food: .12, transportation: .15, recreation: .10, misc: .12, insurance: .02 };
const TYPICAL_SAVINGS = .08;
const PAY_MIN_CENTS = 100, PAY_MAX_CENTS = 200000000;        // $1 to $2,000,000

/* ----- Tax data: one of the site's own files, loaded when the Pay sheet or the report first needs it ----- */
const taxData = { status: 'idle', data: null, pending: null };

// The estimator needs every part of the file. A placeholder file (no real figures yet) does not count.
function validTaxData(d) {
  const num = (v) => typeof v === 'number' && Number.isFinite(v);
  const brackets = (b) => Array.isArray(b) && b.length > 0 && b[b.length - 1].upTo === null && b.every((x) => x && num(x.rate));
  const pension = (c) => !!c && num(c.ympe) && num(c.yampe) && num(c.exemption) && num(c.baseRate) && num(c.firstAdditionalRate) && num(c.secondAdditionalRate);
  if (!d || typeof d !== 'object' || d.placeholder === true) return false;
  const f = d.federal;
  if (!f || !brackets(f.brackets) || !num(f.creditRate) || !f.bpa || !num(f.bpa.max) || !num(f.employmentAmount) || !num(f.quebecAbatement)) return false;
  if (!pension(d.cpp) || !pension(d.qpp)) return false;
  if (!d.ei || !num(d.ei.maxInsurable) || !num(d.ei.rate) || !num(d.ei.rateQuebec)) return false;
  if (!d.qpip || !num(d.qpip.maxInsurable) || !num(d.qpip.rate)) return false;
  return !!d.provinces && PROVINCE_CODES.every((code) => {
    const p = d.provinces[code];
    return !!p && brackets(p.brackets) && num(p.creditRate) && !!p.bpa && num(p.bpa.max);
  });
}

// Resolves true when estimates are possible, false otherwise. Never rejects.
function loadTaxData() {
  if (taxData.status === 'ok') return Promise.resolve(true);
  if (taxData.pending) return taxData.pending;
  taxData.status = 'loading';
  taxData.pending = fetchJson(TAX_DATA_URL)
    .then((data) => {
      if (!validTaxData(data) || !window.DSTax) throw new Error('tax data not usable');
      taxData.data = data; taxData.status = 'ok'; return true;
    })
    .catch(() => { taxData.status = 'failed'; return false; })
    .then((ok) => { taxData.pending = null; return ok; });
  return taxData.pending;
}

function provinceName(code) {
  const fromData = taxData.status === 'ok' && taxData.data.provinces[code] && taxData.data.provinces[code].name;
  return (typeof fromData === 'string' && fromData) || PROVINCES[code] || '';
}

// Household take-home in dollars a month from gross pay, or null when it cannot be worked out here.
function estimateTakeHome(earnersCents, province) {
  if (taxData.status !== 'ok' || !earnersCents.length || PROVINCE_CODES.indexOf(province) === -1) return null;
  try {
    const monthly = window.DSTax.household(taxData.data, earnersCents.map((c) => c / 100), province).takeHomeMonthly;
    return Number.isFinite(monthly) && monthly > 0 ? monthly : null;
  } catch (e) { return null; }
}

// The saved pay as take-home dollars a month: the user's own figure if they gave one, else the estimate.
function savedTakeHome() {
  const pay = state.settings.pay;
  if (!pay) return null;
  if (pay.takeHomeOverrideCents !== null) return pay.takeHomeOverrideCents / 100;
  return estimateTakeHome(pay.earners, pay.province);
}

const wholeDollars = (dollars) => STRINGS.wholeDollars(intFmt.format(Math.round(dollars)));

// "85,000", "85000.50" or "$85,000" to cents; null when it is not an amount from $1 to $2,000,000.
function parsePayAmount(text) {
  const t = String(text).replace(/[$,\s]/g, '');
  if (!/^\d{1,7}(\.\d{1,2})?$/.test(t)) return null;
  const c = typedToCents(t);
  return c >= PAY_MIN_CENTS && c <= PAY_MAX_CENTS ? c : null;
}
const payFieldText = (cents) => (cents % 100 === 0 ? intFmt.format(cents / 100) : centsToPlain(cents));

function paySummaryText() {
  const pay = state.settings.pay;
  if (!pay) return STRINGS.payNotSet;
  if (pay.takeHomeOverrideCents !== null) return STRINGS.payOwn(wholeDollars(pay.takeHomeOverrideCents / 100));
  const where = (pay.earners.length === 2 ? STRINGS.payTwoEarners + STRINGS.sep : '') + provinceName(pay.province);
  const estimate = estimateTakeHome(pay.earners, pay.province);
  return estimate === null ? where : where + STRINGS.sep + STRINGS.payAbout(wholeDollars(estimate));
}

/* ----- Pay sheet. from: 'summary' (then the report opens) or 'profile' ----- */
function openPaySheet(from) {
  const profile = from === 'profile';
  const saved = state.settings.pay;
  let second = !!saved && saved.earners.length === 2;
  let editing = !!saved && saved.takeHomeOverrideCents !== null;      // the take-home field is showing
  let override = saved ? saved.takeHomeOverrideCents : null;
  const money = (id, value) =>
    `<span class="money-field"><i aria-hidden="true">$</i><input class="input num" type="text" inputmode="decimal" id="${id}" autocomplete="off" value="${esc(value)}"></span>`;
  const provinceOptions = () => `<option value="">${esc(STRINGS.payChoose)}</option>` + PROVINCE_CODES
    .map((code) => ({ code, name: provinceName(code) }))
    .sort((a, b) => a.name.localeCompare(b.name, 'en'))
    .map((p) => `<option value="${p.code}"${saved && saved.province === p.code ? ' selected' : ''}>${esc(p.name)}</option>`).join('');
  const node = openSheet(STRINGS.payTitle,
    `<p class="help" id="pay-intro">${esc(STRINGS.payIntro)}</p>
     <div class="field"><label class="label" for="pay-1">${esc(STRINGS.payGross)}</label>${money('pay-1', saved && saved.earners[0] ? payFieldText(saved.earners[0]) : '')}</div>
     <div class="field" id="pay-second"${second ? '' : ' hidden'}>
       <div class="field-head"><label class="label" for="pay-2">${esc(STRINGS.payGrossSecond)}</label>
         <button type="button" class="icon-btn" id="pay-remove-2" aria-label="${esc(STRINGS.payRemoveSecond)}">×</button></div>
       ${money('pay-2', saved && saved.earners[1] ? payFieldText(saved.earners[1]) : '')}</div>
     <button type="button" class="link-row" id="pay-add-earner"${second ? ' hidden' : ''}>${esc(STRINGS.payAddEarner)}</button>
     <label class="field"><span class="label">${esc(STRINGS.payProvince)}</span>
       <select class="input" id="pay-province">${provinceOptions()}</select></label>
     <div class="pay-estimate plain" id="pay-estimate-box"><span id="pay-estimate" role="status"></span>
       <button type="button" class="btn small" id="pay-edit">${esc(STRINGS.payEdit)}</button>
       <button type="button" class="btn small" id="pay-use-estimate" hidden>${esc(STRINGS.payUseEstimate)}</button></div>
     <div class="field" id="pay-takehome-field"${editing ? '' : ' hidden'}><label class="label" for="pay-takehome">${esc(STRINGS.payTakeHome)}</label>
       ${money('pay-takehome', override !== null ? payFieldText(override) : '')}</div>
     <p class="error" id="pay-error" role="alert"></p>
     <p class="help" id="pay-footnote">${esc(STRINGS.payFootnote)}</p>
     <button type="button" class="btn primary block" id="pay-save" disabled>${esc(profile ? STRINGS.save : STRINGS.paySeeReport)}</button>
     <div class="btn-row">${profile
       ? (saved ? `<button type="button" class="btn ghost-danger" id="pay-remove">${esc(STRINGS.payRemove)}</button>` : `<button type="button" class="btn" data-sheet-close>${esc(STRINGS.cancel)}</button>`)
       : `<button type="button" class="btn" id="pay-skip">${esc(STRINGS.paySkip)}</button>`}</div>`);
  const q = (id) => $('#' + id, node);
  const province = q('pay-province');

  // What the fields say right now.
  const read = () => {
    const texts = [q('pay-1').value.trim()].concat(second ? [q('pay-2').value.trim()] : []);
    const cents = texts.map(parsePayAmount);
    const takeText = editing ? q('pay-takehome').value.trim() : '';
    return {
      cents,
      grossOk: cents.every((c) => c !== null) && province.value !== '',
      badGross: texts.some((t, i) => t !== '' && cents[i] === null),
      takeText,
      take: takeText === '' ? null : parsePayAmount(takeText)
    };
  };
  const refresh = () => {
    const r = read();
    const estimate = r.grossOk ? estimateTakeHome(r.cents, province.value) : null;
    const failed = taxData.status === 'failed';
    if (failed && !editing) { editing = true; q('pay-takehome-field').hidden = false; }
    // An edited take-home that differs from the estimate is the user's own figure.
    override = r.take !== null && (estimate === null || r.take !== Math.round(estimate) * 100) ? r.take : null;
    let line;
    if (override !== null) line = STRINGS.payUsing(wholeDollars(override / 100));
    else if (estimate !== null) line = STRINGS.payEstimated(wholeDollars(estimate));
    else if (failed) line = STRINGS.payNoEstimate;
    else line = STRINGS.payEstimateHint;
    q('pay-estimate').textContent = line;
    q('pay-estimate-box').classList.toggle('plain', override === null && estimate === null);
    q('pay-edit').hidden = editing;
    q('pay-use-estimate').hidden = !(editing && !failed);
    q('pay-error').textContent = r.badGross || (r.takeText !== '' && r.take === null) ? STRINGS.payError : '';
    q('pay-save').disabled = !(override !== null || (r.grossOk && estimate !== null));
    return { r, estimate };
  };
  node.addEventListener('input', refresh);
  node.addEventListener('change', refresh);
  q('pay-add-earner').addEventListener('click', () => {
    second = true;
    q('pay-second').hidden = false; q('pay-add-earner').hidden = true;
    refresh();
    q('pay-2').focus();
  });
  q('pay-remove-2').addEventListener('click', () => {
    second = false;
    q('pay-2').value = '';
    q('pay-second').hidden = true; q('pay-add-earner').hidden = false;
    refresh();
    q('pay-add-earner').focus();
  });
  q('pay-edit').addEventListener('click', () => {
    const { estimate } = refresh();
    editing = true;
    q('pay-takehome-field').hidden = false;
    if (q('pay-takehome').value.trim() === '' && estimate !== null) q('pay-takehome').value = intFmt.format(Math.round(estimate));
    refresh();
    q('pay-takehome').focus();
  });
  q('pay-use-estimate').addEventListener('click', () => {
    editing = false;
    q('pay-takehome').value = '';
    q('pay-takehome-field').hidden = true;
    refresh();
    q('pay-edit').focus();
  });
  q('pay-save').addEventListener('click', () => {
    const { r, estimate } = refresh();
    if (override === null && !(r.grossOk && estimate !== null)) return;
    state.settings.pay = {
      earners: r.grossOk ? r.cents : [],
      province: r.grossOk ? province.value : null,
      takeHomeOverrideCents: override,
      taxYear: TAX_YEAR,
      updatedAt: nowIso()
    };
    state.settings.paySkipped = false;
    saveState();
    closeSheet();
    if (profile) { render(); showToast(STRINGS.paySaved, { ms: 2000 }); } else openCompare();
  });
  if (q('pay-skip')) q('pay-skip').addEventListener('click', () => {
    state.settings.paySkipped = true;
    saveState();
    closeSheet();
    openCompare();
  });
  if (q('pay-remove')) q('pay-remove').addEventListener('click', () => {
    state.settings.pay = null;
    state.settings.paySkipped = false;
    saveState();
    closeSheet();
    render();
    showToast(STRINGS.payRemoved, { ms: 2000 });
  });
  refresh();
  loadTaxData().then(() => {
    if (sheet.node !== node) return;
    const chosen = province.value;
    province.innerHTML = provinceOptions();       // names as the data file spells them
    province.value = chosen;
    refresh();
  });
}

/* ----- The report's numbers. Pure: takes the Summary scope and the take-home (dollars a month, or null). ----- */
const onePlace = (x) => (Math.round(x * 10) / 10).toFixed(1);
const pctText = (ratio) => String(Math.round(ratio * 1000) / 10) + '%';        // 17.5%, 30%

function reportModel(scope, takeHome) {
  const months = scope.range ? scope.months.length : 1;
  const spent = groupTotals(scope.list);                                        // groups with spending, in cents
  const S = new Map(spent.map((g) => [g.group.id, g.cents / 100 / months]));    // dollars a month
  const logged = GROUPS.filter((g) => S.has(g.id));
  const total = logged.reduce((sum, g) => sum + S.get(g.id), 0);
  const typicalTotal = logged.reduce((sum, g) => sum + TYPICAL[g.id], 0);
  const payMode = takeHome !== null;
  const items = logged.map((group) => {
    const s = S.get(group.id);
    // Every comparison uses the figures as shown (whole dollars, or shares to one decimal place), so the cards foot.
    const shown = Math.round(s);
    const item = { group, index: GROUPS.indexOf(group), spend: shown, trim: Math.round(0.1 * shown) };
    if (payMode) {
      item.typical = Math.round(TYPICAL[group.id] * takeHome);
      item.diff = item.spend - item.typical;                                    // whole dollars over (+) or under (-)
      item.yours = s / takeHome;
      item.typicalShare = TYPICAL[group.id];
    } else {
      item.yours = s / total;
      item.typicalShare = TYPICAL[group.id] / typicalTotal;
      item.yoursShown = Math.round(item.yours * 1000) / 10;                     // 45.5
      item.typicalShown = Math.round(item.typicalShare * 1000) / 10;
      item.diff = Math.round((item.yoursShown - item.typicalShown) * 10) / 10;  // points over (+) or under (-)
    }
    item.win = item.diff <= 0;
    return item;
  });
  const wins = items.filter((i) => i.win).sort((a, b) => a.diff - b.diff);      // furthest under first
  const overs = items.filter((i) => !i.win).sort((a, b) => b.diff - a.diff);    // furthest over first
  const ratio = items.length ? wins.length / items.length : 0;
  const now = monthPrefix(currentMonth());
  const includesNow = scope.range || monthPrefix(ui.month) === now;
  const model = {
    payMode, takeHome, months, items, wins, overs, total,
    notLogged: GROUPS.filter((g) => !S.has(g.id)),
    headline: ratio === 1 ? STRINGS.rpBoss : ratio >= 0.75 ? STRINGS.rpSharp : ratio >= 0.5 ? STRINGS.rpBalanced : STRINGS.rpGrow,
    period: scope.range ? scope.label + STRINGS.sep + STRINGS.rpMonthlyAverage : scope.label,
    includesNow,
    nowAlone: !scope.range && includesNow,
    enough: payMode ? items.length >= 1 : items.length >= 2
  };
  if (payMode) {
    const pay = Math.round(takeHome), left = pay - Math.round(total);            // as shown, so the line foots
    model.savings = { left, rate: left / pay, win: left / pay >= TYPICAL_SAVINGS, target: Math.round(TYPICAL_SAVINGS * takeHome) };
  }
  return model;
}

/* ----- The report's cards ----- */
function reportCards(m) {
  const pay = state.settings.pay;
  const payButton = (id) => `<button type="button" class="btn" id="${id}" data-rp="pay">${esc(m.payMode ? STRINGS.rpEditPay : STRINGS.rpAddPay)}</button>`;
  const box = (kind, attrs, inner) => ({ kind, html: `<section class="rp-card${attrs.cls || ''}" data-kind="${kind}"${attrs.data || ''} aria-roledescription="slide">
      <div class="rp-box">${inner}</div></section>` });
  if (!m.enough) {
    return [box('few', {}, `<h3 tabindex="-1">${esc(STRINGS.reportTitle)}</h3><p class="rp-lead" id="rp-few">${esc(STRINGS.rpFew)}</p>${payButton('rp-add-pay')}`)];
  }
  const money = wholeDollars;
  const amountOf = (item) => (m.payMode ? money(Math.abs(item.diff)) : onePlace(Math.abs(item.diff)));
  const underLine = (item) => (m.payMode
    ? (item.diff === 0 ? STRINGS.rpAtTypical : STRINGS.rpLess(amountOf(item)))
    : (item.diff === 0 ? STRINGS.rpAtTypicalShare : STRINGS.rpPointsUnder(amountOf(item))));
  const overLine = (item) => (m.payMode
    ? (item.diff <= 0.05 * item.typical ? STRINGS.rpJustOver(amountOf(item)) : STRINGS.rpOver(amountOf(item)))
    : STRINGS.rpPointsOver(amountOf(item)));
  const trimLine = (item) => STRINGS.rpTrim(money(item.trim), money(12 * item.trim));
  const cards = [];

  // 1. Score
  const where = pay && pay.province && pay.takeHomeOverrideCents === null ? STRINGS.sep + provinceName(pay.province) : '';
  cards.push(box('score', {}, `<div class="rp-emoji" aria-hidden="true">📊</div>
    <h3 tabindex="-1" id="rp-headline">${esc(m.headline)}</h3>
    <p class="rp-lead" id="rp-score">${esc(STRINGS.rpScore(m.wins.length, m.items.length))}</p>
    <p class="rp-text" id="rp-period">${esc(m.period)}</p>
    ${m.payMode
      ? `<button type="button" class="btn link" id="rp-edit-pay" data-rp="pay">${esc(STRINGS.rpTakeHome(money(m.takeHome)) + where)}</button>`
      : `<p class="rp-text" id="rp-mode">${esc(STRINGS.rpSplitMode)}</p>${payButton('rp-add-pay')}`}
    ${m.includesNow ? `<p class="rp-note" id="rp-so-far">${esc(STRINGS.rpSoFar)}</p>` : ''}
    ${m.nowAlone ? `<p class="rp-note" id="rp-not-over">${esc(STRINGS.rpNotOver)}</p>` : ''}`));

  // 2. Wins, then 3. overs: you against typical, in the group's colours
  const compare = (item) => {
    const scale = Math.max(item.yours, item.typicalShare);
    const width = (v) => Math.max(2, (v / scale) * 100).toFixed(1);
    const you = m.payMode ? STRINGS.rpYou(money(item.spend), pctText(item.yours)) : STRINGS.rpYouShare(item.yoursShown.toFixed(1), money(item.spend));
    const typical = m.payMode ? STRINGS.rpTypical(money(item.typical), pctText(item.typicalShare)) : STRINGS.rpTypicalShare(item.typicalShown.toFixed(1));
    return `<div class="rp-emoji" aria-hidden="true">${esc(item.group.emoji)}</div>
      <h3 tabindex="-1">${esc(item.group.name)}</h3>
      <div class="rp-bars" aria-hidden="true">
        <div><div class="rp-bar-label"><b>${esc(STRINGS.rpYouLabel)}</b></div><div class="rp-bar you"><i style="width:${width(item.yours)}%"></i></div></div>
        <div><div class="rp-bar-label"><b>${esc(STRINGS.rpTypicalLabel)}</b></div><div class="rp-bar typical"><i style="width:${width(item.typicalShare)}%"></i></div></div>
      </div>
      <p class="rp-text rp-you">${esc(you)}</p><p class="rp-text rp-typical">${esc(typical)}</p>`;
  };
  m.wins.forEach((item) => cards.push(box('win', { cls: ' gc' + item.index, data: ` data-group="${item.group.id}" data-confetti="1"` },
    `${compare(item)}<p class="rp-strong rp-diff">${esc(underLine(item))}</p>
     ${m.payMode && item.diff < 0 ? `<p class="rp-text rp-year">${esc(STRINGS.rpYear(money(12 * -item.diff)))}</p>` : ''}`)));
  m.overs.forEach((item) => cards.push(box('over', { cls: ' gc' + item.index, data: ` data-group="${item.group.id}"` },
    `${compare(item)}<p class="rp-strong rp-diff">${esc(overLine(item))}</p>
     <p class="rp-text rp-trim">${esc(trimLine(item))}</p>
     <p class="rp-tip">${esc(STRINGS.tips[item.group.id])}</p>`)));

  // 4. Savings (pay mode only)
  if (m.payMode) {
    const s = m.savings;
    let lines;
    if (s.left < 0) {
      lines = `<p class="rp-strong" id="rp-savings-line">${esc(STRINGS.rpSpentMore(money(-s.left)))}</p><p class="rp-text" id="rp-savings-next">${esc(STRINGS.rpStartBiggest)}</p>`;
    } else {
      lines = `<p class="rp-strong" id="rp-savings-line">${esc(STRINGS.rpLeft(money(s.left), pctText(s.rate)))}</p>
        <p class="rp-text" id="rp-savings-typical">${esc(STRINGS.rpTypicalSaves)}</p>
        <p class="rp-lead" id="rp-savings-next">${esc(s.win ? STRINGS.rpSavingsWin : STRINGS.rpSavingsTarget(money(s.target)))}</p>`;
    }
    cards.push(box('savings', { data: s.win ? ' data-confetti="1"' : '' },
      `<div class="rp-emoji" aria-hidden="true">💰</div><h3 tabindex="-1">${esc(STRINGS.rpSavingsTitle)}</h3>${lines}
       <p class="rp-note">${esc(STRINGS.rpOnlyLogged)}</p>`));
  }

  // 5. Not logged yet
  if (m.notLogged.length) {
    cards.push(box('notlogged', {}, `<h3 tabindex="-1">${esc(STRINGS.rpNotLogged)}</h3>
      <ul class="rp-list" id="rp-not-logged">${m.notLogged.map((g) => `<li>${esc(g.name)}</li>`).join('')}</ul>
      <p class="rp-text">${esc(STRINGS.rpNotLoggedHint)}</p>`));
  }

  // 6. Wrap-up
  const best = m.wins[0], opp = m.overs[0];
  cards.push(box('wrap', { data: m.wins.length ? ' data-confetti="1"' : '' }, `<h3 tabindex="-1">${esc(STRINGS.rpWrapTitle)}</h3>
    ${best ? `<p class="rp-lead" id="rp-best">${esc(STRINGS.rpBest(best.group.name, underLine(best)))}</p>` : ''}
    ${opp ? `<p class="rp-lead" id="rp-opp">${esc(STRINGS.rpOpp(opp.group.name, overLine(opp)))}</p><p class="rp-text" id="rp-opp-trim">${esc(trimLine(opp))}</p>` : ''}
    <button type="button" class="btn primary" id="rp-done">${esc(STRINGS.done)}</button>
    ${payButton('rp-pay')}
    <p class="rp-note" id="rp-footnote">${esc(STRINGS.rpFootnote)}</p>`));
  return cards;
}

/* ----- The report: a full-screen dialog of cards that swipe sideways ----- */
const report = { node: null, opener: null, index: 0, count: 0, seen: new Set(), quietUntil: 0 };

function confetti() {
  if (!motionOK()) return;
  const hues = ['teal', 'blue', 'orange', 'purple', 'green', 'rose', 'indigo', 'slate'];
  const layer = document.createElement('div');
  layer.className = 'fx-confetti';
  let html = '';
  for (let i = 0; i < 24; i++) {
    const hue = hues[i % hues.length];
    const x = Math.round((Math.random() - 0.5) * 80), y = 260 + Math.round(Math.random() * 320);
    html += `<i style="left:${(4 + Math.random() * 92).toFixed(1)}%;--x:${x}px;--y:${y}px;--r:${Math.round((Math.random() - 0.5) * 900)}deg;--d:${Math.round(Math.random() * 140)}ms;--cc:var(--c-${hue});--ce:var(--c-${hue}-edge)"></i>`;
  }
  layer.innerHTML = html;
  $$('.fx-confetti', el.fx).forEach((old) => old.remove());   // one burst at a time
  fxAdd(layer, 900);
}

function reportGo(index, how) {
  if (!report.node) return;
  const track = $('#rp-track', report.node);
  const cards = $$('.rp-card', report.node);
  report.index = Math.max(0, Math.min(report.count - 1, index));
  cards.forEach((card, i) => {
    const on = i === report.index;
    card.inert = !on;
    if (on) card.removeAttribute('aria-hidden'); else card.setAttribute('aria-hidden', 'true');
  });
  $$('.rp-dots i', report.node).forEach((dot, i) => dot.classList.toggle('on', i === report.index));
  $('#rp-back', report.node).disabled = report.index === 0;
  $('#rp-next', report.node).disabled = report.index === report.count - 1;
  if (how !== 'swipe') {
    report.quietUntil = performance.now() + 500;          // ignore the scroll events this scroll causes
    try { track.scrollTo({ left: report.index * track.clientWidth, behavior: how === 'jump' || !motionOK() ? 'auto' : 'smooth' }); }
    catch (e) { track.scrollLeft = report.index * track.clientWidth; }
  }
  const card = cards[report.index];
  const heading = $('h3', card);
  if (heading) heading.focus({ preventScroll: true });
  // Confetti the first time a win card becomes the card on screen, once per opening.
  if (card.dataset.confetti && !report.seen.has(report.index)) confetti();
  report.seen.add(report.index);
}

function openReport(takeHome) {
  const scope = summaryScope();
  const cards = reportCards(reportModel(scope, takeHome));
  closeSheet();
  fxClear();
  const opener = report.node ? report.opener : document.activeElement;
  el.reportRoot.innerHTML =
    `<div id="report" role="dialog" aria-modal="true" aria-labelledby="report-title" tabindex="-1" data-mode="${takeHome === null ? 'split' : 'pay'}">
       <header class="rp-head"><h2 id="report-title">${esc(STRINGS.reportTitle)}</h2>
         <button type="button" class="icon-btn" id="rp-close" aria-label="${esc(STRINGS.close)}">×</button></header>
       <div class="rp-track" id="rp-track">${cards.map((c, i) => c.html.replace('aria-roledescription="slide"',
         `aria-roledescription="slide" aria-label="${esc(STRINGS.rpSlide(i + 1, cards.length))}"`)).join('')}</div>
       <footer class="rp-foot"><button type="button" class="btn" id="rp-back">${esc(STRINGS.back)}</button>
         <div class="rp-dots" aria-hidden="true">${cards.map(() => '<i></i>').join('')}</div>
         <button type="button" class="btn primary" id="rp-next">${esc(STRINGS.next)}</button></footer>
     </div>`;
  el.reportRoot.hidden = false;
  report.node = $('#report', el.reportRoot);
  report.opener = opener;
  report.count = cards.length;
  report.seen = new Set();
  el.app.inert = true;
  el.app.setAttribute('aria-hidden', 'true');
  const track = $('#rp-track', report.node);
  track.addEventListener('scroll', () => {
    if (!report.node || performance.now() < report.quietUntil) return;
    const at = Math.round(track.scrollLeft / Math.max(1, track.clientWidth));
    if (at !== report.index) reportGo(at, 'swipe');
  }, { passive: true });
  reportGo(0, 'jump');
}

function closeReport() {
  if (!report.node) return;
  const opener = report.opener;
  report.node = null;
  report.opener = null;
  el.reportRoot.hidden = true;
  el.reportRoot.innerHTML = '';
  fxClear();
  el.app.inert = false;
  el.app.removeAttribute('aria-hidden');
  if (opener && document.contains(opener) && typeof opener.focus === 'function') {
    try { opener.focus({ preventScroll: true }); } catch (e) { /* ignore */ }
  }
}

el.reportRoot.addEventListener('click', (e) => {
  if (e.target.closest('#rp-close') || e.target.closest('#rp-done')) closeReport();
  else if (e.target.closest('#rp-back')) reportGo(report.index - 1);
  else if (e.target.closest('#rp-next')) reportGo(report.index + 1);
  else if (e.target.closest('[data-rp="pay"]')) { closeReport(); openPaySheet('summary'); }
});

// The Summary button. No pay and not skipped: ask. Pay saved: compare with take-home. Skipped: compare the split.
function openCompare() {
  const pay = state.settings.pay;
  if (!pay) {
    if (state.settings.paySkipped) openReport(null); else openPaySheet('summary');
    return;
  }
  if (pay.takeHomeOverrideCents !== null) { openReport(pay.takeHomeOverrideCents / 100); return; }
  loadTaxData().then(() => {
    const takeHome = savedTakeHome();
    if (takeHome === null) openPaySheet('summary'); else openReport(takeHome);    // no estimate here: ask for take-home
  });
}

/* =====================================================================
   20. First-run setup (two steps; can be skipped at either)
   ===================================================================== */
// Shown once, the first time the app opens after categories were moved into budget groups.
function openGroupsNotice() {
  openSheet(STRINGS.groupsNoticeTitle,
    `<p class="ob-lead" id="mig-text">${esc(STRINGS.groupsNotice)}</p>
     <button type="button" class="btn primary block" id="mig-ok" data-sheet-close>${esc(STRINGS.ok)}</button>`,
    { onClose: () => { state.settings.groupsNotice = false; saveState(); } });
}

function openWelcome() {
  let step = 1;
  // However the sheet goes away (Skip, Done, ×, backdrop, Escape), setup is not shown again.
  const finished = () => {
    if (!state.settings.onboarded) { state.settings.onboarded = true; saveState(); }
  };
  const buttons = (last) =>
    `<div class="btn-row"><button type="button" class="btn" id="ob-skip">${esc(STRINGS.skip)}</button>
       <button type="button" class="btn primary" id="${last ? 'ob-done' : 'ob-next'}">${esc(last ? STRINGS.done : STRINGS.next)}</button></div>`;
  const stepLine = () => `<p class="ob-step" id="ob-step">${esc(STRINGS.obStep(step, 2))}</p>`;

  function show() {
    let node;
    if (step === 1) {
      node = openSheet(STRINGS.obTitle1,
        `${stepLine()}<p class="ob-lead">${esc(STRINGS.obBody1)}</p>
         <p class="help" id="ob-privacy">${esc(STRINGS.privacy)}</p>${buttons(false)}`, { onClose: finished });
      $('#ob-next', node).addEventListener('click', () => { step = 2; show(); });
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
      $('#ob-done', node).addEventListener('click', () => { closeSheet(); switchTab('add'); });
    }
    $('#ob-skip', node).addEventListener('click', closeSheet);
  }
  show();
}

/* =====================================================================
   21. Offline: service worker registration and the "Update ready" banner
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
   22. Events
   ===================================================================== */
const monthCopy = () => ({ y: ui.month.y, m: ui.month.m });

const ACTIONS = {
  tab: (t) => switchTab(t.dataset.tab),
  chip: (t) => selectCategory(t.dataset.cat, true),
  usual: (t) => selectCategory(t.dataset.cat, true),
  'chip-more': openAllCategoriesSheet,
  save: saveDraft,
  details: openDetailsSheet,
  recent: openRecentSheet,
  month: (t) => {
    ui.month = shiftMonth(ui.month, Number(t.dataset.delta));
    if (ui.tab === 'history') { renderHistoryBody(); return; }
    ui.drawCharts = ui.tab === 'summary';      // a new month draws in, like arriving on the tab
    VIEWS[ui.tab]();
  },
  compare: openCompare,
  'pay-edit': () => openPaySheet('profile'),
  edit: (t) => { if (swipe.open) { closeOpenSwipe(); return; } openEditSheet(t.dataset.id); },
  'swipe-delete': (t) => swipeDelete(t.dataset.id),
  'filter-category': openCategoryFilterSheet,
  'filter-card': openCardFilterSheet,
  'filter-loc': () => setFilter({ hasLocation: !ui.filters.hasLocation }),
  'filter-day-clear': () => setFilter({ day: null }),
  'filter-month-clear': () => setFilter({ month: null }),
  'filter-range-clear': () => setFilter({ range: null }),
  'filter-clear': clearFilters,
  // Summary: a donut slice opens its group inside Summary; a By group row opens in place.
  'open-group': (t) => { ui.summaryGroup = t.dataset.group; VIEWS.summary(); el.view.scrollTop = 0; },
  'close-group': () => { ui.summaryGroup = null; VIEWS.summary(); el.view.scrollTop = 0; },
  'toggle-group': (t) => { const id = t.dataset.ref; if (ui.openGroups.has(id)) ui.openGroups.delete(id); else ui.openGroups.add(id); VIEWS.summary(); },
  // Summary taps on an item, card or day: History with that filter, for the month or range on screen (a day needs neither).
  'filter-cat': (t) => openHistoryFiltered(Object.assign({ cats: [t.dataset.ref] }, summaryScope().filter)),
  'filter-card-row': (t) => openHistoryFiltered(Object.assign({ cards: [t.dataset.ref] }, summaryScope().filter)),
  'set-range': (t) => { if (RANGES.indexOf(t.dataset.range) === -1) return; ui.range = t.dataset.range; ui.drawCharts = true; VIEWS.summary(); el.view.scrollTop = 0; },
  // a bar of the monthly chart: that month, in Month view
  'open-month': (t) => {
    ui.month = { y: Number(t.dataset.month.slice(0, 4)), m: Number(t.dataset.month.slice(5, 7)) - 1 };
    ui.range = 'month';
    ui.summaryGroup = null;
    ui.drawCharts = true;
    VIEWS.summary();
    el.view.scrollTop = 0;
  },
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
  if (swipe.suppressClick) {
    swipe.suppressClick = false;
    if (el.view.contains(e.target)) return;      // only the list swallows the click after a swipe; the tab bar never does
  }
  const key = e.target.closest('[data-key]');
  if (key) { pressKey(key.dataset.key); return; }
  const target = e.target.closest('[data-act]');
  if (target && ACTIONS[target.dataset.act]) ACTIONS[target.dataset.act](target);
});

el.app.addEventListener('change', (e) => {
  if (e.target.id === 'set-auto-loc') onAutoLocationToggle(e.target);
});

document.addEventListener('keydown', (e) => {
  if (report.node && !sheet.node) {
    if (e.key === 'Escape') { e.preventDefault(); closeReport(); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); reportGo(report.index + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); reportGo(report.index - 1); }
    else if (e.key === 'Tab') trapFocusIn(report.node, e);
    return;
  }
  if (sheet.node) {
    if (e.key === 'Escape') { e.preventDefault(); if (sheet.back) sheet.back(); else closeSheet(); }   // up one level, or close
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
  else if (e.key === 'Enter' && e.target === document.body) { e.preventDefault(); saveDraft(); }
});

// Another tab changed the data: reload it.
window.addEventListener('storage', (e) => {
  if (e.key !== null && e.key !== STORAGE_KEY) return;
  if (store.mode !== 'ok') return;
  loadState();
  refreshChips();
  closeSheet();
  closeReport();
  if (ui.draft.cardId && !cardById(ui.draft.cardId)) ui.draft.cardId = null;
  ui.filters.cards = ui.filters.cards.filter((id) => id === NO_CARD || cardById(id));
  render();
  loadBadges();
});

// Keep "Today" correct when the app is reopened on a later day, and look for a new version.
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState !== 'visible') return;
  checkForUpdate();
  if (sheet.node || report.node) return;
  if (ui.tab === 'history' && document.activeElement && document.activeElement.id === 'h-search') renderHistoryBody();
  else render();
});

/* =====================================================================
   23. Start
   ===================================================================== */
loadState();
refreshChips();
resetDraft();
setKeyboardOverlap(0);
render();
probeDownloads().then(() => { if (ui.tab === 'profile' && !sheet.node) { const b = $('#btn-download'); if (b) b.hidden = !ui.canDownload; } });
registerServiceWorker();
loadBadges();
// After the move to budget groups: say so, once. Otherwise, first launch with nothing saved: the two-step welcome.
if (state.settings.groupsNotice) openGroupsNotice();
else if (!state.settings.onboarded && state.expenses.length === 0) openWelcome();

})();
