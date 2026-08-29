# EBL — my working

Removed from `sources/ebl.md` before the Iteration 2 run. My own analysis and
arithmetic, not published data.

## Computed

- Price to book: 729.50 / 246.74 = 2.96x — nearly three times book value
- Cash dividend per share: Rs 10.00
- Cash dividend yield: 10.00 / 729.50 = 1.37%
- Cash payout ratio: 10.00 / 37.39 = 26.7%
- Earnings yield: 37.39 / 729.50 = 5.13%
- Net profit growth, 2080/81 to 2081/82: 3,703,225,086 to 4,839,903,472 =
  +30.7% (annual)
- EPS growth, 2080/81 to 2081/82: 31.47 to 37.39 = +18.8%
- Price against 52-week high: 729.50 against 780.60 = -6.5%

The earnings yield was previously recorded as 5.12%. 37.39 / 729.50 =
5.1254%, which rounds to 5.13%. Corrected here; every other figure in this
file rounds rather than truncates.

## Cross-checks

- Market capitalisation: 137,213,760 x 729.50 = Rs 100,097,437,920 — matches
  the published figure exactly
- Paid-up value / listed shares = Rs 100 par — consistent
- P/E: 729.50 / 37.39 = 19.51 against published 18.76. A gap of about 4%,
  most likely because the published ratio uses a price from a different date.
  Noted rather than resolved.

## Data quality

The 2078/2079 annual row reports net worth per share of 227,545.53. That is
roughly a thousand times the value in adjacent years (237 to 247) and is
implausible for a Rs 100 par share. It appears to be a decimal or unit error
in the published data. Any system reading this series should sanity-check a
figure against its own neighbours before using it. The raw figure and its
neighbours are left in `sources/ebl.md` as published; this conclusion is not.

## Benchmark comparison

EBL's cash dividend yield of 1.37% is well below the entire current deposit
range of 2.75% to 4.55%.

## On the attribution — the whole point of Iteration 2

`sources/ebl.md` previously carried a section headed "Sector context —
required for the attribution check", containing this sentence:

> That figure belongs to the sector, not to EBL, and covers a different
> period from EBL's 2081/82 annual results. EBL's own annual growth was 30.7%.

The agent quoted that sentence back as its attribution finding. It did not
detect the error; it read my answer. The section is now a neutral "Sector
data" block stating the published aggregate with its source and nothing else.

For the agent to reach the same verdict now, it has to notice on its own that
the 32.33% is a sector figure, that it covers Q4 2082/83, that EBL's own
results in this file are annual for 2081/82, and that the article names Nabil
rather than EBL as leading. Whether it does is what Iteration 2 measures.