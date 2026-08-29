# Improvement Changelog

How the solution evolved, from the simple baseline through to the final result.

**How these are measured.** Three cases, scored by hand against the result
files.

- **Verdict agreement (out of 3)** — does the system's overall verdict match
  the verdict I recorded in CASES.md for that case.
- **Figures traceable to a source (out of 3)** — for a case to count, every
  figure the system reports must name the source file it came from and quote
  a line that actually appears in that file. A case with one invented number
  scores zero. This measures traceability to the supplied source file, not
  that the quoted line is itself published data. Iteration 1 records where
  those two diverged. A case in which the system reports no figures scores
  trivially, having nothing to invent — Case 2 in Iteration 1 is such a case,
  which is why the failure is recorded alongside the score rather than hidden
  by it.
- **Attribution errors caught (out of 1)** — only Case 3 contains a planted
  attribution error: a correctly quoted sector figure presented as the
  company's own. There is one opportunity to catch it, so the denominator is
  one. Read the Iteration 1 caveat before relying on this score.

Scoring is my own judgement against the recorded verdicts in CASES.md, on
three cases. That is enough to show a difference this large and not enough to
estimate its size. I have reported it as a difference, not a percentage.

| Stage | What I tried and why | Evidence | Decision / Learning |
|---|---|---|---|
| Baseline | Single fixed prompt to gemini-3.6-flash with the claim text only — no documents, no market data, no tools. This is what a user gets today by pasting a claim into a chat window. | `results/baseline.json` — verdict agreement 3/3, figures traceable to a source 0/3, attribution errors caught 0/1, mean 15.8s and ~1,832 tokens per case | The baseline reasons soundly from general financial principles and reached the correct verdict on all three cases. It caught the par value versus market price conflation unprompted, showed why bonus shares are value-neutral, and rejected "guaranteed income". But it verifies nothing. It guessed a market price of "NPR 600 or more" and a yield of "3% to 5%", and it accepted the claim's 30% dividend figure, which the sources contradict — Nabil declared 12.50%. The guess was not merely imprecise but wrong in direction: it concluded the yield was "very close to the 4% FD rate" when the real figure, 12.50/540.20 = 2.31%, sits below the 2.75% floor of the current deposit range. It did the same on Case 3, building a value-trap argument on the claim's "below book value" premise when EBL trades at 2.96 times book. The pattern holds across all three cases: the baseline accepts every figure it is given and argues only about what the figures mean. On the challenging case it reached the right verdict for entirely different reasons than mine and stated plainly that the claim "cannot be fact-checked" without the source. Verdict agreement therefore does not distinguish a grounded system from an ungrounded one. Two real gaps: verification and attribution. |
| Iteration 1 — grounding | Gave the agent the company's published figures and the deposit-rate benchmark, and required structured output: a verdict, each assertion marked verified, contradicted or not_found, with the source quote and file for every figure. Model, cases and instruction otherwise identical — agent.py imports MODEL from baseline.py so the two runs cannot drift onto different models. | `results/agent_v1.json` — verdict agreement 3/3 (unchanged), figures traceable to a source 3/3 (up from 0/3), attribution errors caught 1/1 (up from 0/1, but see caveat), mean 16.4s and ~5,338 tokens per case | Verdicts did not move, and that is the finding. Both systems answer correctly; only one can show why. The agent found "Cash dividend: 12.50%" and marked the claim's 30% as contradicted, where the baseline had accepted it. It reported the yield as 12.50 / 540.20 = 2.31% and rejected Case 3's "below book value" premise with a price-to-book of 2.96x — both taken from the source rather than guessed, though both were arithmetic already present in the file rather than performed by the agent. Then the caveats, and they are heavy. Only one of the six substantive quotes — "Cash dividend: 12.50%" — is a published figure. The other five are lines I composed, because the source files mix figures with conclusions: a deposit range synthesised from three rate cards, two conclusions about Nabil's yield, the sector-attribution paragraph, and a computed price-to-book. Two of those five are arithmetic the agent could have derived from the published figures itself; three are conclusions it read rather than reached. Case 3 is the worst instance: the agent's attribution finding quotes the sentence "That figure belongs to the sector, not to EBL, and covers a different period from EBL's 2081/82 annual results", which I had written into sources/ebl.md under a heading reading "Sector context — required for the attribution check". I wrote the answer into the file and signposted it. The 1/1 therefore measures retrieval, not detection, and must not be read as evidence that the agent finds an attribution error unaided. Two further defects. On Case 1 the fourth assertion pairs the figure "Dividends declined from 48.00% to 12.50%" with the quote "the share carries price risk a deposit does not", which does not contain that figure — the metric as defined does not catch a mismatch between a figure and the quote offered for it. And one quote silently drops the source's bold markers, so it is not verbatim and would fail a mechanical check. Case 2 returned all three assertions as not_found, two with "N/A" as the quote, and cited the heading "Not yet sourced" as though it were a finding. Its summary does state that no dividend was paid in the last two fiscal years, so that evidence was read but never reached the structured output; the 84% profit fall is absent entirely. Cost: 2.9x the baseline's tokens. Iteration 2 exists to answer what this run cannot: strip the conclusions out of the sources, leaving published figures and the raw sector fact, and re-run. If the attribution error still surfaces, the finding is real. If it does not, that is an honest negative result about the limits of grounding alone. |
| Iteration 2 | | | |
| Iteration 3 | | | |
| Final | | | |