"""Grounded run with a validation loop.

This is the treatment condition, the counterpart to baseline.py. The structure
is deliberately identical so the result files line up case for case. The only
differences are what the model receives and what it is asked to return:

  baseline.py -> instruction + claim, free-text explanation
  agent.py    -> instruction + source documents + claim, structured JSON

Every figure in the answer must be traceable to a line in the source documents.
The difference between this run's output and results/baseline.json is the
measure of what grounding adds.

Since Iteration 4 the response is checked before it is accepted. validate.py
applies three mechanical rules -- permitted status, quote present in the file
it names, figures present in their own quote. A response that breaks any of
them is sent back with the violations named, up to MAX_ATTEMPTS times. Every
attempt is recorded, with its own token count, so both the correction and its
cost are visible in the evidence rather than hidden behind a clean final
answer.

The API key is read from the environment variable GEMINI_API_KEY and is never
written to any output file.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Same TLS handling as baseline.py: this machine runs Norton, which does TLS
# interception with its own root CA. That CA is in the Windows trust store but
# not in certifi, so httpx (used by the Gemini SDK) fails verification unless it
# consults the OS store. truststore makes the stdlib ssl module do that.
import truststore

truststore.inject_into_ssl()

from google import genai  # noqa: E402 - must follow inject_into_ssl()
from google.genai import types  # noqa: E402

# Imported from baseline.py so the two runs cannot drift apart on model choice.
from baseline import MODEL  # noqa: E402

# The same rules that score a finished run also correct a running one.
from validate import validate_response  # noqa: E402

INSTRUCTION = """\
You are checking whether an investment claim is supported by a company's own \
filings. You are given a set of SOURCE DOCUMENTS and then a CLAIM.

Work only from the source documents. Then return a single JSON object, and \
nothing else, in exactly this shape:

{
  "verdict": "supported | partly supported | unsupported",
  "assertions": [
    {
      "claim_text": "the specific assertion being checked",
      "status": "verified | contradicted | not_found",
      "source_figure": "the actual figure from the source documents",
      "quote": "the exact line from the source document",
      "source_file": "which file it came from"
    }
  ],
  "computed": {"any calculation performed, showing the arithmetic"},
  "summary": "two or three sentences for a retail investor"
}

Rules:
- Break the claim into its separate assertions and check each one.
- Every figure must come from the source documents. Do not use general \
knowledge about these companies.
- If a figure is not in the sources, mark it not_found rather than estimating \
it.
- Where a claim compares against a benchmark that varies by tenure, category \
or period, do not mark it verified because one row matches. State the full \
range across the sources, name the specific rate you are comparing against, \
and say why that one.
- Before assessing a claim that depends on a ratio — a yield, a payout, a \
price to book, a growth rate — compute it from the published figures and show \
the arithmetic. Do not assess the claim without it.
- Show the arithmetic for anything computed, e.g. "1200 / 40000 = 0.03 = 3%".
- "status" must be exactly one of verified, contradicted or not_found. Nothing \
else is permitted in that field.
- Every number you put in "source_figure" must appear in the "quote" you give \
beside it. If one quoted line cannot support the whole figure, quote the line \
that can, or reduce the figure to what the quote supports.
- If "computed" has no entries, return it as an empty object {}.
- Never advise buying or selling. Describe what the evidence shows and stop.\
"""

# Single source of truth for this run's identity. The output filename and the
# "run" label in the JSON both derive from it, so they cannot drift apart.
RUN_NAME = "agent_v4"

# One initial attempt plus this many corrections before giving up.
MAX_ATTEMPTS = 3

CASES_PATH = Path("cases.json")
RESULTS_PATH = Path("results") / f"{RUN_NAME}.json"


def load_sources(paths: list[str]) -> dict[str, str]:
    """Read each source file, keyed by its path as the agent will see it."""
    return {rel: Path(rel).read_text(encoding="utf-8") for rel in paths}


def build_sources_block(sources: dict[str, str]) -> str:
    """Concatenate the source files, each under its own header."""
    return "\n\n".join(
        f"--- {rel} ---\n{text.strip()}" for rel, text in sources.items()
    )


def build_prompt(sources_text: str, claim: str) -> str:
    """Instruction, then the source documents, then the claim."""
    return (
        f"{INSTRUCTION}\n\n"
        f"=== SOURCE DOCUMENTS ===\n\n{sources_text}\n\n"
        f"=== CLAIM ===\n\n{claim}"
    )


def build_correction(prompt: str, previous: str, violations: list[str]) -> str:
    """Re-send the original task with the failed response and what was wrong
    with it. Naming the violations is the point: a bare 'try again' gives the
    model nothing to act on."""
    listed = "\n".join(f"- {v}" for v in violations)
    return (
        f"{prompt}\n\n"
        f"=== YOUR PREVIOUS RESPONSE ===\n\n{previous}\n\n"
        f"=== SCHEMA VIOLATIONS IN THAT RESPONSE ===\n\n{listed}\n\n"
        "Return a corrected JSON object of the same shape. Fix every violation "
        "listed above. Do not change any verdict or assertion that was not at "
        "fault."
    )


def main() -> int:
    # Each results file is evidence for a row in the changelog. Refuse to
    # overwrite one: a lost run leaves a claim with nothing behind it.
    if RESULTS_PATH.exists():
        print(
            f"{RESULTS_PATH} already exists. Change RUN_NAME or move the old file aside.",
            file=sys.stderr,
        )
        return 1

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY is not set in the environment.", file=sys.stderr)
        return 1

    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(response_mime_type="application/json")

    results = []
    for case in cases:
        source_files = case.get("sources", [])
        sources = load_sources(source_files)
        prompt = build_prompt(build_sources_block(sources), case["claim"])
        print(f"Running {case['id']} ...", file=sys.stderr)

        attempts = []
        current_prompt = prompt
        response_text = None
        response_json = None
        response_raw = None
        error = None
        started = time.monotonic()

        for attempt_no in range(1, MAX_ATTEMPTS + 1):
            try:
                response = client.models.generate_content(
                    model=MODEL, contents=current_prompt, config=config
                )
                response_text = response.text
                response_raw = response.model_dump(mode="json")
            except Exception as exc:  # noqa: BLE001 - record whatever was raised
                error = f"{type(exc).__name__}: {exc}"
                break

            try:
                response_json = json.loads(response_text)
            except json.JSONDecodeError:
                response_json = None

            violations = (
                validate_response(response_json, sources)
                if response_json is not None
                else ["response was not valid JSON"]
            )

            attempts.append(
                {
                    "attempt": attempt_no,
                    "prompt": current_prompt,
                    "response_text": response_text,
                    "response_json": response_json,
                    "violations": violations,
                    # Recorded per attempt: the loop can make several calls,
                    # and the cost of a corrected answer is all of them, not
                    # just the last.
                    "total_tokens": (response_raw or {})
                    .get("usage_metadata", {})
                    .get("total_token_count"),
                }
            )

            if not violations:
                print(f"  attempt {attempt_no}: clean", file=sys.stderr)
                break

            print(
                f"  attempt {attempt_no}: {len(violations)} violation(s)",
                file=sys.stderr,
            )
            if attempt_no < MAX_ATTEMPTS:
                current_prompt = build_correction(prompt, response_text, violations)

        elapsed = time.monotonic() - started

        results.append(
            {
                "id": case["id"],
                "company": case.get("company"),
                "model": MODEL,
                "source_files": source_files,
                "prompt": prompt,
                "attempts": attempts,
                "attempts_used": len(attempts),
                "total_tokens_all_attempts": sum(
                    a["total_tokens"] or 0 for a in attempts
                ),
                "final_violations": attempts[-1]["violations"] if attempts else None,
                "response_text": response_text,
                "response_json": response_json,
                "response_raw": response_raw,
                "error": error,
                "time_taken_seconds": round(elapsed, 3),
            }
        )

    output = {
        "run": RUN_NAME,
        "description": (
            "Gemini assessing each claim against the company's filings plus "
            "macro context, required to return structured JSON with a source "
            "quote for every figure, with the response validated and returned "
            "for correction when it breaks the schema."
        ),
        "model": MODEL,
        "instruction": INSTRUCTION,
        "max_attempts": MAX_ATTEMPTS,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cases_file": str(CASES_PATH),
        "results": results,
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {RESULTS_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())