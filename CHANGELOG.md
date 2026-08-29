# Improvement Changelog

How the solution evolved, from the simple baseline through to the final result.

| Stage | What I tried and why | Evidence | Decision / Learning |
|---|---|---|---|
| Baseline | Single fixed prompt to gemini-3.6-flash with the claim text only — no documents, no market data, no tools. This is what a user gets today by pasting a claim into a chat window. | `results/baseline.json` — verdict agreement with my assessment 2/3 (one over-rejection), figures traceable to a source 0/3, attribution errors caught 0/1, mean 15.8s and ~1,832 tokens per case | The baseline reasons soundly from general financial principles: it caught the par value versus market price conflation unprompted, showed why bonus shares are value-neutral, and rejected "guaranteed income". But it verifies nothing — it guessed a market price of "NPR 600 or more" and a yield of "3% to 5%". On the challenging case it reached the right verdict for the wrong reasons and stated that the claim "cannot be fact-checked" without the source. It also over-rejects: Nabil genuinely did declare 30%, but the baseline condemned the whole claim rather than separating the true figure from the misleading frame. Three measurable gaps: verification, attribution, and discrimination between the accurate and misleading parts of a claim. |
| Iteration 1 | | | |
| Iteration 2 | | | |
| Iteration 3 | | | |
| Final | | | |