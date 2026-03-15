# factcheck_youtube

`factcheck_youtube` is a Codex skill for analyzing YouTube videos and other
video URLs, extracting their claims, and producing a sourced fact-check report
in Markdown.

The project is designed for one concrete job: take a video that sounds
confident, break it into verifiable statements, look for confirming and
contradicting evidence, and return a report that is explicit about uncertainty.
It is not a generic summarizer and it is not meant to generate vibes-only
commentary.

## What This Project Is

This repository contains a complete skill package that can be installed into
Codex. The package includes:

- The skill definition in `SKILL.md`
- UI metadata in `agents/openai.yaml`
- Reference documents for claim extraction and verification methodology
- A helper shell script for transcript extraction
- Local tests that verify the package structure and extraction fallback logic

The skill is aimed at workflows like:

- fact-checking Shorts, interviews, explainers, and commentary videos
- checking whether a creator cited research accurately
- reviewing health, tech, business, or history claims against reliable sources
- producing a reusable Markdown report that can be stored in notes or a repo

## What The Skill Does

At a high level, the skill follows this pipeline:

1. Accept a video URL and optional focus area
2. Extract a transcript through the `summarize` CLI
3. Turn the transcript into a queue of concrete claims
4. Prioritize the most important claims first
5. Search for supporting evidence and counter-evidence
6. Assign a verdict and confidence level to each claim
7. Save a Markdown report in the current working directory

The intended outcome is not "prove the video right" or "prove the video wrong".
The intended outcome is to determine what can actually be supported by the
evidence available in the session.

## Repository Layout

```text
.
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── claim-extraction.md
│   └── verification-methodology.md
├── scripts/
│   └── extract-video-transcript.sh
└── tests/
    ├── test_extract_video_transcript.py
    └── test_skill_package.py
```

## Core Design Principles

### Evidence before confidence

The skill is built to avoid unsupported confidence. It explicitly prefers:

- fetched or opened sources over memory
- primary sources when practical
- official guidance for health and technical claims
- adversarial search instead of one-sided validation
- explicit uncertainty over fabricated certainty

### Claim-level analysis

The skill does not try to rate a whole video with one vague judgment. It breaks
the video into claims and assigns verdicts claim by claim. That makes the
analysis easier to audit and easier to reuse later.

### Honest failure modes

If transcript extraction fails, the skill should say so. If the evidence is
thin, the skill should say so. If a cited study cannot be located, the skill
should say so. Unknown is an acceptable result.

## Verdict Model

Each claim gets one verdict:

- `SUPPORTED`
- `PARTIALLY TRUE`
- `MISLEADING`
- `UNSUPPORTED`
- `CONTRADICTED`
- `CONTESTED`
- `OPINION`
- `UNVERIFIABLE`

Each claim also gets a separate confidence level:

- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`

This distinction matters. A claim can be `UNSUPPORTED` with `LOW` confidence if
the available evidence is incomplete, or `CONTRADICTED` with `HIGH` confidence
if high-quality sources clearly oppose it.

## Installation

### 1. Install the skill into Codex

If you want to install from GitHub into your local Codex skills directory:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Oleks1y/factcheck_youtube \
  --path . \
  --name factcheck_youtube
```

After installation, restart Codex so it picks up the new skill.

### 2. Install the transcript dependency

The extraction helper depends on the `summarize` CLI. Without it, the skill
cannot extract video transcripts through the bundled script.

Check whether it exists:

```bash
command -v summarize
```

If it is missing, install it using the method appropriate for your environment.

## Usage

The skill is invoked by name:

```text
Use $factcheck_youtube to fact-check this video: https://youtube.com/shorts/...
```

Other useful prompts:

```text
Use $factcheck_youtube to verify the claims in this video: https://youtube.com/watch?v=...
```

```text
Use $factcheck_youtube to analyze this video, focus on nutrition claims: https://youtube.com/shorts/...
```

```text
Use $factcheck_youtube to review this video and save a sourced markdown report: https://example.com/video
```

## How The Skill Works Internally

### 1. Transcript extraction

The helper script `scripts/extract-video-transcript.sh` tries three strategies:

1. raw extraction through `summarize --extract`
2. YouTube fallback through `summarize --youtube yt-dlp --extract`
3. summary fallback through `summarize --length xxl`

If it falls back to the generated summary path, it writes a note into the output
file warning that claims may be paraphrased or omitted.

### 2. Claim extraction

The skill reads `references/claim-extraction.md` and converts the transcript
into a structured queue of claims. It prioritizes:

- central thesis claims
- health, safety, legal, or financial advice
- exact statistics and cited studies
- surprising or counter-intuitive claims

### 3. Verification

The skill reads `references/verification-methodology.md` and checks claims using
both direct and adversarial search. The goal is to find not only support, but
also serious criticism, failed replication, caveats, and missing context.

### 4. Report generation

The final output is a Markdown file named like:

```text
factcheck_youtube-YYYY-MM-DD-[slugified-title].md
```

The report is meant to be easy to read and easy to audit later.

## Output Structure

The report generated by the skill follows this general structure:

- title and source URL
- analysis date and focus area
- executive summary
- what the video got right
- what the video got wrong or oversimplified
- what the video missed
- claim-by-claim analysis
- sources
- methodology note

This makes the output useful both as a quick read and as a deeper research note.

## Domain-Specific Behavior

### Health and medical content

Health content is treated as high-stakes. The skill prefers:

- primary sources
- systematic reviews and meta-analyses
- official guidance
- explicit mention of contraindications and side effects

### Tech and programming content

Tech claims are checked against:

- official documentation
- changelogs
- version-specific guidance

This matters because many technical videos are accurate only for one library
version or one specific tool release.

### Business, finance, and legal content

These topics are often time-sensitive or jurisdiction-sensitive. The skill is
intended to note when definitions, laws, or market conditions may have changed.

## Limitations

This skill is useful, but it has hard limits:

- it depends on transcript extraction quality
- it cannot verify inaccessible or missing sources
- it may only partially verify very recent or niche claims
- it does not replace professional legal, medical, or financial advice
- it is not ideal for purely subjective content

Short-form videos can be especially tricky because they often compress several
claims into a few seconds and omit critical context.

## Development

The repository includes local tests to verify the package.

Run the full test suite with:

```bash
python3 -m unittest discover -s tests -v
```

Additional targeted check:

```bash
bash -n scripts/extract-video-transcript.sh
```

The test suite covers:

- required file presence
- expected skill metadata
- expected reference coverage
- extraction helper fallback behavior

## GitHub

Public repository:

- [Oleks1y/factcheck_youtube](https://github.com/Oleks1y/factcheck_youtube)

## Summary

`factcheck_youtube` is a focused Codex skill for turning video fact-checking
into a repeatable workflow. It is small in code size, but opinionated in method:
extract first, separate claims clearly, verify with real sources, search for
counter-evidence, and report uncertainty honestly.
