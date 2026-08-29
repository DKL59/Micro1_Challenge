# Reproduction Guide

Written for someone starting from a clean machine.

## Setup

1. Install Python 3.10 or later from python.org
2. Clone this repository
3. From the project folder, install dependencies:

    pip install -r requirements.txt

## Required data

All source documents are included in this repository under `sources/`. They
contain published figures for the three companies under test and current bank
deposit rates, each with the URL it came from. No external data needs to be
downloaded.

You need your own Gemini API key. Get one free at aistudio.google.com. The key
is read from an environment variable and is never stored in this repository.

## Before you run anything: the results files are evidence

`results/` already contains the runs this project's claims are based on. Each
script refuses to overwrite an existing results file, so a fresh run will stop
immediately if its output already exists. That is deliberate: a results file
backs a row in CHANGELOG.md, and silently replacing one would leave a claim
with nothing behind it.

To produce your own run without disturbing mine, either move the existing file
aside, or change `RUN_NAME` at the top of the script you are running to a name
of your own. The output filename and the run label inside the JSON both derive
from that one constant.

## Run the baseline

The baseline sends each claim to the model with no documents and no context.

PowerShell:

    $env:GEMINI_API_KEY = "your-key-here"
    python baseline.py

Bash:

    GEMINI_API_KEY="your-key-here" python baseline.py

## Run the solution

The agent sends the same claims together with the source documents, and
requires a source quote for every figure.

Run this in the same terminal session as the baseline, so that
GEMINI_API_KEY is still set:

    python agent.py

Both scripts import the model name from the same place, so the two runs
cannot drift onto different models.

## Run the evaluation

Two parts, because two different kinds of claim are being checked.

The arithmetic is checked by script. This reads the result files and
recomputes the per-case timings and token counts quoted in CHANGELOG.md:

    python check_results.py

It needs no API key and no network, and it writes nothing.

The judgements are checked by hand. Compare the two result files against the
verdicts and reasoning recorded in `CASES.md`. How each score is counted, and
what each one does and does not establish, is set out under "How these are
measured" at the top of CHANGELOG.md.

Those verdicts are my own assessments, written before either system was run,
with one correction made afterwards. Case 1's verdict was revised from
"partly supported" to "unsupported" during a file audit, when checking the
source showed Nabil declared a 12.50% cash dividend rather than the higher
figure I had assumed. The revision came from the source document, not from
either system's output. Both result files were re-scored against the
corrected verdict, and the correction moved both systems equally, so the
comparison between them is unaffected. The change is recorded in
`DECISIONS.md`.

## Expected output

The repository ships with `results/baseline.json` and `results/agent_v1.json`,
the runs behind the figures in CHANGELOG.md.

Each contains, per case: the case id, the exact prompt sent, the full model
response, any error, and the time taken. The agent file additionally contains
the parsed structured output, the source files used, and — inside each
recorded prompt — the full text of the documents the agent was shown.

A fresh run of `agent.py` as shipped writes `results/agent_v2.json`, taken
from `RUN_NAME` at the top of that file.

Both scripts print progress to the terminal and confirm the file written.

## Versions

- Windows 11
- Python 3.12.4
- google-genai 1.29.0
- truststore 0.10.4
- Model: gemini-3.6-flash

The model is pinned, but a pin is not a guarantee. `gemini-2.5-flash` was
retired during this project and began returning 404 mid-run, with a message
naming its replacement. If `gemini-3.6-flash` has since been retired, results
will differ from those recorded here, and the difference will come from the
model rather than from the code.

## Runtime and cost

Three cases per run.

- Baseline: mean 15.8s per case (14.9 / 19.4 / 13.2), about 1,832 tokens
- Agent: mean 16.4s per case (25.8 / 11.4 / 12.1), about 5,338 tokens

The per-case figures are given because with three cases a mean is fragile: the
agent's mean is one slow case pulling two fast ones, and its median is 12.1s,
below the baseline's 14.9s.

Both runs together take under two minutes and sit well within the free tier.

## If you get SSL certificate errors

Some antivirus software and corporate networks inspect HTTPS traffic and
present their own certificate, which Python does not trust by default. On the
machine this was built on, both pip and the Gemini client failed with
CERTIFICATE_VERIFY_FAILED.

Setting SSL_CERT_FILE is not sufficient, because the Gemini SDK uses httpx,
which carries its own bundled certificate list and ignores that variable.

The fix is the `truststore` package, already pinned in requirements.txt. It
makes Python read the operating system's certificate store, where such a
certificate is already trusted. Both `baseline.py` and `agent.py` call
`truststore.inject_into_ssl()` before importing the SDK.

If pip itself cannot reach PyPI, run this once:

    pip config set global.use-feature truststore

None of this is required on a machine without TLS interception.