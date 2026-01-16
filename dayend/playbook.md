# Dayend Playbook

Examples of invocation and expected behavior.

Example 1 — Quick run with pasted transcript

User: "Run the dayend skill for project infra and save files."

Assistant: gathers metadata (project=infra), requests any missing context, builds transcript from pasted content, renders files, returns code blocks, asks to save.

Example 2 — Run from within workspace

User: "Run the dayend skill — include open editors and recent git diffs."

Assistant: enumerates open files and diffs, builds transcript, renders artifacts, returns code blocks, and suggests `Inventory/dayend/YYYY-MM-DD/` as save path.

Example 3 — Iterative update

User: "Shorten the SUMMARY and remove debug logs from the transcript."

Assistant: re-renders SUMMARY per the instruction and returns updated code block.
