# Verification Methodology

Use this reference after claim extraction. The job is to discover whether a
claim holds up, not to defend or attack the video's thesis.

## Core Principle

Verify, do not validate. Treat each claim as genuinely uncertain until the
evidence says otherwise.

## Search Tiers

### High Priority Claims

Run three to four searches:
1. Direct evidence search
2. Review or meta-analysis search
3. Adversarial Search for criticism, debunks, side effects, or failed replication
4. Specific source lookup when the speaker cites a study or institution

### Medium Priority Claims

Run two searches:
1. General evidence search
2. Adversarial Search

### Low Priority Claims

Run one quick search:
1. Fact-check or evidence search

## Adversarial Search

Every important claim needs a serious attempt to find counter-evidence. Useful
patterns include:

- "[claim] debunked"
- "[claim] criticism"
- "[claim] myth"
- "[study] retracted"
- "[study] failed replication"
- "[product] side effects"
- "[person or company] conflict of interest"

## Source hierarchy

Prefer sources in this order:
1. Meta-analyses and systematic reviews
2. Replicated peer-reviewed studies
3. Single peer-reviewed studies
4. Official guidance from public institutions or professional bodies
5. Credible expert commentary that cites primary evidence
6. High-quality journalism citing primary evidence

## Domain Rules

### Health and Medical

- Prefer primary sources and official guidance.
- Use full source pages, not only snippets, for high-stakes claims.
- Check dose, duration, contraindications, and population limits.

### Tech and Programming

- Prefer official documentation and versioned release notes.
- Check dates and versions before deciding something is wrong.

### Business, Finance, and Legal Topics

- Be careful with jurisdiction, date, and definition drift.
- Distinguish marketing claims from verifiable evidence.

## Verdict Criteria

Use one verdict per claim:

| Verdict | Meaning |
| --- | --- |
| SUPPORTED | Multiple reliable sources support the claim |
| PARTIALLY TRUE | Core idea is right, but details are wrong or overstated |
| MISLEADING | The framing implies more than the evidence supports |
| UNSUPPORTED | Reliable evidence could not be found |
| CONTRADICTED | Reliable evidence points the other way |
| CONTESTED | Credible disagreement exists |
| OPINION | The statement is fundamentally normative or subjective |
| UNVERIFIABLE | The claim is too vague or inaccessible to check responsibly |

## Confidence

- HIGH: multiple reliable sources and clear signal
- MEDIUM: useful evidence but not complete coverage
- LOW: thin evidence or indirect inference
- UNKNOWN: insufficient evidence either way

## Anti-Hallucination Rules

- Every verdict must map to sources that were actually fetched.
- Do not invent citations, quotes, or study details.
- State when evidence is missing.
- Separate what the source says from what you infer.
- If the claim depends on a missing paper or inaccessible data, say that directly.
