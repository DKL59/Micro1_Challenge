# NEPSE Claim Validator

A tool that checks whether an investment claim circulating publicly is
actually supported by the company's filings and current market conditions.
It does not tell anyone what to buy.

## Intended user

There are many kinds of participants in the NEPSE market: institutional
investors with large capital, business houses, and individuals investing
small and medium amounts. This system is for the last group — specifically
people in full-time jobs who invest on the side, and who do not have the
time, or in some cases the financial background, to check whether the
advice circulating about a particular company rests on any evidence.

Gathering the information, analysing it, and comparing one company against
another takes hours they do not have, or hours they would rather spend on
something else.

I was one of them. I invested on NEPSE from 2021 to 2023, trading mostly on
technical analysis with some basic fundamental research. Charts tell you
what a price has done. They tell you nothing about whether a declared
dividend is real, whether a yield beats a deposit, or whose growth figure is
being quoted. This is not a tool I designed for someone else's problem.

## Current bottleneck

They act on advice received from someone else, without validating it. That
hurts in two ways. They do not know why a particular stock is being
promoted, or what the person promoting it stands to gain. And they are
usually unaware of the macro conditions that determine whether any stock
does well.

During the last bear trend this was decisive. As commercial bank liquidity
declined, banks raised deposit rates — individual fixed deposits reached
12.133% in Ashoj 2079, remittance deposits 13.133%, with some banks
offering as much as 15%. Money flowed out of the capital market and into
the banks, and the market fell for a sustained period. Investors who did
not follow the connection between deposit rates and NEPSE lost money they
could have moved.

That was 2022 into 2023, and it is history rather than a description of
now. Deposit rates today run from 2.75% to 4.55%, and the money that left
the market for the banks has no such reason to stay there. It is here
because it is why I understand this problem: I invested through that period
and exited in 2023, and the calculation I was making by hand — is this
dividend worth more than a deposit — is the one this tool performs.

## Why solving it is valuable

The promise here is not that a validation check will make anyone's
investments rise. It won't, and a tool that implied otherwise would be
selling the same certainty this one exists to question. What it does is
narrower: it puts the evidence in front of the investor before the
decision, and leaves the decision with them.

What makes that worth doing is that the claims circulating in this market
are rarely false. A company really did declare a 30% dividend — in 2078/79,
three years before the claim that quotes it. The sector's profit really did
rise 32%. Deposit rates really did reach 15%. Every figure survives
checking. What is missing is the qualifier that gives it meaning — the
fiscal year the 30% belongs to, and that a dividend is a percentage of par
value rather than of the market price, which makes this year's 12.50% a
yield of 2.31% on what you actually pay; 32% for the sector rather than for
that company; 15% on remittance deposits rather than ordinary ones. The
claim is true and the conclusion does not follow from it, and from the
inside those two situations feel identical.

The evidence that would settle any of this is public and free. What is
missing is the hour it takes to open a hundred-page annual report and find
the relevant line. Someone in a full-time job does not have that hour, so
the check does not happen — not through ignorance, but because verifying
costs more than the decision appears to be worth. Closing that gap will not
make anyone a better investor. It makes them an investor who knows what
they are deciding on.

## Setup and usage

See REPRODUCE.md.

## Agent instructions

The instruction sent to the model is defined as the `INSTRUCTION` constant
at the top of each script, so it can be read without running anything.

- `baseline.py` — a single sentence: "Assess whether this investment claim
  is supported. Explain your reasoning." Nothing else is sent.
- `agent.py` — the same task, plus the required JSON schema and four rules:
  every figure must come from the source documents, anything absent is
  marked `not_found` rather than estimated, arithmetic must be shown, and
  the system never advises buying or selling.

`agent.py` imports `MODEL` from `baseline.py` so the two runs cannot drift
onto different models.

The source documents the agent reads are in `sources/`, one file per
company plus `macro.md` for the deposit-rate benchmark. Each case in
`cases.json` names the files it is given.

## Tools disclosed

- **Claude Code (Sonnet 5)** — development agent. Built `cases.json`,
  `baseline.py`, `agent.py` and `requirements.txt`, and diagnosed the TLS
  certificate problem. 28–29 August 2026.
- **Gemini API, model `gemini-3.6-flash`** — the runtime model this system
  calls to assess claims. Used identically by the baseline and the agent.
  Not a development tool.
- **Claude (Opus 5), via chat** — problem selection, scoping, review of
  agent output, drafting of documentation, and `check_results.py`.
  28–31 August 2026.
- **Gemini CLI** — used once on 28 August to verify trajectory export
  before the competition began. Not used to build this project.
- **Gemini (free web version)** — used to locate candidate sources for the
  three companies and for background on the market. Its output was treated
  as a lead rather than a finding: every figure was verified against the
  primary source before use, and several of its suggestions did not survive
  that check. One summary it produced cited article titles that do not
  exist. 29 August 2026.

## Evaluation

Three synthetic claims, written by me and modelled on the shape of
investment commentary circulating publicly. My own verdict and reasoning
for each is recorded in `CASES.md`.

Those verdicts were written before either system was run, with one
correction made afterwards: Case 1 was revised once, from the source
document rather than from either system's output. The change and its effect
on the measurements are recorded in `DECISIONS.md` and disclosed in
`REPRODUCE.md`.

How each score is counted, and what it does and does not establish, is set
out at the top of `CHANGELOG.md`. The per-case timings and token counts can
be recomputed from the result files with `check_results.py`.

## Improvement changelog

See CHANGELOG.md.

## Main failure mode

_To be written after the final iteration._

## Hot take

_To be written._

## What existed before this competition

The repository was created on 27 August 2026, before kickoff, with a single
commit containing four files: a throwaway `fib.py`, a `.gitignore`, a
`.gitattributes` created automatically by the git client, and a Gemini CLI
trajectory export. All four existed only to confirm that the toolchain
worked and that agent traces could be exported before the competition began.

That trajectory file has since been renamed to
`trajectory-00-gemini-setup-test.json` for clarity. The rename is visible in
the commit history.

The original planning brief, written on the evening of 28 August before the
market was chosen, is preserved unedited as `PLAN-2026-08-28.md`. Where it
diverges from what was actually built, the divergence is the record.

Everything else — the sources, the evaluation cases, both scripts, the
results and every document in this repository — was built between 28 and 31
August 2026. The commit history is timestamped throughout and can be checked
against these dates.