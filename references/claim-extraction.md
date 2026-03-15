# Claim Extraction

Use this reference after a transcript has been extracted and before verification
starts. The goal is to convert free-form speech into a clean, prioritized queue
of verifiable claims.

## Claim Categories

Use one primary category per claim:

| Category | What it covers | Example |
| --- | --- | --- |
| Scientific | Empirical statements about how the world works | "Creatine improves sprint performance" |
| Causal | X causes, prevents, or changes Y | "Blue light delays melatonin release" |
| Statistical | Explicit percentages, counts, dates, or effect sizes | "Risk drops by 30 percent" |
| Recommendation | Advice the viewer could act on | "Everyone should take magnesium" |
| Historical | Claims about people, events, or chronology | "This law passed in 1994" |
| Mechanistic | Explanations of how something works | "The drug blocks receptor X" |
| Comparative | One option is better or worse than another | "Tool A is faster than Tool B" |
| Authority | Claims anchored in experts or institutions | "The WHO recommends this" |

## Extraction Rules

1. One claim per entry.
2. Preserve specificity.
3. Record timestamps when present.
4. Separate direct claims from speaker opinion or anecdote.
5. Merge duplicates only after preserving the most specific wording.

## Claim Signals

Strong signals:
- "Studies show"
- Specific numbers, dates, dosages, or percentages
- Named researchers, journals, institutions, or laws
- "It has been proven" or "research found"

Medium signals:
- "X causes Y"
- "The best way to"
- "Most people do not know"
- Comparative wording like "better than"

Weak signals:
- "I think"
- "It seems"
- "In my experience"

Skip:
- Intros, calls to action, jokes, and transitions without factual content

## Prioritization

Build the Verification queue in this order:
1. Central thesis claims
2. Health, safety, legal, or financial advice
3. Specific statistics and citations
4. Surprising or counter-intuitive claims
5. Supporting background claims
6. Clearly marked opinion

If the user gave a focus area, move those claims to the top of the queue.

## Output Format

For each entry, capture:

```text
Claim:
Timestamp:
Category:
Specificity:
Speaker confidence:
Priority:
Context:
```

## Verification queue Summary

Before starting research, produce a compact summary:

```text
Total claims identified:
By category:
By priority:
Verification queue:
```
