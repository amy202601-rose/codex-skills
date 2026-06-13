# -*- coding: utf-8 -*-
"""Verbatim-transcribe the 5 source zones implicated by the JianYing SRT
findings, to pin exact cut coordinates."""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel

SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC, "ai_cut")
ZONES = [
    ("C0022.MP4", 477.0, 484.0, "so the diff false start"),
    ("C0025.MP4", 37.0, 44.5, "highest volatility double take"),
    ("C0025.MP4", 28.0, 38.5, "just flip it double take"),
    ("C0026.MP4", 252.0, 263.0, "2.17s uncaptioned gap region"),
    ("C0022.MP4", 282.5, 287.0, "very, fragment heard as there"),
]
model = WhisperModel("small.en", device="cpu", compute_type="int8")
snip = os.path.join(WORK, "zone_snip.wav")
for clip, t0, t1, label in ZONES:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", str(t0), "-to", str(t1), "-i", os.path.join(SRC, clip),
                    "-vn", "-ar", "16000", "-ac", "1", snip], check=True)
    segments, _ = model.transcribe(snip, language="en", word_timestamps=True,
                                   vad_filter=False, beam_size=5,
                                   condition_on_previous_text=False, temperature=0.0)
    print(f"=== {label}  ({clip} {t0}-{t1}) ===")
    out = []
    for seg in segments:
        for w in seg.words or []:
            out.append(f'{t0 + w.start:.2f}"{w.word.strip()}"')
    print("  " + " ".join(out) + "\n")
