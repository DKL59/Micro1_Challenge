# NEPSE Claim Validator

A tool that checks whether an investment claim circulating publicly is
actually supported by the company's published results and current market
conditions. It does not tell anyone what to buy.

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

I invested on NEPSE from 2021 to 2023, trading mostly on
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
now. Deposit rates today run from 2.75% to 4.55% on ordinary individual
deposits, and up to 5.55% on remittance-linked ones, and the money that
left the market for the banks has no such reason to stay there. It is here
because it is why I understand this problem: the calculation I was making
by hand — is this dividend worth more than a deposit — is the one this tool
performs.

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

One thing to be clear about: this is an evaluation harness, not a product.
Checking a new claim means adding it to `cases.json` and assembling the
source file it should be checked against. There is no interface, and the
person described above could not use it as it stands. What the weekend
bought was evidence that the method works and a measurement of what it
costs — not something anyone can pick up.

## Agent instructions

The instruction sent to the model is defined as the `INSTRUCTION` constant
at the top of each script, so it can be read without running anything.

- `baseline.py` — a single sentence: "Assess whether this investment claim
  is supported. Explain your reasoning." Nothing else is sent.
- `agent.py` — the same task, plus the required JSON schema and a set of
  rules: break the claim into separate assertions and check each one; every
  figure must come from the source documents; anything absent is marked
  `not_found` rather than estimated; where a claim compares against a
  benchmark that varies by tenure, category or period, state the full range
  and name the specific rate being compared against rather than marking it
  verified because one row matches; compute any ratio the claim turns on
  before assessing it; show the arithmetic; use only the three permitted
  status values; every number in a figure must appear in the quote beside
  it; and never advise buying or selling.

`agent.py` imports `MODEL` from `baseline.py` so the two runs cannot drift
onto different models.

Since Iteration 4 the response is not simply accepted. `validate.py` applies
three mechanical rules to every assertion — the status must be permitted, the
quote must appear in the source file it names, and every number in a figure
must appear inside its own quote. A response that breaks any of them is sent
back with its violations named, up to three attempts. Every attempt is
recorded in the result file with its own token count, so a correction is
visible in the evidence rather than hidden behind a clean final answer.

The source documents the agent reads are in `sources/` — one file per
company plus `macro.md` for the deposit-rate benchmark — and contain only
published figures, each with the URL it came from. Each case in `cases.json`
names the files it is given. My own analysis of those figures — computed
yields, cross-checks, conclusions — lives in `notes/`, which the agent never
sees. That split was made after Iteration 1 showed the agent quoting my
conclusions back as evidence. `notes/README.md` records what moved and why.

## Tools disclosed

- **Claude Code (Sonnet 5)** — development agent. Built the first versions
  of `cases.json`, `baseline.py`, `agent.py` and `requirements.txt`, and
  diagnosed the TLS certificate problem. 28–29 August 2026.
- **Gemini API, model `gemini-3.6-flash`** — the runtime model this system
  calls to assess claims. Used identically by the baseline and the agent.
  Not a development tool.
- **Claude (Opus 5), via chat** — problem selection, scoping, review of
  agent output, drafting of documentation, `check_results.py`, `validate.py`,
  the overwrite guards in both scripts, the Iteration 2 rewrite of `sources/`
  and `notes/`, the instruction rules added in Iterations 3 and 4, and the
  validation loop. 28–31 August 2026.
- **Gemini CLI** — used once on 28 August to verify trajectory export
  before the competition began. Not used to build this project.
- **Gemini (free web version)** — used to locate candidate sources for the
  three companies and for background on the market. Its output was treated
  as a lead rather than a finding: every figure was verified against the
  primary source before use, and several of its suggestions did not survive
  that check. One summary it produced cited article titles that do not
  exist. 29 August 2026.

Session transcripts for the coding agent are in `trajectories/`, with a
manifest explaining what each file covers, why the chat-based work has no
tool-call trajectory, and recording one redaction.

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
out at the top of `CHANGELOG.md`. Two of the four metrics are recomputable
from the result files without an API key: `check_results.py` gives per-case
timings, token counts and verdict agreement; `validate.py` gives the schema
violation count for any run.

## Improvement changelog

See CHANGELOG.md.

## Main failure mode

The system can now prove a citation is well-formed. It cannot tell whether
the citation is apt.

Since Iteration 4, every quote in the final run exists in the file it names,
and every number in a figure appears in the quote beside it. That is checked
in code before the answer is accepted, not requested in a prompt and hoped
for. The violation count went from four to zero.

What the validator cannot check is whether the quoted line actually supports
the assertion made about it. Iteration 3 produced this on Case 2: it marked
"Bonus shares provide free shares to investors." as **contradicted** and
quoted the row showing NIC Asia paid no dividend in 2081/2082. That row is
real, it is in the named file, and the figure quoted appears in it. It passes
all three rules. It also does not address the claim, which is about what a
bonus share is, not about whether this company issued one.

So the guarantee is narrower than it looks. Every figure offered as coming
from a source is traceable, and none is invented. Two things sit outside it.
Whether the traced line is the *right* line remains a human judgement. And
the `computed` block is not checked at all — the validator reads only the
assertions, so an arithmetic error in the calculation that decides a case
would pass every rule. That one is mechanically checkable and simply is not
checked.

Two further questions are open. The model still breaks its own schema on the
first attempt — two of three cases needed correcting in the final run — so
the loop is repairing behaviour rather than the model getting it right. And
Iteration 4 changed two things at once, the loop and two instruction rules,
so how much of the zero belongs to the loop is not established. The control
run that would settle it is written and waiting on a quota reset.

The next steps are of very different kinds. Checking the arithmetic in
`computed` is a few lines of code and would close the gap above. Checking
whether a quote is responsive to the assertion it is offered for cannot be
done mechanically at all — it needs a second model to judge it, which is a
different system with a different set of failure modes, including the obvious
one that it would be a model grading a model.

## Hot take

Grounding a model in documents does not make it verify things. It makes it
quote things. Those look identical in the output and they are not the same
capability, and the difference is invisible unless you go looking for it.

This project scored 1 out of 1 on catching a planted attribution error and I
believed it for most of a day. Then I read the evidence file and found the
agent had quoted a sentence I had written into the source myself, under a
heading that named the check it was performing. I had graded a system on
whether it could find an answer I had already given it.

So here is the test I would apply to any retrieval-augmented system, my own
included: remove your conclusions from the corpus and run it again. Whatever
survives is the capability. Whatever disappears was your own work, reflected
back at you. When I did that, the attribution catch held and a verdict I was
proud of fell over. Iteration 3 earned it back, with two rules that made the
agent do the arithmetic instead of reading it off a page I had written.

The same lesson applied again one level up. When I finally built something to
check whether the output obeyed its own schema, it turned out three
iterations had been quietly breaking it — five violations, then two, then
four — and nobody had noticed, because nothing had ever looked. A rule stated
in a prompt is a request. Only code makes it a contract.

And one thing I did not expect. Every wrong number in this project's
documentation was put there by a human. The 30% dividend, the 2-out-of-3
baseline score, the count of contaminated quotes — each was asserted by me
or by my assistant without opening the file it came from, and each was
caught only by opening it. The model invented figures too; the baseline run
is a record of exactly that. But it never did so with a source in front of
it. Given a source, it cited the source. Given a deadline, we guessed.

## What existed before this competition

The repository was created on 27 August 2026, before kickoff, with a single
commit containing four files: a throwaway `fib.py`, a `.gitignore`, a
`.gitattributes` created automatically by the git client, and a Gemini CLI
trajectory export. All four existed only to confirm that the toolchain
worked and that agent traces could be exported before the competition began.

That trajectory file has since been renamed to
`trajectory-00-gemini-setup-test.json` and moved into `trajectories/`. Both
changes are visible in the commit history.

The original planning brief, written on the evening of 28 August before the
market was chosen, is preserved unedited as `PLAN-2026-08-28.md`. Where it
diverges from what was actually built, the divergence is the record.

Everything else — the sources, the evaluation cases, both scripts, the
results and every document in this repository — was built between 28 and 31
August 2026. The commit history is timestamped throughout and can be checked
against these dates.