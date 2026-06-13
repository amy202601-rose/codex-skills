# -*- coding: utf-8 -*-
"""Round-trip QC: transcribe the rendered final-timeline audio (no VAD filter,
so fillers/stutters survive), then scan for consecutive repeated words/bigrams.
This catches what text-based scans on the ORIGINAL transcript can't see —
fillers Whisper dropped the first time, and words clipped at cut boundaries."""
import json, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel

WORK = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\ai_cut"
WAV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "v3_qc.wav")
OUT = WAV + ".words.json"


def norm(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


if os.path.exists(OUT):
    with open(OUT, encoding="utf-8") as f:
        words = json.load(f)["words"]
    print(f"loaded cached {OUT}: {len(words)} words")
else:
    t0 = time.time()
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segments, info = model.transcribe(WAV, language="en", word_timestamps=True,
                                      vad_filter=False, beam_size=5,
                                      condition_on_previous_text=False,
                                      initial_prompt="Umm, so, so, so... like, hmm, okay, uh, I mean...")
    words = []
    for seg in segments:
        for w in seg.words or []:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"words": words}, f, ensure_ascii=False)
    print(f"transcribed {len(words)} words in {time.time()-t0:.0f}s")


def fmt(t):
    return f"{int(t//60)}:{t%60:05.2f}"


print("\n=== first 40s of the cut ===")
for w in words:
    if w["s"] > 40:
        break
    print(f'{fmt(w["s"])}  {w["w"]}')

print("\n=== stutter scan: same word 2+ times in a row ===")
i = 0
while i < len(words) - 1:
    n = norm(words[i]["w"])
    j = i + 1
    while j < len(words) and norm(words[j]["w"]) == n and n:
        j += 1
    if j - i >= 2:
        print(f'[{fmt(words[i]["s"])}] "{n}" x{j-i}')
    i = max(j, i + 1)

print("\n=== bigram stutter: A B A B ===")
for i in range(len(words) - 3):
    a, b, c, d = (norm(words[k]["w"]) for k in range(i, i + 4))
    if a and b and a == c and b == d and a != b:
        ctx = " ".join(words[k]["w"] for k in range(i, min(i + 6, len(words))))
        print(f'[{fmt(words[i]["s"])}] {ctx}')
