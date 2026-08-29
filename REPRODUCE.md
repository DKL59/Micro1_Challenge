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

## What is reproducible, and what the free tier allows

The Gemini free tier allows **twenty requests per day per model**.

The baseline makes three calls, one per case. The shipped agent makes three at
minimum, and more when the validator sends a response back for correction —
the recorded run took five. So reproducing the shipped configuration costs
about eight calls, comfortably inside a day's allowance.

What you cannot reproduce from this repository is the earlier iterations.
Iterations 1, 2 and 3 ran against source files and instructions that have
since been replaced. Only their results survive, in `results/`. Each of those
files records the exact prompt it was sent, including the full text of the
source documents as they stood at the time, so what those runs were shown can
be read directly from the evidence — but re-running them would mean
reconstructing configurations this repository no longer contains. The
changelog treats them as history for that reason.

Two of the four metrics can be verified with no API calls at all:
`check_results.py` and `validate.py` read the committed result files and
recompute their figures. If you only want to check whether the numbers in
CHANGELOG.md are real, start there — it costs nothing.

If you do run several times in a day, watch the quota. It ran out mid-run
here and cost a control experiment.

## Before you run anything: the results files are evidence

`results/` already contains the five runs this project's claims are based on.
Each script refuses to overwrite an existing results file, so a fresh run will
stop immediately if its output already exists. That is deliberate: a results
file backs a row in CHANGELOG.md, and silently replacing one would leave a
claim with nothing behind it.

This means both scripts, run as they ship, will refuse. `baseline.py` ships
with `RUN_NAME = "baseline"` and `agent.py` with `RUN_NAME = "agent_v4"`, and
both of those files exist. To make your own run, change `RUN_NAME` at the top
of the script to a name of your own. The output filename and the run label
inside the JSON both derive from that one constant.

## Run the baseline

The baseline sends each claim to the model with no documents and no context.

`results/baseline.json` already exists, so change `RUN_NAME` at the top of
`baseline.py` to something of your own — `baseline-mine`, say — before
running, or the script will refuse.

PowerShell:

    $env:GEMINI_API_KEY = "your-key-here"
    python baseline.py

Bash:

    GEMINI_API_KEY="your-key-here" python baseline.py

## Run the solution

The agent sends the same claims together with the source documents. It must
quote a source line for every figure, state the full range when comparing
against a benchmark that varies by tenure or category, and compute any ratio
the claim turns on before assessing it.

Its response is then checked by `validate.py` before being accepted. If it
breaks the schema, it is sent back with the violations named, up to three
attempts. So a case can cost more than one API call, and the terminal reports
each attempt as it happens.

Change `RUN_NAME` in `agent.py` the same way before running.

Run this in the same terminal session as the baseline, so that
GEMINI_API_KEY is still set:

    python agent.py

Both scripts import the model name from the same place, so the two runs
cannot drift onto different models.

If a response cannot be corrected within three attempts, the last one is kept
and its remaining problems are recorded in `final_violations` for that case.
The run does not fail. In the recorded run every case came out clean, two of
them on the second attempt, but model output varies and yours may not.

## Run the evaluation

Two parts, because two different kinds of claim are being checked.

The reproducible part is checked by two scripts. Neither needs an API key or a
network connection, and neither writes anything.

    python check_results.py

reads the result files and `cases.json`, recomputes the per-case timings and
token counts quoted in CHANGELOG.md, and scores verdict agreement for any run
that returns structured output.

    python validate.py

applies three mechanical rules to every assertion in every agent run — the
status must be one of the three permitted values, the quote must appear in the
source file it names, and every number in a figure must appear inside its own
quote — and reports the violation count per run. It checks each run against
the source text recorded in that run's own prompt, so a run made before
Iteration 2 replaced the source files is still judged against what it was
actually shown.

If you produce runs under new names, add them to the `RUNS` list at the top of
each script and they will be scored alongside the rest.

The rest is human judgement. The baseline returns free text, so its verdicts
cannot be parsed and were scored by hand. Figures traceable to a source and
attribution errors caught are judgements throughout. For those, compare the
result files against the verdicts and reasoning recorded in `CASES.md`. How
each score is counted, and what it does and does not establish, is set out
under "How these are measured" at the top of CHANGELOG.md.

Those verdicts are my own assessments, written before either system was run,
with one correction made afterwards. Case 1's verdict was revised from
"partly supported" to "unsupported" during a file audit, when checking the
source showed Nabil declared a 12.50% cash dividend for the year in question
rather than the higher figure I had assumed. The revision came from the
source document, not from either system's output. The two result files that
existed at that point were re-scored against the corrected verdict, and the
correction moved both systems equally, so the comparison between them is
unaffected. The change is recorded in `DECISIONS.md`.

## Expected output

The repository ships with five result files, one per row in CHANGELOG.md:

- `results/baseline.json` — the control condition, no documents
- `results/agent_v1.json` — grounded, against the original source files
- `results/agent_v2.json` — grounded, after my analysis was stripped out of
  the sources into `notes/`
- `results/agent_v3.json` — as above, plus the range and ratio rules in the
  agent's instruction
- `results/agent_v4.json` — as above, plus the validation loop; the shipped
  configuration

Each contains, per case: the case id, the exact prompt sent, the full model
response, any error, and the time taken. The agent files additionally contain
the parsed structured output, the source files used, and — inside each
recorded prompt — the full text of the documents the agent was shown. That
last point matters: `agent_v1.json` still carries the source files as they
were before my analysis was stripped out of them, so the change made in
Iteration 2 can be read directly from the evidence rather than taken on trust.

`agent_v4.json` additionally records every attempt: the prompt sent, the
response, the violations found and the tokens spent, for each pass through the
loop. Where a case took two attempts, both are there.

A fresh run writes `results/<RUN_NAME>.json`. Both scripts print progress to
the terminal and confirm the file written.

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

| Run | Mean time per case | Per-case times | Mean tokens per case |
|---|---|---|---|
| baseline | 15.8s | 14.9 / 19.4 / 13.2 | 1,832 |
| agent_v1 | 16.4s | 25.8 / 11.4 / 12.1 | 5,338 |
| agent_v2 | 15.3s | 15.0 / 14.3 / 16.6 | 4,805 |
| agent_v3 | 20.3s | 24.2 / 18.5 / 18.1 | 5,620 |
| agent_v4 | 70.1s | 53.5 / 82.6 / 74.3 | 10,741 |

The per-case times are given because with three cases a mean is fragile:
agent_v1's mean is one slow case pulling two fast ones, and its median of
12.1s sits below the baseline's 14.9s.

agent_v4 costs what it does because two of its three cases needed a second
call. Its token figure is the total across all attempts, not the final one.

A baseline run plus the shipped agent run takes about four and a half minutes
and eight API calls.

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