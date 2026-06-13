# Workflow Notes

## Beat Selection From SRT

Prefer text cards and SFX at the precise SRT cue where the speaker says the keyword:

- Hook: first 0-4 seconds.
- Numbers: percentages, dollar amounts, years, ownership shares.
- Comparisons: country vs country, institution vs retail, single asset vs diversified portfolio.
- Examples: roads, infrastructure, REITs, private equity, phone trading.
- Conclusions: "do not only...", "key takeaway...", "copy the allocation logic...".
- CTA: final 3-6 seconds.

Avoid putting a text card at a segment start if the speaker says the key phrase several seconds later.

## B-roll Rhythm

- Keep B-roll intervals mostly 6-11 seconds.
- Leave A-roll-only gaps between B-roll sections so the speaker does not disappear.
- Use B-roll full-screen. Do not split the screen into top/bottom panels unless the user asks.
- During full-screen B-roll, show the A-roll as a circular bottom-right PiP.
- Crop PiP to include face, neck, and some shoulder. Avoid face-only crops.
- Add a metallic/gold ring to the PiP.

## Visual Asset Prompt Pattern

For generated B-roll, use prompts like:

```text
Use case: productivity-visual
Asset type: vertical B-roll image for a Chinese short-form finance explainer video
Primary request: <specific beat>
Style/medium: vertical 9:16 documentary financial explainer, premium editorial realism
Composition/framing: full-screen portrait, strong central concept, room for later text overlay
Color palette: black, white, charcoal, metallic gold, restrained red/green accents
Text: no readable text, no logos, no numbers unless requested
Constraints: no real company logos, no watermark, no tiny unreadable text
```

## Text Card Rules

- Use 1-2 lines.
- Prefer exact terms from the user's SRT and requested terminology.
- For Chinese finance shorts, use big bold white/gold text with shadow and underline.
- Keep text in the upper half so it does not cover the PiP.
- Generate text as transparent PNG overlays when drawtext/font handling is risky.

## Audio Rules

- Preserve original speech timing.
- Maximize voice with highpass/lowpass, dynamic normalization, compression, volume, and limiter.
- Keep final peak at or below 0 dB; prefer limiter around 0.93-0.96.
- If BGM is supplied, loop it to the full video. Start around 0.18-0.30 volume when the music is already loud.
- If the user says BGM is audible but speech is small, keep BGM volume and increase voice chain first.
- Make SFX clearly audible. If not audible, regenerate or boost SFX; do not only raise BGM.

## Validation Checklist

- ffmpeg can decode the output without errors.
- Output has one video stream and one AAC audio stream.
- Preview frames at key text points show correct text, B-roll, and PiP position.
- Text does not overlap the PiP.
- BGM and SFX are audible in a short exported test clip.
- Voice is not distorted after maximization.
