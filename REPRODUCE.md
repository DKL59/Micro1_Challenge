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

## Run the baseline

The baseline sends each claim to the model with no documents and no context.

PowerShell:

    $env:GEMINI_API_KEY = "your-key-here"
    python baseline.py

Bash:

    GEMINI_API_KEY="your-key-here" python baseline.py

## Run the solution

The agent sends the same claims together with the source documents, and
requires a source quote for every figure:

    python agent.py

## Run the evaluation

Compare the two result files against the verdicts and reasoning recorded in
`CASES.md`, which are my own assessments, made before either system was run.

## Expected output

`results/baseline.json` and `results/agent_v1.json`. Each contains, per case:
the case id, the exact prompt sent, the full model response, any error, and
the time taken. The agent file additionally contains the parsed structured
output and the source files used.

Both scripts print progress to the terminal and confirm the file written.

## Versions

- Windows 11
- Python 3.12.4
- google-genai 1.29.0
- truststore 0.10.4
- Model: gemini-3.6-flash

## Runtime and cost

Three cases per run.

- Baseline: about 16 seconds per case, roughly 1,800 tokens per case
- Agent: about 16 seconds per case, roughly 5,300 tokens per case

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