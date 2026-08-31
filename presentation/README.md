# Presentation

`PRAMAAN.pptx` and `PRAMAAN.pdf` — the slides behind the solution video.
Fourteen slides — a title, an agenda, then the six beats the challenge asks the
video to cover:
the problem and the simple baseline, one execution start to finish, the final
comparison and the changelog, the change that contributed most, and one
experiment removed.

The PDF is a straight export. Read that if you do not have PowerPoint; the
`.pptx` additionally carries speaker notes naming the source file behind each
claim.

## Every figure on these slides comes from this repository

Nothing on the slides is estimated, and nothing was typed from memory. Each
number can be recomputed here without an API key:

| What the slides show | Where it comes from | How to recompute it |
|---|---|---|
| Mean time and mean tokens per run | `results/*.json` | `python check_results.py` |
| Verdict agreement, 3 / 3 / 2 / 3 / 3 | `results/*.json` against `cases.json` | `python check_results.py` |
| Schema violations, 5 / 2 / 4 / 0 | `results/*.json` | `python validate.py` |
| The two Case 3 quotes, and the truncation | `results/agent_v4.json` | open the file; both attempts are stored |
| Line 80 of the sector paragraph | `sources/ebl.md` | open the file |
| Nabil's dividends, price and par value | `sources/nabil.md` | open the file |
| Fixed deposit range, 2.75% to 4.55% | `sources/macro.md` | open the file |
| What the baseline invented | `results/baseline.json` | open the file |
| The loop-on / loop-off control | `results/agent_v5.json` | `python check_results.py` |
| The runtime / scorer divergence | `results/agent_v4.json` | `python check_divergence.py` |

Where a slide states a limit — three evaluation cases, one attribution case, no
user, five defects shipped unfixed — the fuller version is in `README.md` under
*Main failure mode* and in `DECISIONS.md`.

## One thing the slides say that the changelog says more carefully

The comparison slide (slide 9) separates two questions that are easy to
conflate:

- **Biggest change from the baseline** is traceability, 0/3 to 3/3.
- **Biggest change across the iterations** is schema violations, 5 to 0 — which
  is *not* a comparison against the baseline, because the baseline returns free
  text and has no schema to break. `CHANGELOG.md` records that in the baseline
  row.

The deck is a summary. Where it and the changelog differ in detail, the
changelog and the result files are the record.
