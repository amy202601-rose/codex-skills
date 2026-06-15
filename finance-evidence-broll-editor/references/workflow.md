# Workflow Notes

## Beat Extraction

Start with the transcript/SRT when available. If only an MP4 is available, use the user's timestamps and screenshots first, then inspect nearby frames.

Track four beat types:

- Numbers: rates, tax brackets, years, durations, counts, prices, percentages, ROI, inflation.
- Entities: people, institutions, countries, cities, policies, account types, products.
- Concepts: opportunity cost, nominal vs real return, tax drag, liquidity, spread, leverage.
- Decisions: "ask this first", "if less than X years", "if more than Y years", "use this account first".

Each B-roll insert should answer one question: does this clarify, prove, structure, or make the spoken claim more memorable?

## Visual Grammar

- Use pale gray/white backgrounds for diagrams.
- Use white cards with black outlines and one active yellow card for focus.
- Use black arrows with endpoints clipped to card/circle boundaries.
- Use numeric badges with a high-contrast outline and short label.
- Use key-text plates with a black or white backing plate; center text vertically when there is only one line.
- Keep lower-screen text above player/subtitle safe areas unless the output platform requires otherwise.
- Vary layout: full-screen B-roll, A-roll side panel, picture-in-picture, entity card, diagram, chart, key phrase.

## Spoken Number Handling

Prefer exact spoken numbers. If the speaker says:

- "4 to 5 percent": show `4%-5%`.
- "4.5 percent": show `4.5%`.
- "35 percent tax": show `35% tax`.
- "3 percent inflation": show `3% inflation`.
- "one to two years": show `1-2 years`.
- "five years or more": show `5+ years`.

When a calculation is implied, show a simple chain:

```text
Nominal 4.5% -> after-tax about 2.9% -> after inflation about 0%
```

Use `about`, `~`, or `approx.` for inferred math. Never fabricate a precise value just to make the graphic look complete.

## Audio and Motion

- Add a whoosh at B-roll entrance and a smaller tick/pop when cards, badges, arrows, or charts reveal.
- Keep BGM audible but speech-led. If the user says music or SFX is missing, boost SFX/voice intentionally instead of only raising BGM.
- Animate diagrams quickly enough to finish within the spoken beat. Do not wait before the first movement.
- Use smooth reveal, slide, fly-in, dissolve, scale, line growth, or chart draw. Avoid long static holds unless the viewer must read dense evidence.

## Local Patch Rendering

For small revisions, do not re-render the entire video. Use this pattern:

1. Identify changed intervals and add 0.3-0.8 seconds of buffer if transitions/audio need it.
2. Render only those changed intervals from the source video with the updated B-roll function.
3. Cut unchanged intervals from the previous final video.
4. Concatenate all segments in order.
5. Validate duration drift. A few hundredths of a second can happen; larger drift needs re-cutting.

Use `scripts/render_changed_segments.py` as a template when the project uses MoviePy and ffmpeg.

## Preview Validation

Create a contact sheet from the finished output at:

- the B-roll start,
- the moment the target word/number is spoken,
- the B-roll end,
- the next A-roll return point.

For multi-scene revisions, make a 3x3 or 2x3 sheet. Check readability at thumbnail size, not only full size.
