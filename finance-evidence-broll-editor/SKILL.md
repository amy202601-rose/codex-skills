---
name: finance-evidence-broll-editor
description: Edit long-form finance, investing, business, and analytical talking-head videos with evidence-led B-roll. Use when Codex needs to add or revise B-roll, show spoken numbers, create entity/person/place/event cutaways, add key-text plates, music, SFX, transitions, animated diagrams, or render only changed video segments for an existing MP4.
---

# Finance Evidence B-roll Editor

## Core Workflow

Use this skill when the user gives a finance or business talking-head video and wants B-roll added, corrected, or made closer to a reference style.

1. Inspect the source MP4, current edited MP4 if any, script/SRT/transcript if available, and user screenshots or timestamps.
2. Build a shot list from the narration, not from generic decoration:
   - concepts become diagrams or decision trees,
   - claims and numbers become visible numeric badges or formulas,
   - named people, companies, places, institutions, policies, events, and products become concrete cutaways,
   - important phrases become readable key-text plates.
3. Keep A-roll as the spine. Use full-screen B-roll only when the visual is stronger; otherwise move A-roll to one side or use a picture-in-picture/side panel.
4. Match B-roll timing to the spoken beat. If the user points to "29 seconds" or says a word appears there, place the B-roll over that exact beat with a small lead-in and tail.
5. Add motion: slide/fly-in, dissolve, subtle zoom, parallax, arrow growth, chart reveal, and animated badges. Avoid static-looking inserts.
6. Add background music, whoosh/tick/pop SFX at B-roll entrances and visual reveals, and keep speech clearly dominant.
7. For small revisions, render only changed intervals and concatenate with the unchanged video. Do not re-render the full video unless global audio, global timing, or many intervals require it.
8. Validate with metadata and preview frames at the edited timestamps before returning the final MP4.

For detailed visual rules and local rendering patterns, read `references/workflow.md`.

## Defaults

- Canvas: 1920x1080 horizontal unless the user asks for vertical.
- Style: clean Chinese finance essay, pale gray or white background, black arrows, white/yellow cards, restrained red/green financial accents.
- B-roll length: 3-8 seconds for entity or key-text cutaways; 6-18 seconds for concept diagrams.
- A-roll visibility: keep host visible for most long-form edits; return to A-roll after dense diagrams.
- Text: large, readable Chinese text on black or white translucent/solid backing plates.
- Numbers: always surface spoken rates, years, percentages, dollar amounts, tax rates, counts, and decision thresholds in the B-roll when they matter.
- Audio: speech first, BGM audible but below voice, SFX clearly audible at visual events.
- Output: write a new MP4 when making substantial changes; for quick revisions, use a suffix such as `_numbers`, `_patch`, or `_v2` rather than overwriting unless asked.

## Number Sync Rules

When A-roll says a number, put that number in the B-roll if it clarifies the point.

- Show percentage rates as badges near the related object: `4%-5%` near GIC, `35%` near tax, `3%` near inflation.
- Show formulas as a sequence when the narration compares nominal, after-tax, and real return.
- Show time thresholds in decision trees: `1-2 years`, `5+ years`, lock-in terms, account limits, or deadlines.
- Keep numeric badges large enough to read in a preview thumbnail.
- Do not invent precise values. Use approximate markers like `about`, `approx.`, or `~` when the narration is approximate.

## Entity Cutaway Rules

When the narration names a concrete subject, show it visually instead of staying abstract:

- People: generated/editorial portrait card, name label, or A-roll plus portrait side panel.
- Places: map crop, skyline, landmark, arrival board, street/building exterior, or generated/licensed scene.
- Institutions: bank, tax agency, government document, account card, office/building, or report page.
- Events/policies: date card, timeline, headline-style card, document close-up, or simple map.

Use original, generated, licensed, or public-domain replacement visuals. Do not copy frames from a reference video.

## Validation Checklist

- Edited timestamps show the requested B-roll and return to A-roll at the requested end.
- Spoken numbers are present and readable in relevant B-roll.
- Key text is vertically centered in its backing plate.
- Arrows stop at the intended object boundary instead of crossing important labels.
- No text overlaps icons, faces, subtitles, or player-safe bottom areas.
- BGM and SFX are audible without drowning speech.
- Output metadata is sane: duration, resolution, fps, and audio stream.
- Provide a contact sheet or key preview frames for the changed moments.
