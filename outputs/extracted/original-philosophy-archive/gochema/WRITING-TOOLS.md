# WRITING TOOLS — co-write/edit the essays with AI (free, browser-first)

> Researched 2026-10-19. Rule: owner writes the words; tools suggest.
> Privacy note: free tiers train on text by default — opt out (ChatGPT
> data settings, Gemini activity off) since drafts are IP.

## Quick use (browser, no setup)
1. **ChatGPT Free — Canvas/Writing Blocks** (best all-rounder, free):
   unlimited chat + full-screen long-form writing blocks (since May/Jun 2026)
   + targeted edits (change length/tone of a selection, not whole rewrite).
   Workflow: paste a draft1 section → "keep my exact words, fix only X" →
   accept edits manually. Caveat: copy-paste loop; drafts live in one chat.
2. **Claude Free** — best prose-drafter/rewriter on free tier (Sonnet 5).
   Best for: "match this voice" tasks with a short sample. Limited messages.
3. **Gemini Free — Canvas** (Google): free drafting space, version stepping,
   "Suggest edits" button, export to Docs. Docs-Gemini integration itself is
   PAID now (flag) — Canvas-only on free.
4. **LanguageTool / Grammarly Free** — typo cleanup (owner's call: draft1 is
   verbatim, cleaning = re-record decision).

## Serious workflow (fits this repo)
5. **Obsidian vault over /root/gochema + Copilot plugin** (open source;
   free with own key/agent account): Quick Ask on any selection inside
   draft1.md — "continue in my tone" / "replace with quote from WEAVE" —
   edits proposed as reviewable hunks; **explicitly supports running
   opencode inside Obsidian** (the same agent stack). Markdown stays git.
   Alternates: **Caret** (local-first, any model, file-over-app), meld
   (local-first markdown agent), Companion-for-Claude (diff-review edits).
6. **ONLYOFFICE free** + AI plugin (bring own key: OpenAI/Anthropic/
   Gemini/local) — full word-processor with accept/reject edits for the
   final polish pass.

## For THIS project specifically
- draft1.md / ESSAY.md live in git — Obsidian+Copilot edits stay auditable
  (git diffs show exactly what the AI touched; verbatim blocks never lost).
- Suggested loop: write in browser canvas → paste into repo → commit →
  tool-suggest edits → hunk-review → commit. The compiler law still applies
  to the agent: suggestions on YOUR text, never new agent-voice text.
