/* Daily Spend: take-home pay estimator.
   Pure functions: no DOM, no storage, no network. The figures come from the data object
   passed in (data/tax-ca-<year>.json, loaded by app.js). Amounts are annual dollars and
   every component is rounded to cents. An estimate for salary income only. */
(function () {
'use strict';

const cents = (x) => Math.round(x * 100) / 100;

// Progressive tax over [{ upTo, rate }], ascending, the last upTo null.
function bracketTax(brackets, x) {
  let tax = 0, floor = 0;
  for (const b of brackets) {
    const top = b.upTo === null ? Infinity : b.upTo;
    if (x > floor) tax += (Math.min(x, top) - floor) * b.rate;
    floor = top;
  }
  return tax;
}

// Basic personal amount: flat, or reduced in a straight line between two incomes.
function bpa(b, netIncome) {
  if (b.phaseOutStart === null || b.phaseOutStart === undefined) return b.max;
  if (netIncome <= b.phaseOutStart) return b.max;
  if (netIncome >= b.phaseOutEnd) return b.min;
  return b.max - (b.max - b.min) * (netIncome - b.phaseOutStart) / (b.phaseOutEnd - b.phaseOutStart);
}

function taxReduction(r, tax, netIncome) {
  if (!r) return 0;
  if (r.type === 'ON') return Math.min(tax, Math.max(0, 2 * r.basic - tax));
  if (r.type === 'linear') return Math.min(tax, Math.max(0, r.max - r.rate * Math.max(0, netIncome - r.phaseOutStart)));
  return 0;
}

// One earner. G = gross pay for the year, P = province or territory code.
function estimate(data, grossDollars, provinceCode) {
  const G = Number(grossDollars), P = provinceCode;
  const quebec = P === 'QC';
  const c = quebec ? data.qpp : data.cpp;
  const pensionable = Math.max(0, Math.min(G, c.ympe) - c.exemption);
  const cppBase = cents(pensionable * c.baseRate);
  const cppFirst = cents(pensionable * c.firstAdditionalRate);
  const cpp2 = cents(Math.max(0, Math.min(G, c.yampe) - c.ympe) * c.secondAdditionalRate);
  const ei = cents(Math.min(G, data.ei.maxInsurable) * (quebec ? data.ei.rateQuebec : data.ei.rate));
  const qpip = cents(quebec ? Math.min(G, data.qpip.maxInsurable) * data.qpip.rate : 0);
  const NI = G - cppFirst - cpp2;                       // the enhanced contributions are deductible

  // Federal
  const f = data.federal;
  const fedCredits = bpa(f.bpa, NI) + Math.min(f.employmentAmount, G) + cppBase + ei + qpip;
  let federalTax = Math.max(0, bracketTax(f.brackets, NI) - f.creditRate * fedCredits);
  if (quebec) federalTax *= 1 - f.quebecAbatement;
  federalTax = cents(federalTax);

  // Provincial or territorial
  const p = data.provinces[P];
  const TI = NI - (p.employmentDeduction ? Math.min(p.employmentDeduction.max, p.employmentDeduction.rate * G) : 0);
  const credits = p.credits || {};
  const pCredits = bpa(p.bpa, NI) + (p.employmentAmount ? Math.min(p.employmentAmount, G) : 0) +
    (credits.cppBase ? cppBase : 0) + (credits.ei ? ei : 0) + (credits.qpip ? qpip : 0);
  const basic = Math.max(0, bracketTax(p.brackets, TI) - p.creditRate * pCredits);
  const surtax = (p.surtax || []).reduce((sum, s) => sum + s.rate * Math.max(0, basic - s.over), 0);
  const reduction = taxReduction(p.taxReduction, basic + surtax, NI);
  const premium = (p.healthPremium || []).reduce((sum, h) => sum + Math.min(h.max, Math.max(0, (TI - h.over) * h.rate)), 0);
  const provincialTax = cents(Math.max(0, basic + surtax - reduction) + premium);

  const takeHome = cents(G - (cppBase + cppFirst + cpp2) - ei - qpip - federalTax - provincialTax);
  return { gross: cents(G), cppBase, cppFirst, cpp2, ei, qpip, federalTax, provincialTax, takeHome };
}

// Earners in the same province, added up.
function household(data, earnersDollars, provinceCode) {
  const perEarner = earnersDollars.map((g) => estimate(data, g, provinceCode));
  const takeHomeAnnual = cents(perEarner.reduce((sum, e) => sum + e.takeHome, 0));
  return { perEarner, takeHomeAnnual, takeHomeMonthly: takeHomeAnnual / 12 };
}

window.DSTax = { estimate, household };
})();
