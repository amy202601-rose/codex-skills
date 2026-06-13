# -*- coding: utf-8 -*-
"""Run ffmpeg silencedetect on each raw clip's audio and save intervals to
silences.json. Audio-only decode (-vn) so the 4K video stream is skipped."""
import json, os, re, subprocess

SRC_DIR = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC_DIR, "ai_cut")
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
NOISE_DB = "-32dB"   # below this is "silence" (breaths usually sit around -35..-25dB; tune if needed)
MIN_SIL = 0.30       # only report silences >= this length

out = {}
for clip in CLIPS:
    path = os.path.join(SRC_DIR, clip)
    cmd = ["ffmpeg", "-hide_banner", "-vn", "-i", path,
           "-af", f"silencedetect=noise={NOISE_DB}:d={MIN_SIL}", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    sils = []
    start = None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            start = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and start is not None:
            sils.append([round(start, 3), round(float(m.group(1)), 3)])
            start = None
    out[clip] = sils
    print(f"{clip}: {len(sils)} silences >= {MIN_SIL}s")

with open(os.path.join(WORK, "silences.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("saved silences.json")
