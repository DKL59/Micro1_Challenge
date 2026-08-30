# Agent trajectories

Two kinds of agent appear in this project: the development agents that built
it, and the runtime agent it ships. Both have a record here.

## Claude Code (Sonnet 5) — the development agent

Full session transcripts, exported from Claude Code's own local session
records rather than re-typed or summarised. Each line is one event: a prompt,
a tool call, a file write, or an approval I gave. They are dense but complete.

- `trajectory-01-claude-code-session-1.jsonl` — 29 August, morning.
- `trajectory-02-claude-code-session-2.jsonl` — 29 August, to 14:22.
- `trajectory-03-claude-code-session-3.jsonl` — 29 August, to 14:27.

`trajectory-agent-build-readable.txt` is a plain-text export covering the
agent build and the TLS certificate diagnosis. It duplicates material in the
session files above and is included because the JSON is hard to read. It
carries no session number because I did not verify which session it came from.

## Gemini CLI

- `trajectory-00-gemini-setup-test.json` — 28 August, before the competition
  opened. A Fibonacci exercise run once to confirm that trajectory export
  worked. It is not part of this project's development; it is here because the
  repository's first commit contained it and removing it would misrepresent
  what existed before kickoff.

## Claude (Opus 5), via chat

Used for problem selection, scoping, review of agent output, drafting of
documentation, `check_results.py`, `validate.py`, `test_validate.py`, the
overwrite guards in both scripts, the Iteration 2 rewrite of `sources/` and
`notes/`, the instruction rules added in Iterations 3 and 4, and the
validation loop. This was a conversation rather than a coding agent session,
and it produced no tool-call trajectory. Its output is evidenced instead by
the commit history, which is timestamped and where each message names the
specific change made.

## The runtime agent

The system this project ships is itself an agent. Since Iteration 4 it acts,
evaluates its own output against `validate.py`, and acts again on what the
evaluation found. Its trajectory is not a file in this folder. It is the
result files themselves.

`results/agent_v4.json` records, per case and per attempt: the exact prompt
sent, the full response, the parsed structured output, the violations the
validator returned, and the tokens that attempt cost. Where a case took two
attempts both are present in order, so the feedback that shaped the second
pass can be read directly rather than inferred.

Case 3 is the clearest example. The first attempt reaches the right verdict,
identifies that the claimed 32% belongs to the sector rather than to EBL, and
computes price to book at 729.50 / 246.74 = 2.956. The validator rejects it on
one citation. The second attempt returns the same verdict, the same three
assertions and the same arithmetic, with a single quote changed. That is
precisely what the correction prompt asked for, and it is visible side by side
in the file.

One qualification, recorded in full in `DECISIONS.md`. The violations in those
attempt records were produced by a stricter path than the one that scores
these runs: `agent.py` gives the validator the source files as written, while
`validate.py` gives it the same files with whitespace collapsed. All four
recorded violations recompute to zero under the scoring rule. The trajectory
is a faithful record of what happened. What it means is qualified there.

## Redaction

One Gemini API key appeared in `trajectory-03-claude-code-session-3.jsonl`,
found by a pattern sweep of the repository before the file was committed. It
has been replaced with `AIza-REDACTED-KEY` and the key itself was rotated.
Nothing else in these files has been altered: the file is 22 bytes smaller
than the original, which is the difference between a 39-character key and the
17-character placeholder.