"""Recompute the headline figures directly from the result files.

Everything in CHANGELOG.md that is an average was worked out by hand. This
prints the same figures from the files themselves, so the changelog can be
checked rather than trusted.

It also scores verdict agreement against the verdicts recorded in cases.json,
for runs that return structured output. The baseline returns free text, so its
verdicts cannot be parsed and remain hand-scored -- the script says so rather
than guessing.

Figures traceable to a source and attribution errors caught are human
judgements and are not scored here. See CHANGELOG.md for how they are counted.
Schema violations are scored separately by validate.py.
"""

import json
import statistics
from pathlib import Path

# Each run's results file. Add new runs here as they are produced.
RUNS = ["baseline", "agent_v1", "agent_v2", "agent_v3", "agent_v4"]

CASES_PATH = Path("cases.json")


def load_expected_verdicts() -> dict[str, str]:
    """Map each case id to the verdict I recorded before the runs."""
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    return {c["id"]: c.get("my_verdict") for c in cases}


def summarise(name: str, expected: dict[str, str]) -> None:
    path = Path("results") / f"{name}.json"
    if not path.exists():
        print(f"\n{name}: file not found")
        return

    cases = json.loads(path.read_text(encoding="utf-8"))["results"]

    times = [c["time_taken_seconds"] for c in cases]

    # Runs with a correction loop record the total across all attempts;
    # earlier runs made one call, so the final response carries the whole cost.
    tokens = [
        c.get("total_tokens_all_attempts")
        or c["response_raw"]["usage_metadata"]["total_token_count"]
        for c in cases
    ]

    print(f"\n{name}  ({len(cases)} cases)")

    agreed = 0
    scorable = 0
    for case in cases:
        want = expected.get(case["id"])
        # Structured runs carry a parsed verdict; the baseline returns free text.
        got = (case.get("response_json") or {}).get("verdict")

        if got is None:
            print(f"  {case['id']}: free text -- not machine-scorable")
            continue

        scorable += 1
        match = "match" if got == want else f"DIFFERS (recorded: {want})"
        if got == want:
            agreed += 1

        # Runs with a correction loop report how many calls each case took.
        used = case.get("attempts_used")
        suffix = f"   [{used} attempt(s)]" if used else ""
        print(f"  {case['id']}: {got} -- {match}{suffix}")

    if scorable:
        print(f"  verdict agreement: {agreed}/{scorable} (machine-checked)")
    else:
        print("  verdict agreement: hand-scored, see CHANGELOG.md")

    print(f"  mean time:   {statistics.mean(times):.2f}s   {times}")
    print(f"  mean tokens: {statistics.mean(tokens):.1f}   {tokens}")


if __name__ == "__main__":
    expected = load_expected_verdicts()
    for run in RUNS:
        summarise(run, expected)