# -*- coding: utf-8 -*-
"""Find suspiciously long words (>1.4s) in the ORIGINAL transcripts that fall
inside kept pieces — these often hide merged retakes — then verbatim
re-transcribe ±4s around each (VAD off + filler prompt) to reveal what was
actually said."""
import json, os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel

SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC, "ai_cut")
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
MIN_DUR = 1.4

pieces = []
with open(os.path.join(WORK, "v3_pieces.txt"), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((m.group(1), float(m.group(2)), float(m.group(3))))


def in_kept(clip, t):
    return any(c == clip and s - 0.5 <= t <= e + 0.5 for c, s, e in pieces)


suspects = []
for clip in CLIPS:
    with open(os.path.join(WORK, clip + ".words.json"), encoding="utf-8") as f:
        for w in json.load(f)["words"]:
            dur = w["e"] - w["s"]
            # ignore genuinely long spoken items (TFSA spelled out is ~1.2s);
            # >1.4s for a normal word means dead air or a swallowed retake
            if dur > MIN_DUR and in_kept(clip, w["s"]):
                suspects.append((clip, w["s"], w["e"], w["w"], dur))

print(f"suspect words (> {MIN_DUR}s) inside kept pieces: {len(suspects)}\n")

model = WhisperModel("small.en", device="cpu", compute_type="int8")
for clip, s, e, word, dur in suspects:
    a, b = max(0, s - 4), e + 4
    snip = os.path.join(WORK, "suspect_snip.wav")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", f"{a:.2f}", "-to", f"{b:.2f}", "-i", os.path.join(SRC, clip),
                    "-vn", "-ar", "16000", "-ac", "1", snip], check=True)
    segments, _ = model.transcribe(snip, language="en", word_timestamps=True,
                                   vad_filter=False, beam_size=5,
                                   condition_on_previous_text=False, temperature=0.0,
                                   initial_prompt="Umm, so, so, so... like, hmm, okay, uh, I mean...")
    print(f'=== {clip} {s:.2f}-{e:.2f} "{word}" ({dur:.1f}s) — verbatim of {a:.1f}-{b:.1f}: ===')
    out = []
    for seg in segments:
        for w in seg.words or []:
            out.append(f'{a + w.start:.2f} "{w.word.strip()}"')
    print("  " + " | ".join(out) + "\n")
