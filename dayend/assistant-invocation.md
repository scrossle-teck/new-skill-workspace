# Assistant Invocation Guide

This guide describes how the assistant should be invoked from within the workspace to generate the day-end artifacts without running any local scripts.

Steps for a user:

1. In the workspace, open any files or terminals you want included in the summary.
2. Ask the assistant: "Run the `dayend` skill and summarize today's work for project X." Optionally paste or attach a transcript.
3. The assistant will confirm what context it will use, and may ask clarifying questions if necessary.
4. The assistant returns the four completed files as code blocks with filenames and suggested save paths.

Assistant behavior expectations:

- Collect context: open editors, recent git diffs, recent terminal commands, and pasted transcript.
- Build an internal transcript capturing key actions, decisions, and open asks.
- Render templates substituting `{transcript}`, `{date}`, `{user}`, and `{project}`.
- Return files as code blocks labeled with filenames. If asked, propose paths for saving into the repository.
