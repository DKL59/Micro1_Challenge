# Decision Log

A record of the choices made while building this project, including the ones
that were reversed and why. Entries are in the order they were made.

## 28 Aug 2026, late evening — Which market

**Decision:** NEPSE.

**Options considered:** NEPSE, where I invested personally from 2021
to 2023, versus US-listed companies, where filings are free and
machine-readable through EDGAR.

**Why:** Familiarity with the market, and first-hand familiarity with
the gap this tool addresses. I invested on NEPSE from 2021 to 2023,
trading mostly on technical analysis with some basic fundamental
research. That is exactly the position the tool is built for: someone
reading charts has no way to judge whether a dividend figure is real,
whether a yield beats a deposit, or whose growth number is being
quoted. I know how these claims circulate because I was in the
audience for them, and I know the local conventions that make them
misleading: dividends quoted against Rs 100 par value rather than
market price, bonus shares presented as free money, fiscal years
stated in Bikram Sambat. In a market I had never invested in I would
not have known which claims were worth testing, or what makes them
mislead rather than simply being wrong.

EDGAR would have meant structured filings, an API and no manual
sourcing. NEPSE has no equivalent: results are published as HTML on
company websites and aggregator portals, in inconsistent formats,
with no machine-readable feed. That is why the files in `sources/`
were assembled by hand, with a URL recorded against each individual
figure. I accepted that cost for the familiarity.

**Disclosure:** I hold no positions on NEPSE, including in any of the
three companies used as test cases.

**Overruled:** Not applicable — this was the first decision made.

## 28 Aug 2026, night — Scope boundary: NEPSE only, no claim of generalisation

**Decision:** The system targets NEPSE only. I will not claim it
generalises to other markets.

**Options considered:** Building it market-agnostic, or scoping it
explicitly to NEPSE and stating why it does not transfer.

**Why:** The method transfers — check claims against source
documents, require a citation for every assertion, compare promised
yield against the local risk-free alternative, flag omitted risks.
The parameters do not. Nepali filings do not follow US GAAP or
EDGAR's structure. The macro comparison depends on NRB policy rates
and local deposit rates. Most importantly, NEPSE is long-only: a
retail investor in a downtrend has no instrument to profit from the
decline, which is why I exited my own positions in 2023. A US
investor can short or hedge, so that structural argument does not
hold there.

**Overruled:** Rejected the temptation to claim broad applicability.
Claiming generalisation without evidence would be the same
unsupported-confidence failure this project exists to detect.

## 29 Aug 2026 — Evaluation cases will be synthetic, not real posts

**Decision:** Build the evaluation set from synthetic investment
claims modelled on patterns circulating on NEPSE-focused social
media, rather than collecting real posts from named individuals.
Reframe the material as "investment claims circulating publicly"
rather than "influencer recommendations".

**Options considered:** Collecting real posts from YouTube, Facebook
groups and forums, versus writing synthetic claims based on the
patterns those posts follow.

**Why:** SEBON announced a zero-tolerance policy in July 2026
explicitly targeting finfluencers and unauthorised investment
advice, with licensing requirements and legal action planned. Real
posts would therefore identify individuals potentially exposed to
enforcement, in a submission that micro1 owns and may publish. That
conflicts with ground rule 6 — a legal and ethical use case that
treats people responsibly. Ground rule 7 names synthetic data as an
acceptable and usually easiest option.

Synthetic cases are also better evaluation design: I control the
ground truth by construction, and I can deliberately build the one
challenging case the brief asks for rather than hoping to find one.

**Overruled:** My assistant's original framing had me collecting
real influencer posts. I raised the legality question and checked
SEBON's position; the framing changed as a result.

**Strengthens the problem statement:** the regulator has publicly
identified unverified investment claims as a live harm, so the value
of the problem is now evidenced rather than asserted.

## 29 Aug 2026 — The benchmark rate must be looked up, never hardcoded

**Decision:** The benchmark deposit rate is read from a dated macro
context file at run time and used as the comparison for any dividend
yield claim. It is never written into the code as a constant.
Because rates vary by tenure and by depositor category, the agent
reports the range and names the category it is comparing against,
rather than silently picking one number.

**Options considered:** Hardcoding a representative deposit rate as
a constant, versus reading it from a small macro context file that
is updated with a dated source.

**Why:** While sourcing this figure I found that rates have moved
enormously. In Ashoj 2079 (September 2022) banks held term deposit
rates at 12.133% for individuals, 10.133% for institutions and
13.133% for remittances, with some banks offering as much as 15% on
remittance deposits. Those rates held until Poush, then the Nepal
Bankers Association cut them to 11% for individuals and 9% for
institutions from Magh 2079 (January 2023). NIC Asia currently
offers 2.75% to 4.0% depending on tenure, effective Shrawan 2083
(July 2026).

That inverts the verdict. In 2022 a 7% dividend yield lost to a
12.133% deposit and the correct answer was to leave the money in the
bank. In 2026 a 5% yield beats even the 4.0% five-year rate, though
it carries price risk the deposit does not. Same check, opposite
conclusion, purely because the rate regime changed.

Had I hardcoded the rate I remembered, every verdict the system
produced would have been wrong in the same direction.

The spread matters too. A 3.5% dividend yield loses against the 4.0%
five-year rate but beats the 2.75% short-term rate. Picking one
number silently would hide that judgement from the user, so the
agent surfaces the range and names the comparison it is making.

Later widened from one bank to three. The range now used is 2.75% to
4.55% across NIC Asia, Nabil and Everest, with remittance-linked
deposits running to 5.55%. Rates cluster tightly, so one bank was
representative — but a range stated from three sources can be
checked and a range stated from one cannot.

**Overruled:** Both of us, and neither of us was wrong. I wrote that
rates reached 15%, recalling remittance-linked deposits. My
assistant found 12.133% and told me I was mistaken. Both figures
were accurate about different deposit categories. My sentence had
not named the category, and the entire disagreement came from that
one missing qualifier.

The claim was not false. It was unqualified. That is the failure
mode this project exists to catch: almost no misleading investment
claim is a lie. It is a true statement with the qualifier removed —
the tenure, the category, the period, the assumption. It survives
scrutiny in isolation and misleads in context.

**Consequence for the README:** the 2022 mechanism — rising deposit
rates pulling money out of NEPSE — is history, not an explanation of
current conditions. It will be presented as background that explains
why I understand this problem, not as a claim about 2026.

**Sources**

- Ashoj 2079 (September 2022) term deposit rates: 12.133%
  individuals, 10.133% institutions, 13.133% remittances, with some
  banks offering up to 15% on remittance deposits. Held until Poush.
  — ShareSansar
  https://www.sharesansar.com/newsdetail/most-banks-alter-their-interest-rates-individuals-deposit-interest-rates-increased-by-3-digits-after-the-decimal-point-2022-09-21

- Nepal Bankers Association cut to 11% individuals / 9% institutions
  from Magh 2079 (12 January 2023) — ShareSansar
  https://www.sharesansar.com/newsdetail/committee-of-nepal-bankers-association-has-decided-to-decrease-fixed-deposits-interest-rates-for-the-month-of-magh-2023-01-12

- Individual fixed deposit rates 2.75% (shorter terms) to 4.0%
  (five years and above), effective 1 Shrawan 2083 (July 2026)
  — NIC Asia Bank
  https://www.nicasiabank.com/interest-rates/

## 29 Aug 2026 — Environment dependency: TLS interception

**What happened:** pip and the Gemini client both failed with
certificate verification errors. The cause was antivirus software
inspecting HTTPS traffic and substituting its own certificate.

**Why it matters beyond my machine:** the first fix worked when the
coding agent ran it and failed when I ran the same command in my own
PowerShell terminal. "It works on my machine" turned out to mean "it
works in one particular shell on my machine" — which is a sharper
version of exactly what the reproducibility criterion is testing.

**Decision:** nothing machine-specific enters the project. No
certificate file paths, no hostnames, no `--trusted-host`, no
disabled verification. Anything that only makes sense on this laptop
stays in my shell and is documented in REPRODUCE.md as an
environment note.

**Resolution:** the fix is the `truststore` package. It tells Python
to read the operating system's certificate store, where the
intercepting certificate is already trusted. Both `baseline.py` and
`agent.py` call `truststore.inject_into_ssl()` before importing the
SDK, and truststore is pinned in requirements.txt.

The first attempted fix, setting the `SSL_CERT_FILE` environment
variable, did not work. The Gemini SDK uses httpx, which carries its
own bundled certificate list and ignores that variable — which is
why the failure looked intermittent and shell-dependent for the best
part of an hour.

**Overruled:** my own stated decision, one paragraph up. I had said
no workaround would enter the project at all, including
requirements.txt, and truststore is in both the code and the
dependency list. The distinction I had missed is between a
machine-specific workaround and a portable one. A hardcoded
certificate path describes this laptop and breaks everywhere else. A
call to read the operating system's trust store describes no
particular machine: on a laptop without interception it is a no-op,
and it removes a setup step for anyone behind a corporate proxy
rather than adding one. The original rule was aimed at the right
target and drawn in the wrong place.

## 29 Aug 2026 — The pinned model was deprecated mid-project

**What happened:** `gemini-2.5-flash` began returning 404 during the
runs, with a message naming `gemini-3.6-flash` as its replacement. I
replaced the model name and re-ran.

**Decision:** pin the exact model in code and record it in
REPRODUCE.md, while stating plainly that the pin is not a guarantee.

**Why it matters for reproducibility:** the same thing can happen to
a judge. A pinned model is reproducible only for as long as the
provider keeps serving it, and that turned out to be days rather
than years. Recording the model version is still right — without it
nobody can tell whether a different result came from the code or
from the model — but it should not be presented as though it made
the run permanently repeatable.

**Consequence:** REPRODUCE.md names the model under Versions and
states that a retirement would change the results, so a reader meets
that fact before they meet a 404.

## 29 Aug 2026 — Protecting the comparison from drift and from loss

**Decision:** three safeguards. `agent.py` imports `MODEL` from
`baseline.py` rather than declaring its own, so the two runs cannot
drift onto different models. Both scripts refuse to run if their
output file already exists. And `check_results.py` recomputes the
headline timings and token counts directly from the result files,
and scores verdict agreement against the verdicts recorded in
`cases.json`, so the figures quoted in CHANGELOG.md can be checked
rather than trusted.

**Options considered:** declaring the model separately in each
script and remembering to keep them in step; letting each run
overwrite its predecessor; reporting averages worked out by hand.

**Why:** the whole claim of this project is that one number differs
from another because of one change. That claim is worth nothing if
the two runs silently used different models, nothing if the earlier
run's evidence has been overwritten by the later one, and nothing if
the averages themselves were never checked. All three failures are
quiet: none produces an error, and each leaves a plausible-looking
file behind.

The second safeguard came from a near miss. `agent.py` wrote to
`results/agent_v1.json` by default, so re-running it for Iteration 2
would have destroyed the evidence for a changelog row I had just
spent an hour validating. The run name is now a single constant that
the filename and the JSON label both derive from, and an existing
file stops the run before it reaches the API.

The third came from finding two wrong numbers by hand-checking. If
hand arithmetic produced errors twice, it should not be the last
word on any figure a script can recompute. Verdict agreement is now
machine-scored for any run returning structured output; the baseline
returns free text and remains hand-scored, and the script says so
rather than guessing.

**Consequence for the design:** a results file is evidence, not
output. It is never hand-edited and never overwritten. To change
one, re-run the script under a new run name.

## 29 Aug 2026 — The improvement axis is verification, not explanation

**Decision:** The agent's value over the baseline will come from
verifying claims against source documents and live market data, not
from reasoning about them more thoroughly. Every figure the agent
reports must come from a named source and be traceable to it.

**Options considered:** Improving the reasoning through better
prompting, a more capable model, or multi-step analysis, versus
grounding the assessment in retrieved documents and current data.

**Why:** I ran the baseline expecting it to be weak. It was not. With
no documents, no market data and no tools, it identified the par
value versus market price conflation unprompted, showed the
arithmetic for why bonus shares are value-neutral, and rejected
"guaranteed income" correctly.

Measured against my own assessments it scored 3 of 3 on verdict
agreement, 0 of 3 on figures traceable to a source, and 0 of 1 on
catching the attribution error. Mean 15.8 seconds and about 1,832
tokens per case.

That first number is the finding, and it is not the one I expected
to report. Verdict agreement does not distinguish a grounded system
from an ungrounded one. Both reach the right answer on all three
cases. What separates them is whether the answer rests on anything.

Two gaps came out of that.

**Verification.** Every company-specific figure the baseline produced
was invented. It had the Rs 100 par value convention right from
general knowledge, and guessed everything else: a market price of
"NPR 600 or more" and a yield that "might only be 3% to 5%", when the
real figure is 12.50 / 540.20 = 2.31% — below the lowest deposit rate
surveyed. It was right by argument and wrong on the arithmetic, and
it had no way to tell the difference, which means neither does the
user. More precisely: the baseline never disputes a premise. It
accepts every figure in the claim and argues only about what the
figure means.

**Attribution.** On the challenging case it reached the right verdict
for entirely different reasons than mine — value trap risk, earnings
quality, misuse of "blue chip" — and never caught that the 32%
belongs to the sector rather than to EBL. It could not, and it said
so: the claim "cannot be fact-checked" without identifying the
source.

**Consequence for the design:** the agent must retrieve the filing
and state the actual declared dividend, the actual market price, the
computed yield and today's actual deposit rate rather than guessed
ones. It must check whose figure a number belongs to, and separate
what is accurate in a claim from what is misleading about it. And
every claim it makes must cite the passage it came from.

Baseline: "your yield might be around 5%."
Agent: "Nabil declared X, the share trades at Y, the yield is Z, and
here is the page it came from."

**Overruled:** My own assumption, and my assistant's, that a stronger
prompt or more thorough reasoning would be the improvement. The
evidence says otherwise. Had I not run the baseline before building
the agent, I would have spent the weekend optimising the wrong axis.

A third gap was recorded here and later withdrawn. See the entry
below on the ground truth correction.

**Evidence:** results/baseline.json, generated 29 Aug 2026.

## 29 Aug 2026 — Source hierarchy: primary over secondary, and say which

**Decision:** Where a figure exists in more than one place, the agent uses
the primary source — the institution stating its own terms or reporting its
own results — and names which source each figure came from. Where only a
secondary source exists, the output says so.

**Options considered:** Treating all sources as equivalent, versus ranking
them and making the ranking visible in the output.

**Why:** While assembling the benchmark I used three banks' own published
rate cards for current fixed deposit rates, and news reporting for the 2022
historical rates, because banks do not publish historical rate cards. Those
are different classes of evidence and should not be presented as though
they were the same.

A bank's own rate card is the institution stating its terms. A news article
reporting those rates is accurate in most cases but one step removed, and it
can be summarised, rounded or stale. The Investopaper article on NIC Asia
demonstrated the risk directly: it described a company that paid nothing in
four of the last five years as having "provided consistent dividends," which
is defensible across twenty years and misleading about now.

Corroboration between two independent secondary sources is also worth
recording. Nabil's dividend history was confirmed identically by ShareSansar
and Hamroshare, and NIC Asia's by NEPSE and Investopaper. A figure confirmed
twice is stronger evidence than a figure stated once, and the output should
be able to say so.

**Consequence for the design:** every figure in a source file carries its own
URL rather than the file carrying one URL for everything. The agent cites the
specific source behind each number, not the document it happened to find it
in. Where two sources agree, it can say so. Where only secondary reporting
exists, it says that too.

**Overruled:** My assistant compiled the macro file with the historical news
links listed alongside the banks' own rate cards. I queried whether
ShareSansar was being credited for the current rates when those came from the
banks directly. The attribution was correct but the presentation was
ambiguous, and ambiguous attribution is the failure this project exists to
catch.

## 29 Aug 2026 — The ground truth was corrected once, after the runs

**Decision:** Case 1's verdict in CASES.md was revised from "partly
supported" to "unsupported" after both systems had already been run.
Rather than quietly restating the verdicts, I am recording the change,
what caused it, and what it did to the measurements.

**What happened:** the Nabil claim quotes a 30% dividend. I had accepted
that the declared figure was genuine and that the claim was misleading
only in how it framed a true number, so I judged it partly supported.
During the file audit I checked the source. Nabil declared a 12.50% cash
dividend and no bonus shares for FY 2081/2082. The quoted figure is
contradicted by the source for the year the claim is about, and the
verdict became unsupported.

**Why the timing does not invalidate the measurement:** a ground truth
adjusted after seeing results is worthless unless you can say what moved
it. What moved this one was the source document, not either system's
output. The two result files that existed at that point were then
re-scored against the corrected verdict, and both moved identically —
baseline and agent each went from 2 of 3 to 3 of 3 on verdict agreement.
That is confirmed rather than assumed: both files record "unsupported" on
Case 1. The comparison between the two systems is therefore unaffected.
The disclosure is in REPRODUCE.md so that anyone reproducing the numbers
meets it before they meet the scores.

**What it cost:** a finding. I had recorded a third gap, "discrimination"
— that the baseline condemns a whole claim rather than separating the
accurate part from the misleading part — and built it on the assumption
that the 30% was real for the current year. Once the figure was checked,
the gap dissolved. I have removed it rather than leave a conclusion
standing on a premise I never verified. Two gaps, not three.

**Overruled:** myself, and my assistant, who asserted at one point that
Nabil had genuinely declared 30% this year. Neither of us checked it
against the source file that was already sitting in the repository.

**Worth noting:** the error is a figure taken on trust and never traced
to its source — which is the exact failure this project was built to
catch. It survived a day of work on a tool designed to detect it, and
was caught only by a line-by-line audit against the sources.

**Later refinement, before the Iteration 2 run:** auditing the source
files showed that 30.00% is Nabil's actual total dividend for FY
2078/2079 — 18.50% bonus plus 11.50% cash. The claim quotes a real
figure and drops the year. That is recorded in CASES.md. It sharpens
the reasoning and does not change the verdict.

## 29 Aug 2026 — The source files answered the question for the agent

**What happened:** validating results/agent_v1.json line by line, I found
that only one of the six substantive quotes the agent returned is a
published figure. The rest are sentences I wrote. On the challenging case
its attribution finding quotes "That figure belongs to the sector, not to
EBL, and covers a different period from EBL's 2081/82 annual results" — a
sentence sitting in sources/ebl.md under a heading reading "Sector context
— required for the attribution check".

**What that means:** the 1 of 1 on attribution measures retrieval, not
detection. I wrote the answer into the file and signposted it. The agent
found the signpost.

**Options considered:** leaving the sources as they are and reporting the
score with a footnote, versus rebuilding them and re-running with two days
left.

**Decision:** Iteration 2 strips the conclusions out of the source files
into a separate notes/ folder, leaving published figures with their URLs
and the raw sector fact without commentary, and re-runs as agent_v2.
Whatever that produces is the honest result. If the attribution error
still surfaces, the finding stands. If it does not, the negative result
is reported as the finding instead.

**Why:** a caveat does not repair a measurement. Any judge who opens
sources/ebl.md sees that heading, and at that point a footnote reads as
damage control rather than disclosure. It is cheaper to run the
experiment than to defend a number I do not believe.

**Overruled:** my own source-file design. I built those files to be
readable by me and wrote my working into them, and that working then
became the agent's evidence. A grounding corpus is not documentation.
Anything in it that reads like an answer will be returned as one.

**One thing had to replace the signposts rather than simply vanish.**
`sources/nica.md` carried a heading reading "Not yet sourced" above the
absent bonus announcement. Deleting it outright would have made absence
ambiguous — a reader could not tell whether the company announced nothing or
whether I had collected nothing. So each source file now opens with a
coverage line stating what it contains and what it does not. That is metadata
about the corpus, not an answer to a case: it lets the agent reason that a
file covering dividend history but not announcements cannot confirm an
imminent announcement, without being told that conclusion. Iteration 2
confirmed the distinction works — on Case 2 the agent quoted the coverage
line to justify `not_found`.

**Evidence:** results/agent_v1.json, and the caveat recorded against
Iteration 1 in CHANGELOG.md.

## 29 Aug 2026 — A credential was found in a trajectory before it was committed

**What happened:** while collecting the Claude Code session transcripts for
submission, a pattern sweep of the repository found one live Gemini API key
inside `trajectory-03-claude-code-session-3.jsonl`. Claude Code records
everything typed into its terminal, and the key had been set there as an
environment variable.

**Options considered:** dropping that trajectory from the submission,
redacting the single string, or editing the transcript more broadly.

**Decision:** redact the key in the submitted copy, leave everything else in
the transcript untouched, rotate the key, and disclose the redaction in
`trajectories/README.md`.

**Why:** the ground rules require agent trajectories and require credentials
to stay out of the submission. Those two requirements collide the moment a
key touches a terminal an agent is recording. Dropping the file would satisfy
the second rule by breaking the first. Redacting one string satisfies both,
and saying so is what makes the rest of the file trustworthy — a transcript
with an unexplained gap is worth less than one with a labelled one.

**What it says about the process:** the sweep is a checklist step run before
committing, added earlier the same day. It is the only reason this was caught.
Nothing else in the workflow would have surfaced it, and the key had been
sitting in that file since the morning.

**Consequence:** the sweep runs again immediately before submission, not only
before commits.

## 29 Aug 2026 — Iteration 2 result: the finding held, a verdict did not

**The prediction, registered before the run:** if the attribution error still
surfaces once the answer is removed from the source file, the finding stands;
if it does not, the negative result is reported as the finding instead.

**What happened:** it surfaced, and more of it than before. With the
signposted sentence gone, the agent quoted the raw sector line to contradict
"EBL net profit up 32% this quarter", separately quoted "Nabil Bank is
reported as leading the sector" to contradict "best in the sector", and
derived both supporting figures itself — price to book 729.50 / 246.74 =
2.96, and EBL's own growth of 30.69% from the two net profit figures. In
Iteration 1 both numbers were sitting in the file waiting to be copied. The
1 of 1 on attribution now measures detection.

**What it cost:** verdict agreement fell from 3 of 3 to 2 of 3. Case 1 came
back "partly supported" rather than "unsupported", because the agent marked
"Bank FD is giving only 4%" as verified against a single rate-card row — the
5-to-10-year tenure at Nabil — from a range running 2.75% to 4.55% on
ordinary individual deposits. And `computed` came back empty: it never
worked out 12.50 / 540.20 = 2.31%, so the comparison that decides the case
never happened. In Iteration 1 that yield was handed to it.

**Decision:** report both. The score that fell was propped up by my source
files; the score that held is now worth something. A 3 of 3 built on a corpus
that contained the answers is worth less than a 2 of 3 that does not.

**What it revealed:** the agent verified a number and missed the claim. That
is the failure Case 3 was built to test, committed by the agent on Case 1, in
the same run where it caught Case 3 unaided. It is now the system's
documented main failure mode rather than a hypothesis about one.

**Evidence:** results/agent_v2.json, and the Iteration 2 row in CHANGELOG.md.

## 29 Aug 2026 — Iteration 3: change the instruction, not the model

**Decision:** fix the failure Iteration 2 exposed by adding two rules to the
agent's instruction, and change nothing else.

**Options considered:** a stronger model; more source material; multi-step
prompting; or two targeted rules aimed at the specific defect.

**Why:** the defect was specific and diagnosed. The agent marked "Bank FD is
giving only 4%" verified because one rate-card row said 4.00%, and it never
computed the yield the case turns on. Neither is a reasoning capacity the
model lacks — Iteration 2 showed it deriving a price-to-book and a growth
rate unprompted on another case. It simply was not asked. So the cheapest
honest fix was to ask.

**What changed:** two rules. Where a claim compares against a benchmark that
varies by tenure, category or period, state the full range, name the rate
being compared against, and say why that one — rather than marking the claim
verified because a row matches. And before assessing a claim that turns on a
ratio, compute it and show the arithmetic.

**What happened:** verdict agreement returned to 3 of 3, and this time the
reasoning is there to support it. Case 1's computed block contains
12.50 / 540.20 = 2.31%, and the deposit assertion reports the range 2.75% to
5.55% while naming the 4.00% five-to-ten-year rate as the specific comparator.

**What it cost:** 33% more time and 17% more tokens than Iteration 2. It also
introduced two new defects. The prohibition on marking such claims verified
gave the agent nowhere to land, and it returned "partly supported" as an
assertion status — a value the schema does not permit at that level. And the
ratio rule fired mechanically on a case that turns on no ratio, producing a
dividend yield of 0%.

**What that says:** a rule that forbids something must also say what to do
instead. And an instruction is a request, not a contract — nothing in this
system checks that the returned status is one of the three permitted values.
The next change would validate the output rather than add a fourth rule.

**Note on the sequence:** Iteration 2 changed the evidence the system reads,
because the measurement was broken. Iteration 3 changed the system itself,
because the measurement was sound and the system was not. Those are different
kinds of change and the distinction is worth keeping visible.

**Evidence:** results/agent_v3.json, and the Iteration 3 row in CHANGELOG.md.

## 29 Aug 2026 — The planning brief is archived, not updated

**What happened:** `context.md`, written on the evening of 28 August, still
described the project as planned rather than as built. It contradicted the
repository in five places: ten real posts against three synthetic ones, the
wrong metric list, the Gemini CLI as the build tool, the market undecided,
and a description of my own experience that claimed more than the work
supports.

**Options considered:** updating it to match the project, or freezing it as a
dated record and pointing to the current documents.

**Decision:** rename it `PLAN-2026-08-28.md`, add a header stating it is
superseded and listing each divergence with a pointer to where that decision
is recorded, and leave the body untouched — including the parts that turned
out wrong.

**Why:** updating it would create a maintained duplicate. Every fact stated
in two places is a place the repository can contradict itself, and this
project spent a full day repairing exactly that. Freezing it costs nothing
and preserves something the current documents cannot show: what I believed
before the evidence arrived. The divergence between the plan and the outcome
is itself a record that the work followed measurement rather than intention.

**Worth noting:** the header flags that the brief claimed "two years
independent equity research on NEPSE" when the accurate description is two
years of personal investing, mostly on technical analysis. I corrected the
claim in the current documents and left it standing in the archive with the
correction noted. An overstatement quietly deleted teaches nothing.