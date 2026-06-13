# -*- coding: utf-8 -*-
"""Check remaining word gaps inside v3 pieces and whether -32dB silence
detection covered them (uncovered = breath noise above threshold)."""
import collections, json, os, re

SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC, "ai_cut")
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]


def norm(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


raw = []
for i, c in enumerate(CLIPS):
    with open(os.path.join(WORK, c + ".words.json"), encoding="utf-8") as f:
        for w in json.load(f)["words"]:
            if norm(w["w"]):
                raw.append({"clip": i, "s": w["s"], "e": w["e"]})

pieces = []
with open(os.path.join(WORK, "v3_pieces.txt"), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((CLIPS.index(m.group(1)), float(m.group(2)), float(m.group(3))))

with open(os.path.join(WORK, "silences.json"), encoding="utf-8") as f:
    sil = json.load(f)

buckets = collections.Counter()
uncovered = 0
uncov_time = 0.0
for c, s, e in pieces:
    ws = [w for w in raw if w["clip"] == c and w["s"] >= s - 0.01 and w["e"] <= e + 0.01]
    for a, b in zip(ws, ws[1:]):
        gap = b["s"] - a["e"]
        if gap >= 0.4:
            buckets[round(min(gap, 2.0), 1)] += 1
            cov = any(x < a["e"] + 0.15 and y > b["s"] - 0.15 for x, y in sil[CLIPS[c]])
            if gap >= 0.55 and not cov:
                uncovered += 1
                uncov_time += gap

print("word-gap distribution (>=0.4s) inside v3 pieces:")
for k in sorted(buckets):
    print(f"  {k:.1f}s: {buckets[k]}")
print(f"gaps >=0.55s NOT covered by -32dB silence: {uncovered}, total {uncov_time:.1f}s")
