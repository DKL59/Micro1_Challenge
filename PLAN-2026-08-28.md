# Context Brief — micro1 Agentic Workflows Hackathon

## Who I am
Dipendra Limbu, data analyst in Nepal (UTC+5:45). Strong in Python
(pandas, scikit-learn), SQL, R, statistics, and analytical writing.
Two years independent equity research on NEPSE. No prior software
engineering experience.

## My setup
Windows 11, VS Code, folder C:\Users\dklim\Micro1_Challenge
PowerShell blocks npm.ps1 — must use `npm.cmd` and `gemini.cmd`
Gemini CLI, authenticated with a Gemini API key (~250 requests/day,
Flash model). Export traces with `/chat share filename.json`
GitHub Desktop, repo Micro1_Challenge, currently private
Python installed. Zoom for screen recording.

## The competition
micro1 Agentic Workflows Hackathon. Open problem — I choose it.
Deadline: Monday 31 Aug, 5:44am Nepal time.
Scoring out of 100: Agent Solution & Engineering 30, End-to-End
Quality 20, Problem & User Value 15, Measured Improvement 15,
Reproducibility 15, Hot Take 5.
Deliverables: solution code + README + improvement changelog;
reproduction guide; video under 5 minutes; agent trajectories for
every agent used.

## The problem I chose
Retail investors are surrounded by confident stock recommendations
from influencers, tipsheets and forums, with no way to judge whether
any of it is supported. They act on belief. They are also often
unaware that macro conditions may matter more than the company.

## What I'm building
An agent that takes one publicly posted stock recommendation and
checks it against the company's public filings and current macro
context. It returns what the claim supports, what it omits, and what
it ignores, with citations. It never says buy or sell.

## What I'm NOT building
Buy/sell advice, price targets, a user interface, live market feeds,
portfolio tools, or more than about ten evaluation cases.

## Evaluation plan
~10 real posted recommendations. I assess each myself against a
rubric before seeing agent output. Metrics: agreement with my
assessment, whether the agent's claims cite real passages, human
time per assessment, cost per assessment.

## Working rules
Build the evaluation harness before the solution.
Reason inside the agent so it lands in the trajectory.
One change at a time, logged with its measured result.
Freeze the code Sunday midday; the rest of Sunday is documentation.
Submit Sunday evening, not Monday morning.

## Current state
[Friday 28 Aug, evening — setup complete, problem chosen, market
not yet decided: NEPSE vs US-listed via EDGAR]