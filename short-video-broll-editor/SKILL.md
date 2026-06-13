---
name: short-video-broll-editor
description: Create a polished vertical short video from a talking-head MP4 and matching SRT subtitle file. Use when the user provides .mp4 and .srt files and wants a finished edit with storyboarded full-screen B-roll, right-bottom circular A-roll picture-in-picture, dynamic Chinese text cards, text-pop sound effects, background music, and maximized voice audio.
---

# Short Video B-roll Editor

## Core Workflow

Use this skill when the user gives a source talking-head video and SRT, then asks for a complete edited short video.

1. Inspect the input MP4/SRT and confirm duration, orientation, audio stream, and subtitle encoding.
2. Read the SRT and identify 8-16 key beats where visual emphasis helps comprehension: hooks, numbers, comparisons, examples, conclusions, CTA.
3. Create a B-roll storyboard with time ranges. Keep A-roll visible 65%-75% of the video; use B-roll for emphasis, explanation, and transitions.
4. Generate or gather vertical 9:16 B-roll assets for the beats. Use the `imagegen` skill for AI-generated raster B-roll when assets do not already exist.
5. Build a render plan JSON for `scripts/render_from_plan.ps1`.
6. Run the render script to compose:
   - full-screen B-roll,
   - right-bottom circular A-roll PiP with metallic/gold ring,
   - dynamic large text cards,
   - pop/chime SFX at text-card entrances,
   - optional looping BGM,
   - maximized/limited voice audio.
7. Validate with ffmpeg decode check, audio stream check, and 4-6 preview frames at key text/B-roll points.
8. Return the final MP4 path plus any preview clips/frames.

## Defaults

- Output format: vertical 1080x1920 MP4, H.264 video, AAC audio.
- B-roll style: full-screen portrait financial/explainer visuals, documentary/editorial, no logos, no unreadable small text.
- A-roll PiP: circular window, bottom-right, include face plus neck/shoulder, metallic gold ring.
- Text cards: big Chinese text, 1-2 lines, 8-14 Chinese characters when possible, gold/white on transparent background.
- Text timing: align to the actual SRT cue that says the keyword, not only the storyboard section start.
- SFX: short, audible but not harsh, triggered exactly at text-card start times.
- BGM: loop if shorter than the video; keep audible but below voice.
- Voice: maximize using dynamic normalization/compression/limiting; do not clip.

## Plan File

Create a JSON plan for the render script:

```json
{
  "output": "final.mp4",
  "text_cards": [
    { "lines": ["7,144", "fund pool"], "start": 22.05, "duration": 3.4, "gold_line": 0 }
  ],
  "broll": [
    { "image": "assets/G02_pension_fund_vault.png", "start": 17.0, "duration": 8.5 }
  ],
  "pip": { "x": 660, "y": 1440, "crop": "980:980:50:360", "size": 340 },
  "audio": {
    "bgm": "01.ogg",
    "bgm_volume": 0.24,
    "sfx_volume": 2.4,
    "voice_mode": "max"
  }
}
```

Paths in the plan may be absolute or relative to the plan file directory.

## Script

Use `scripts/render_from_plan.ps1` after preparing B-roll image files and a plan JSON:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\render_from_plan.ps1 `
  -Video .\input.mp4 `
  -Srt .\input.srt `
  -Plan .\render-plan.json `
  -Output .\final.mp4
```

If the user provides BGM, pass it in the plan as `audio.bgm`. If no BGM is provided, the script can create a quiet generated bed, but prefer the user's music when available.

For detailed storyboard and audio rules, read `references/workflow.md`.
