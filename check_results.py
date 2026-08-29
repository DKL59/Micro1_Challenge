"""Recompute the headline figures directly from the result files.

Everything in CHANGELOG.md that is an average was worked out by hand. This
prints the same figures from the files themselves, so the changelog can be
checked rather than trusted. It verifies arithmetic only -- verdict agreement
and traceability remain human judgements.
"""

import json
import statistics
from pathlib import Path

# Each run's results file. Add new runs here as they are produced.
RUNS = ["baseline", "agent_v1"]


def summarise(name: str) -> None:
    path = Path("results") / f"{name}.json"
    if not path.exists():
        print(f"{name}: file not found")
        return

    cases = json.loads(path.read_text(encoding="utf-8"))["results"]

    # Structured runs carry a parsed verdict; the baseline returns free text.
    verdicts = [
        (c.get("response_json") or {}).get("verdict", "free text -- read manually")
        for c in cases
    ]
    times = [c["time_taken_seconds"] for c in cases]
    tokens = [c["response_raw"]["usage_metadata"]["total_token_count"] for c in cases]

    print(f"\n{name}  ({len(cases)} cases)")
    for case, verdict in zip(cases, verdicts):
        print(f"  {case['id']}: {verdict}")
    print(f"  mean time:   {statistics.mean(times):.2f}s   {times}")
    print(f"  mean tokens: {statistics.mean(tokens):.1f}   {tokens}")


if __name__ == "__main__":
    for run in RUNS:
        summarise(run)