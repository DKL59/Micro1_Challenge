"""Grounded run: Gemini assesses each claim against the company's own filings.

This is the treatment condition, the counterpart to baseline.py. The structure is
deliberately identical so the two result files line up case for case. The only
differences are what the model receives and what it is asked to return:

  baseline.py -> instruction + claim, free-text explanation
  agent.py    -> instruction + source documents + claim, structured JSON

Every figure in the answer must be traceable to a line in the source documents.
The difference between this run's output and results/baseline.json is the
measure of what grounding adds.

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
- Show the arithmetic for anything computed, e.g. "1200 / 40000 = 0.03 = 3%".
- If "computed" has no entries, return it as an empty object {}.
- Never advise buying or selling. Describe what the evidence shows and stop.\
"""

# Single source of truth for this run's identity. The output filename and the
# "run" label in the JSON both derive from it, so they cannot drift apart.
RUN_NAME = "agent_v2"

CASES_PATH = Path("cases.json")
RESULTS_PATH = Path("results") / f"{RUN_NAME}.json"


def load_sources(paths: list[str]) -> str:
    """Concatenate the named source files, each under its own header."""
    blocks = []
    for rel in paths:
        text = Path(rel).read_text(encoding="utf-8")
        blocks.append(f"--- {rel} ---\n{text.strip()}")
    return "\n\n".join(blocks)


def build_prompt(sources_text: str, claim: str) -> str:
    """Instruction, then the source documents, then the claim."""
    return (
        f"{INSTRUCTION}\n\n"
        f"=== SOURCE DOCUMENTS ===\n\n{sources_text}\n\n"
        f"=== CLAIM ===\n\n{claim}"
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
        sources_text = load_sources(source_files)
        prompt = build_prompt(sources_text, case["claim"])
        print(f"Running {case['id']} ...", file=sys.stderr)

        started = time.monotonic()
        error = None
        response_text = None
        response_raw = None
        try:
            response = client.models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
            response_text = response.text
            response_raw = response.model_dump(mode="json")
        except Exception as exc:  # noqa: BLE001 - record whatever the API raised
            error = f"{type(exc).__name__}: {exc}"
        elapsed = time.monotonic() - started

        response_json = None
        if response_text is not None:
            try:
                response_json = json.loads(response_text)
            except json.JSONDecodeError:
                response_json = None

        results.append(
            {
                "id": case["id"],
                "company": case.get("company"),
                "model": MODEL,
                "source_files": source_files,
                "prompt": prompt,
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
            "quote for every figure."
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