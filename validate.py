"""Check whether an agent response obeys the schema it was asked for.

The instruction tells the model what shape to return. Nothing has ever
verified that it did. This module does, using three rules that are
mechanically checkable:

  1. status must be one of verified, contradicted, not_found
  2. quote must appear in the source file it names
  3. every number in source_figure must appear inside its own quote

Rule 2 checks against the source text recorded in the run's own prompt,
not against the files currently on disk. Iteration 2 replaced those files,
so checking an older run against today's sources would fail it for quotes
that were correct when it made them.

Rule 3 checks numbers rather than the whole string, because the model
often adds a descriptive gloss -- "32.33% (sector combined profit)" -- and
the gloss is not a claim about the source. The numbers are.

Run it directly to check the result files in results/. It reads only --
no API key, no network, nothing written.

agent.py imports validate_response() so the same rules that score a run
can also correct one.
"""

import json
import re
import sys
from pathlib import Path

VALID_STATUSES = {"verified", "contradicted", "not_found"}

RUNS = ["agent_v1", "agent_v2", "agent_v3", "agent_v4", "agent_v5"]

# Matches numbers with optional thousands separators and decimals: 729.50,
# 4,839,903,472, 32.33, 2081.
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def normalise(text: str) -> str:
    """Collapse whitespace so formatting differences do not cause false
    failures. Content differences still do."""
    return re.sub(r"\s+", " ", text).strip()


def sources_from_prompt(prompt: str) -> dict[str, str]:
    """Recover each source document from the prompt as it was actually sent.

    agent.py writes them as:  --- sources/nabil.md ---\\n<text>
    """
    section = prompt.split("=== SOURCE DOCUMENTS ===", 1)
    if len(section) < 2:
        return {}
    body = section[1].split("=== CLAIM ===", 1)[0]

    blocks = re.split(r"---\s+(\S+\.md)\s+---", body)
    # re.split returns [before, name1, text1, name2, text2, ...]
    return {
        blocks[i]: normalise(blocks[i + 1])
        for i in range(1, len(blocks) - 1, 2)
    }


def validate_response(response_json: dict, sources: dict[str, str]) -> list[str]:
    """Return a list of rule violations. Empty means the response obeys the
    schema. `sources` maps each source filename to its full text."""
    violations = []

    if not isinstance(response_json, dict):
        return ["response is not a JSON object"]

    for i, assertion in enumerate(response_json.get("assertions", []), start=1):
        status = assertion.get("status")
        quote = assertion.get("quote")
        figure = assertion.get("source_figure")
        named_file = assertion.get("source_file")

        # Rule 1 -- the status must be one the schema permits.
        if status not in VALID_STATUSES:
            violations.append(
                f"assertion {i}: status {status!r} is not one of "
                f"{sorted(VALID_STATUSES)}"
            )

        # Rule 2 -- the quote must appear in the file it names.
        if quote:
            if named_file not in sources:
                violations.append(
                    f"assertion {i}: source_file {named_file!r} is not one of "
                    f"the files supplied for this case"
                )
            elif normalise(quote) not in sources[named_file]:
                violations.append(
                    f"assertion {i}: quote does not appear in {named_file}"
                )

        # Rule 3 -- every number in the figure must appear in its own quote.
        if figure:
            numbers = NUMBER.findall(str(figure))
            if numbers and not quote:
                violations.append(
                    f"assertion {i}: source_figure {figure!r} is offered with "
                    f"no quote"
                )
            elif numbers:
                quoted = normalise(quote)
                missing = [n for n in numbers if n not in quoted]
                if missing:
                    violations.append(
                        f"assertion {i}: figure(s) {', '.join(missing)} do not "
                        f"appear in the quote offered for them"
                    )

    return violations


def check_run(name: str) -> None:
    """Report violations for every case in one result file."""
    path = Path("results") / f"{name}.json"
    if not path.exists():
        print(f"\n{name}: file not found")
        return

    cases = json.loads(path.read_text(encoding="utf-8"))["results"]
    total = 0

    print(f"\n{name}")
    for case in cases:
        response_json = case.get("response_json")
        if response_json is None:
            print(f"  {case['id']}: no structured output -- not checkable")
            continue

        sources = sources_from_prompt(case.get("prompt", ""))
        violations = validate_response(response_json, sources)
        total += len(violations)

        if violations:
            print(f"  {case['id']}: {len(violations)} violation(s)")
            for v in violations:
                print(f"      {v}")
        else:
            print(f"  {case['id']}: clean")

    print(f"  total violations: {total}")


if __name__ == "__main__":
    for run in RUNS:
        check_run(run)
    sys.exit(0)