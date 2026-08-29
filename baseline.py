"""Baseline run: Gemini assesses each claim with no tools, no documents, no context.

This is the control condition for the evaluation harness. The model is given only
a fixed instruction and the raw claim text. Whatever it produces here is what a
user gets today by pasting a claim into a chat window. Later runs add source
documents and macro context; the difference between them and this file is the
measure of what the system adds.

The API key is read from the environment variable GEMINI_API_KEY and is never
written to any output file.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# This machine runs Norton, which does TLS interception with its own root CA.
# That CA is in the Windows trust store but not in certifi, so httpx (used by
# the Gemini SDK) fails verification unless it consults the OS store. truststore
# makes the stdlib ssl module do exactly that, for every library in the process.
import truststore

truststore.inject_into_ssl()

from google import genai  # noqa: E402 - must follow inject_into_ssl()

MODEL = "gemini-3.6-flash"

INSTRUCTION = "Assess whether this investment claim is supported. Explain your reasoning."

# Single source of truth for this run's identity. The output filename and the
# "run" label in the JSON both derive from it, so they cannot drift apart.
RUN_NAME = "baseline"

CASES_PATH = Path("cases.json")
RESULTS_PATH = Path("results") / f"{RUN_NAME}.json"


def build_prompt(claim: str) -> str:
    """The instruction, then the claim text. Nothing else."""
    return f"{INSTRUCTION}\n\n{claim}"


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

    results = []
    for case in cases:
        prompt = build_prompt(case["claim"])
        print(f"Running {case['id']} ...", file=sys.stderr)

        started = time.monotonic()
        error = None
        response_text = None
        response_raw = None
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            response_text = response.text
            response_raw = response.model_dump(mode="json")
        except Exception as exc:  # noqa: BLE001 - record whatever the API raised
            error = f"{type(exc).__name__}: {exc}"
        elapsed = time.monotonic() - started

        results.append(
            {
                "id": case["id"],
                "company": case.get("company"),
                "model": MODEL,
                "prompt": prompt,
                "response_text": response_text,
                "response_raw": response_raw,
                "error": error,
                "time_taken_seconds": round(elapsed, 3),
            }
        )

    output = {
        "run": RUN_NAME,
        "description": (
            "Gemini assessing each claim with the instruction only: no tools, "
            "no documents, no context."
        ),
        "model": MODEL,
        "instruction": INSTRUCTION,
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