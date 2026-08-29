# Macro context

Retrieved: 29 August 2026

This file holds the benchmark rates any dividend yield claim is compared
against. The benchmark is read at runtime, never assumed.

## Current fixed deposit rates — individuals

### Nabil Bank, effective 1 Bhadra 2083 (August 2026)
Source: https://www.nabilbank.com/interest-rate

Normal:

| Tenure | Rate |
|---|---|
| 3 months to below 6 months | 2.80% |
| 6 months to 1 year | 2.85% |
| Above 1 to 2 years | 3.00% |
| Above 2 to 5 years | 3.25% |
| Above 5 to 10 years | 4.00% |
| Above 10 years | 4.55% |
| Cumulative, 1 year | 2.85% |

Remittance, a 1.00% premium over normal at every tenure:

| Tenure | Rate |
|---|---|
| 3 months to below 6 months | 3.80% |
| 6 months to 1 year | 3.85% |
| Above 1 to 2 years | 4.00% |
| Above 2 to 5 years | 4.25% |
| Above 5 to 10 years | 5.00% |
| Above 10 years | 5.55% |
| Cumulative, 1 year | 3.85% |

Minimum tenor: 3 months.

### NIC Asia Bank, effective 1 Shrawan 2083 (July 2026)
Source: https://www.nicasiabank.com/interest-rates/

- Range: 2.75% (shorter terms) to 4.00% (five years and above)

### Everest Bank, effective 1 Bhadra 2083 (17 August 2026)
Source: https://everestbankltd.com/supports/interest-and-rates/interest-rates-deposit/

| Tenure | Rate |
|---|---|
| 3 months to 2 years | 2.75% |
| Above 2 to 5 years | 3.50% |
| Above 5 years | 4.05% |

## Benchmark used

| Bank | Lowest | Highest |
|---|---|---|
| NIC Asia | 2.75% | 4.00% |
| Nabil | 2.80% | 4.55% |
| EBL | 2.75% | 4.05% |

Range across all three banks: **2.75% to 4.55%** for individual normal fixed
deposits. Remittance-linked deposits run higher, from 3.80% to 5.55% at
Nabil.

Rates cluster tightly across banks, so this range is representative rather
than one bank's outlier. The lowest rate available anywhere in this survey is
2.75%.

A dividend yield below this range pays less income than a fixed deposit,
while also carrying price risk the deposit does not.

The correct comparison depends on both tenure and depositor category.
Quoting a single deposit rate would hide that choice, so any comparison must
name which rate it is using and why.

## Historical context

Deposit rates have fallen sharply. In Ashoj 2079 (September 2022) individual
fixed deposits paid 12.133%, institutions 10.133% and remittance deposits
13.133%, with some banks offering as much as 15% on remittance deposits.
Rates were cut to 11% for individuals from Magh 2079 (January 2023).

The 1% remittance premium visible in Nabil's current rate card is the same
structure that produced those higher 2022 remittance figures.

Sources:
- https://www.sharesansar.com/newsdetail/most-banks-alter-their-interest-rates-individuals-deposit-interest-rates-increased-by-3-digits-after-the-decimal-point-2022-09-21
- https://www.sharesansar.com/newsdetail/committee-of-nepal-bankers-association-has-decided-to-decrease-fixed-deposits-interest-rates-for-the-month-of-magh-2023-01-12

The same check produces opposite verdicts in different rate regimes. A 5%
dividend yield loses against a 12% deposit and beats a 4% one. This is why
the benchmark is read from this file rather than written into the code.

## Comparison against the cases

| Company | Yield | Lowest deposit rate | Verdict |
|---|---|---|---|
| NABIL | 2.31% dividend yield | 2.75% | Below every deposit product surveyed |
| EBL | 1.37% cash dividend yield | 2.75% | Below every deposit product surveyed |