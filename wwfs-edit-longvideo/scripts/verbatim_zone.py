# -*- coding: utf-8 -*-
"""Verbatim transcription of an arbitrary source zone: clip T0 T1"""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel

SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC, "ai_cut")
clip, T0, T1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
snip = os.path.join(WORK, "zone_snip.wav")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", str(T0), "-to", str(T1), "-i", os.path.join(SRC, clip),
                "-vn", "-ar", "16000", "-ac", "1", snip], check=True)
model = WhisperModel("small.en", device="cpu", compute_type="int8")
segments, _ = model.transcribe(snip, language="en", word_timestamps=True,
                               vad_filter=False, beam_size=5,
                               condition_on_previous_text=False, temperature=0.0)
for seg in segments:
    for w in seg.words or []:
        print(f'{T0 + w.start:7.2f}-{T0 + w.end:7.2f}  "{w.word.strip()}"')
