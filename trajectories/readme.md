# Agent trajectories

Every agent used to build this project, with the record it produced.

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
documentation, and `check_results.py`. This was a conversation rather than a
coding agent session, and it produced no tool-call trajectory. Its output is
evidenced instead by the commit history, which is timestamped and where each
message names the specific change made.

## Redaction

One Gemini API key appeared in `trajectory-03-claude-code-session-3.jsonl`,
found by a pattern sweep of the repository before the file was committed. It
has been replaced with `AIza-REDACTED-KEY` and the key itself was rotated.
Nothing else in these files has been altered: the file is 22 bytes smaller
than the original, which is the difference between a 39-character key and the
17-character placeholder.