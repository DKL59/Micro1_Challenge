# Working notes

Everything in this folder was removed from `sources/` before the Iteration 2
run. It is my own analysis, arithmetic and commentary — not published data.

## Why the split exists

In Iteration 1 the source files mixed published figures with my conclusions
about them. The agent quoted the conclusions. Only one of the six substantive
quotes it returned was a published figure; the rest were sentences I had
written, including the one that supplied its entire attribution finding on
the challenging case.

That made the strongest number in the evaluation meaningless. It measured
whether the agent could retrieve an answer I had already written down, not
whether it could reach one.

So `sources/` now contains only what a person could read off a published page
— market data, results tables, dividend histories, rate cards, one sector
aggregate — each with the URL it came from. Everything I worked out from
those figures lives here instead.

The arithmetic is not lost, and the diff between the two states is visible in
the commit history and inside `results/agent_v1.json`, where every prompt
embeds the full text of the old source files.

## What is in each file

- `nabil-notes.md` — computed yields and ratios, cross-checks, the note on
  the 15-year dividend average, and the finding that the claim's 30% matches
  FY 2078/2079 exactly
- `nica-notes.md` — computed changes and ratios, cross-checks including an
  unresolved P/E discrepancy, and the note on how a news source framed a
  four-year dividend gap as consistency
- `ebl-notes.md` — computed yields and growth rates, the corrected earnings
  yield, the data quality note on an implausible published figure, and the
  full record of the sector-attribution sentence that Iteration 2 removed
- `macro-notes.md` — the three-bank benchmark range, the conclusions drawn
  from it, and the per-case comparison table that stated two answers outright

The agent never sees this folder. `cases.json` names only files under
`sources/`.