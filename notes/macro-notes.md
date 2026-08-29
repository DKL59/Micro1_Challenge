# Macro — my working

Removed from `sources/macro.md` before the Iteration 2 run. My own synthesis
and conclusions, not published data.

## Benchmark range

| Bank | Lowest | Highest |
|---|---|---|
| NIC Asia | 2.75% | 4.00% |
| Nabil | 2.80% | 4.55% |
| EBL | 2.75% | 4.05% |

Range across all three banks: 2.75% to 4.55% for individual normal fixed
deposits. Remittance-linked deposits run higher, from 3.80% to 5.55% at
Nabil.

Rates cluster tightly across banks, so this range is representative rather
than one bank's outlier. The lowest rate available anywhere in this survey is
2.75%.

This table was previously in `sources/macro.md`. In Iteration 1 the agent
quoted the combined range as its source for "Bank FD is giving only 4%",
which meant it cited my aggregation rather than any bank's published card.
The three rate cards remain in the source file; deriving a range from them is
now the agent's job.

## Conclusions

A dividend yield below this range pays less income than a fixed deposit,
while also carrying price risk the deposit does not.

The correct comparison depends on both tenure and depositor category. Quoting
a single deposit rate would hide that choice, so any comparison must name
which rate it is using and why.

The 1% remittance premium visible in Nabil's current rate card is the same
structure that produced the higher 2022 remittance figures — normal rate plus
one percentage point at every tenure.

The same check produces opposite verdicts in different rate regimes. A 5%
dividend yield loses against a 12% deposit and beats a 4% one. This is why
the benchmark is read from a dated file rather than written into the code.

## Comparison against the cases

| Company | Yield | Lowest deposit rate | Verdict |
|---|---|---|---|
| NABIL | 2.31% dividend yield | 2.75% | Below every deposit product surveyed |
| EBL | 1.37% cash dividend yield | 2.75% | Below every deposit product surveyed |

This table stated the answer to two of the three cases. It was the clearest
instance of the corpus doing the agent's work.