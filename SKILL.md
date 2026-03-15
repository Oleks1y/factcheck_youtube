---
name: factcheck_youtube
description: >
  Use when the user asks to analyze, verify, fact-check, or cross-reference a
  YouTube video or other video URL, especially when they want a sourced report
  about what the video claims and whether those claims hold up.
---

# factcheck_youtube

Extract a transcript, turn it into verifiable claims, check those claims against
 sources, and deliver a markdown report that makes uncertainty explicit.

## Overview

This skill is for evidence-driven analysis of videos, not vibe-based summarizing.

Use it when the user wants one of these outcomes:
- Fact-check a video
- Verify whether the video's claims are accurate
- Understand what the video argues, with sources
- Audit a video in a specific domain such as health, tech, history, or finance

Do not use it for:
- Pure summarization with no request to verify claims
- Subjective review of style, presentation, or persuasion
- Videos that cannot be accessed and have no transcript or summary fallback

## Codex Execution Rules

1. Prefer `spawn_agent` when the harness supports delegated work and the task is
   large enough to justify it. Video transcripts and multi-claim research expand
   context quickly.
2. If delegated work is unavailable, continue in the current session with a
   bounded claim budget and save intermediate artifacts early.
3. Use `scripts/extract-video-transcript.sh` for transcript extraction before
   falling back to manual parsing.
4. Save the final report to the current working directory using a filename in the
   format `factcheck_youtube-YYYY-MM-DD-[slugified-title].md`.

## Workflow

### Phase 1: Intake

Capture:
- Video URL
- User focus area, if any
- Domain risk level: general, tech, business, history, health, finance

If the user says something like "mainly check the nutrition claims", treat that
as the verification priority but still note other major claims.

### Phase 2: Extract Transcript

Run:

```bash
scripts/extract-video-transcript.sh "<URL>"
```

The script attempts:
1. Raw transcript extraction through `summarize ... --extract`
2. YouTube fallback through `summarize ... --youtube yt-dlp --extract`
3. Summary fallback through `summarize ... --length xxl`

If extraction fails entirely:
- State that transcript extraction failed
- Ask for a manual transcript when appropriate
- If the user still wants progress, analyze only the supplied summary and mark
  claims as lower-confidence because they may be paraphrased

### Phase 3: Extract Claims

Read `references/claim-extraction.md`.

Turn the transcript into an explicit verification queue:
- Split compound statements into separate claims
- Preserve numbers, dates, dosages, and named studies
- Capture timestamps when present
- Prioritize thesis claims, safety claims, and exact statistics first

### Phase 4: Verify Claims

Read `references/verification-methodology.md`.

For each prioritized claim:
1. Run direct evidence search
2. Run review-style search for synthesized evidence
3. Run adversarial search for debunks, criticism, failed replication, or safety issues
4. If the speaker cites a specific paper, guideline, or institution, verify it directly

## Source Rules

- Every verdict must trace to sources actually fetched or opened in the session.
- Prefer primary sources when practical.
- For health and medical topics, prefer primary sources and official guidance.
- For tech topics, prefer official guidance and version-specific documentation.
- Do not rely on snippets alone for high-stakes claims.
- If evidence is thin or conflicting, say so explicitly.

## Verdicts

Use one verdict per claim:
- `SUPPORTED`
- `PARTIALLY TRUE`
- `MISLEADING`
- `UNSUPPORTED`
- `CONTRADICTED`
- `CONTESTED`
- `OPINION`
- `UNVERIFIABLE`

Track confidence separately:
- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`

## Output Template

```markdown
# Video Analysis: [Title]

**Source:** [URL]
**Analysis Date:** [YYYY-MM-DD]
**Focus:** [User focus or General]

## Executive Summary
[3-5 sentences]

## What The Video Got Right
[Supported claims]

## What The Video Got Wrong Or Oversimplified
[Misleading, contradicted, or partially true claims]

## What The Video Missed
[Important caveats or counter-evidence]

## Claim-by-Claim Analysis

### Claim: "[quote or precise paraphrase]"
- **Timestamp:** [if available]
- **Category:** [type]
- **Verdict:** [value]
- **Confidence:** [value]
- **Evidence:** [summary with citations]
- **Counter-evidence:** [summary with citations]
- **Assessment:** [brief synthesis]

## Sources
[Numbered list with URLs]

## Methodology Note
[How transcript was obtained, how many claims were checked, major limits]
```

## Domain-Specific Notes

### Health and Medical

- Treat this as high-stakes.
- Check dosage claims against official guidance when available.
- Prefer systematic reviews, meta-analyses, and clinical guidelines over single studies.
- Flag contraindications, side effects, and over-generalized recommendations.

### Tech and Programming

- Verify against official guidance, changelogs, or primary docs.
- Check whether the advice is version-specific.
- Separate opinionated workflow advice from factual claims about tool behavior.

### History and Documentary

- Cross-check names, dates, and timelines with multiple reliable sources.
- Distinguish narration from editorialized interpretation.

## Anti-Hallucination Rules

- Do not invent studies, publication years, effect sizes, or statistics.
- If a cited source cannot be found, say that directly.
- Distinguish source claims from your inference.
- Unknown is an acceptable outcome.
- Do not collapse uncertainty into a strong verdict for the sake of neatness.
