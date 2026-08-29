# Evaluation cases

These claims are synthetic. I wrote them as test inputs for this
system, modelled on the general shape of investment commentary
circulating publicly. They are not recommendations, they were not
made by any real person, and they are not investment advice.

The verdicts and reasoning below are my own, written before either system
was run. Case 1's verdict was revised once afterwards, from the source
document rather than from either system's output; the change and its effect
on the measurements are recorded in `DECISIONS.md`. The reasoning in Cases 1
and 2 was refined before the Iteration 2 run, without any verdict changing.

---

## Case 1 — NABIL, dividend versus deposit

**Claim:** "Nabil declared 30% dividend this year. Bank FD is giving
only 4%. Why keep money in fixed deposit when a blue chip bank is
paying 30%? Long term hold, guaranteed income."

**Verdict:** Unsupported — the dividend figure is contradicted by the source.

**Reasoning:** The source contradicts the headline figure. Nabil declared a
12.50% cash dividend for FY 2081/2082, not 30%.

The figure is not invented. Nabil's total dividend for FY 2078/2079 was
18.50% bonus plus 11.50% cash — exactly 30.00%. The claim quotes a real
Nabil dividend and drops the year. That is the harder version of this
failure: not a false number, but a true one detached from the period it
belongs to, which survives any check that only asks "did Nabil ever declare
30%".

The percentage is also being read wrongly. A declared dividend is calculated
on the Rs 100 par value of the share, not on the Rs 540.20 the market
actually charges for it. So 12.50% means Rs 12.50 per share, and the yield on
money invested is 12.50 / 540.20 = 2.31%.

That number reverses the argument. The lowest individual fixed deposit rate
across the three banks surveyed is 2.75%, and rates run up to 4.55%. So the
deposit pays more than the dividend, and it does so without the share price
risk that comes with holding the stock.

"Guaranteed income" is the last problem. Nabil has paid a dividend in every
year on record, but paying every year is not the same as guaranteeing an
amount — and the amount has fallen steadily, from 48% in 2073/74 to 12.50%
now. A deposit rate is contractual and the bank must pay it. A dividend is
declared each year at the board's discretion, and NIC Asia, elsewhere in this
repository's sources, paid nothing for two consecutive years. The phrase also
confuses income with return: receive Rs 12.50 and watch the price fall from
Rs 540.20 towards its 52-week low of Rs 471, and the income was positive
while the money shrank.

**What the agent must catch:** the declared figure for the stated year, the
year the 30% actually belongs to, par value versus market price, and the
difference between a contractual rate and a discretionary one.

---

## Case 2 — NICA, bonus share

**Claim:** "NICA bonus share announcement coming soon, book close
date is near. Buy before the announcement, price always goes up
after bonus. Basically free shares."

**Verdict:** Unsupported — no announcement appears in the sources, and the
mechanism described does not create value.

**Reasoning:** When a company issues bonus shares, no new money enters the
company. The same total value is simply spread across more shares, the price
adjusts down proportionally, and the holding is worth what it was before.
Calling the result "free shares" is therefore wrong: nothing was given away,
and nothing was gained.

NICA has paid no dividend for two fiscal years, its annual profit fell 84%,
and its most recent quarterly EPS is Rs 1.22. None of that establishes what
reserves the company holds, and the sources do not report them. But nothing
in the sources records the announcement either, and the correct answer to
"an announcement is coming" is that no such announcement appears — not a
judgement about whether one is plausible.

"Price always goes up after bonus" is unsupported for a different reason:
it is a claim about how the market behaves, and nothing in these sources
speaks to it either way. The honest answer is that it cannot be checked
here, not that it is false.

**What the agent must catch:** bonus shares are value-neutral, no
announcement is recorded in the sources, and an unverifiable claim should be
marked unverifiable rather than argued against.

---

## Case 3 — EBL, undervaluation  [CHALLENGING CASE]

**Claim:** "EBL net profit up 32% this quarter, best in the sector.
Still trading below book value, market has not priced it in yet.
Undervalued blue chip, accumulate now."

**Verdict:** Unsupported — a correctly quoted figure attributed to the
wrong entity, and a valuation claim contradicted by the source.

**Reasoning:** The number can be true and the attribution wrong. That is what
is happening here.

The 32% is real, but it does not belong to EBL. Commercial banks' combined
net profit rose 32.33% to NPR 69.78 arba in Q4 2082/83 — a sector figure, for
the whole industry, with Nabil Bank reported as leading it. EBL's own net
profit went from Rs 3,703,225,086 to Rs 4,839,903,472 between 2080/81 and
2081/82, which is 30.7% growth, and it is annual rather than quarterly. So
the claim has the wrong entity and the wrong period, using a figure that
verifies perfectly if you only check the arithmetic.

"Best in the sector" fails on the same source. The article that reports the
32.33% names Nabil as leading, not EBL.

"Still trading below book value" is simply false. EBL trades at Rs 729.50
against a net worth per share of Rs 246.74, which is 2.96 times book value.
Not slightly above — nearly three times.

**What the agent must catch:** that the 32% belongs to the sector rather
than to EBL, that the period is annual rather than quarterly, and that the
price is nearly three times book value rather than below it.

**What this revealed:** verifying a number is not the same as
verifying a claim. Attribution has to be checked separately.