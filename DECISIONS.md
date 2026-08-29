## 28 Aug 2026, late evening — Which market

**Decision:** [NEPSE / US-listed via EDGAR]

**Options considered:** NEPSE, where I have two years of retail
investing experience, versus US-listed companies, where filings are
free and machine-readable through EDGAR.

**Why:** [what you actually find tonight about filing availability]

**Overruled:** [if applicable]

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
decline, which is why I exited my own positions in 2021. A US
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

**Decision:** The agent retrieves the current commercial bank fixed
deposit rate at runtime and uses it as the benchmark for any
dividend yield claim. It is never stored as a constant in the code.
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

**Decision:** keep every workaround outside the project. No
certificate paths in code, none in requirements.txt. The fix lives
in my shell and is documented in REPRODUCE.md as an environment
note, so the project stays portable to a machine without this issue.

**Resolution:** [fill in once fixed]

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

Measured against my own assessments it scored 2 of 3 on verdict
agreement, 0 of 3 on figures traceable to a source, and 0 of 1 on
catching the attribution error. Mean 15.8 seconds and about 1,832
tokens per case.

Three gaps came out of that.

**Verification.** Every number the baseline produced was invented. It
guessed a market price of "NPR 600 or more" and concluded the yield
"might only be 3% to 5%". The reasoning was sound and the figures
were illustrative.

**Attribution.** On the challenging case it reached the right verdict
for entirely different reasons than mine — value trap risk, earnings
quality, misuse of "blue chip" — and never caught that the 32%
belongs to the sector rather than to EBL. It could not, and it said
so: the claim "cannot be fact-checked" without identifying the
source.

**Discrimination.** On the Nabil case I judged the claim partly
supported, because the 30% dividend is genuine — a true figure inside
a misleading frame. The baseline called the whole claim unsupported.
It cannot separate the accurate part from the misleading part, so it
condemns everything. For a real user that is its own failure: being
told "this is all wrong" teaches nothing and invites them to stop
listening.

**Consequence for the design:** the agent must retrieve the filing
and state the actual declared dividend, the actual market price, the
computed yield and today's actual deposit rate rather than guessed
ones. It must check whose figure a number belongs to. It must
separate what is true in a claim from what is misleading about it.
And every claim it makes must cite the passage it came from.

Baseline: "your yield might be around 5%."
Agent: "Nabil declared X, the share trades at Y, the yield is Z, and
here is the page it came from."

**Overruled:** My own assumption, and my assistant's, that a stronger
prompt or more thorough reasoning would be the improvement. The
evidence says otherwise. Had I not run the baseline before building
the agent, I would have spent the weekend optimising the wrong axis.

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