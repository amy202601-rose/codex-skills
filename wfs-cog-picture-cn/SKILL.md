---
name: wfs-cog-picture-cn
description: Generate Wallace Chinese cognition/video-diary vertical cover images. Use when the user says "做认知图视频中文封面", "认知圈中文封面", "Wallace认知圈封面", "中文认知图封面", or asks to make a Chinese cognition talking-head cover from a Wallace photo plus cover title/subtitle. Produces a 9:16 sketchbook-style PNG with beige grid paper, handwritten Chinese title, yellow marker highlights, red sketch accents, and the provided portrait/photo.
---

# WFS Cognition Chinese Cover

Create a 9:16 vertical PNG cover for Wallace Chinese cognition/video-diary posts. This skill is for non-finance cognition, entrepreneurship reflection, work reflection, life observation, and Wallace认知圈 content.

## Inputs

- Use the user-provided current photo as the main visual. Do not reuse an older cutout or previous cover photo unless the user explicitly asks.
- Use explicit cover title/subtitle if provided. If the cover title/subtitle were just generated in the current publishing workflow, reuse those fields.
- If no usable photo path exists, ask for the source photo before rendering.
- If no title/subtitle exists, infer a short cover title and subtitle from the script or latest publishing fields; ask only when the content is unavailable.

## Visual Rules

- Output ratio: always 9:16, preferably 1080 x 1920 PNG, unless the user explicitly asks for another ratio.
- Style: Sketchbook hand-note look based on `E:\00Wallace\00 YouTube视频\B-roll.txt` when available.
- Background: warm beige paper `#f5f0e8`, subtle grid lines `#c8bfa0`, faint horizontal paper texture.
- Typography: use `ZCOOLKuaiLe.ttf` from `C:\Users\admin\.codex\skills\wwfs-covergen-lifestyle\fonts\` when available; otherwise use Microsoft YaHei UI.
- Text colors: deep brown `#3a2e1e`, secondary brown `#7a6a50`, accent red `#c0392b`, optional green `#2d5a1b`.
- Layout: large title on the left, portrait/photo sticker on the right, small top tag, subtitle/note below title, dashed red arrow or small doodle accents.
- Photo treatment: crop the provided photo into a rounded sticker with white border and soft shadow; keep Wallace's face visible and avoid text crossing the face.
- Footer: default to `Wallace · 一个创业者的真心话` unless the user gives another signature.

## Copy Rules

- Main title should be short and split into 1-3 punchy lines. Example: `钱上` / `5件事`.
- Subtitle should explain the emotional or cognitive hook in 1-2 short lines. Example: `30岁回看` / `20岁的弯路`.
- Eyebrow can be inferred from topic, such as `30岁生日复盘`, `创业复盘`, `认知复盘`, `普通人认知`.
- Optional note should be a compact supporting hook, such as `少走弯路` / `让时间替你打工`.
- Keep cover wording readable on mobile. Prefer fewer characters over clever but crowded copy.

## Rendering Workflow

1. Decide the final fields: `PhotoPath`, `Eyebrow`, `TitleLine1`, optional `TitleLine2`, `SubtitleLine1`, optional `SubtitleLine2`, optional `NoteLine1`, optional `NoteLine2`, `Footer`.
2. Save the output next to the source photo when possible, named like `<source-base>-cover-sketchbook-9x16.png` or `<script-number>-cover-sketchbook-9x16.png`.
3. Prefer the bundled script:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\admin\.codex\skills\wfs-cog-picture-cn\scripts\render_cog_cover.ps1 `
  -PhotoPath "E:\path\photo.jpg" `
  -OutPath "E:\path\cover-sketchbook-9x16.png" `
  -Eyebrow "30岁生日复盘" `
  -TitleLine1 "钱上" `
  -TitleLine2 "5件事" `
  -SubtitleLine1 "30岁回看" `
  -SubtitleLine2 "20岁的弯路" `
  -NoteLine1 "少走弯路" `
  -NoteLine2 "让时间替你打工"
```

4. If the script cannot run, use the same layout rules with another renderer. The important invariant is the final 9:16 sketchbook-style PNG.
5. Open the image with `view_image` before final response. Check: 1080 x 1920, text readable, no clipped characters, face visible, no incoherent overlap, and the sketchbook/B-roll style is clear.
6. If the first render is crowded or weak, regenerate a cleaner v2 before showing the result.

## Output

Return the PNG path and show a preview. Keep the final response short and mention any manual assumptions about title/subtitle choices.
