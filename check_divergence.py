"""Show where the correction loop and the scoring path disagree.

`agent.py` hands `validate_response()` the source files as written, line
breaks intact. `validate.py` hands it the same files with whitespace
collapsed. A quote spanning a line break fails the first and passes the
second, so a run can record violations at the time that vanish when the
finished run is scored afterwards.

This prints both numbers, per attempt, for every run that records attempts.
DECISIONS.md, 30 August 2026, explains what it means and why it is not fixed.

Run from the repo root:  python check_divergence.py
Reads only. No API key, no network, nothing written.
"""

import json
from pathlib import Path

from validate import sources_from_prompt, validate_response

RUNS = ["agent_v1", "agent_v2", "agent_v3", "agent_v4"]

disagreements = 0

for name in RUNS:
    path = Path("results") / f"{name}.json"
    if not path.exists():
        print(f"\n{name}: file not found")
        continue

    cases = json.loads(path.read_text(encoding="utf-8"))["results"]

    # Only Iteration 4 runs the loop, so only those record per-attempt data.
    if not any(case.get("attempts") for case in cases):
        print(f"\n{name}: no per-attempt records -- predates the correction loop")
        continue

    print(f"\n{name}")
    for case in cases:
        for attempt in case.get("attempts", []):
            recorded = attempt.get("violations", [])

            # Score the same response the way validate.py scores a finished run.
            sources = sources_from_prompt(attempt.get("prompt", ""))
            recomputed = validate_response(attempt.get("response_json") or {}, sources)

            differs = len(recorded) != len(recomputed)
            disagreements += differs

            print(
                f"  {case['id']} attempt {attempt['attempt']}: "
                f"loop saw {len(recorded)}, scorer sees {len(recomputed)}"
                f"{'   <-- disagree' if differs else ''}"
            )

print(f"\nattempts where the two paths disagree: {disagreements}")