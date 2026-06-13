# -*- coding: utf-8 -*-
"""Fuzzy retake scan over the FINAL v2 output: compare every pair of kept
utterance lines within a 90s final-timeline window using normalized-text
similarity. Catches reworded restatements that exact n-gram matching misses."""
import difflib, json, os, re

SRC_DIR = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC_DIR, "ai_cut")
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
WINDOW_S = 90.0
MIN_RATIO = 0.55
MIN_WORDS = 6


def norm(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


raw_words = []
for idx, clip in enumerate(CLIPS):
    with open(os.path.join(WORK, clip + ".words.json"), encoding="utf-8") as f:
        for w in json.load(f)["words"]:
            n = norm(w["w"])
            if n:
                raw_words.append({"clip": idx, "s": w["s"], "e": w["e"], "w": w["w"], "n": n})

pieces = []
with open(os.path.join(WORK, "v2_pieces.txt"), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((CLIPS.index(m.group(1)), float(m.group(2)), float(m.group(3))))

final_words = []
cursor = 0.0
for clip, s, e in pieces:
    for w in raw_words:
        if w["clip"] == clip and w["s"] >= s - 0.01 and w["e"] <= e + 0.01:
            final_words.append({**w, "tl": cursor + (w["s"] - s)})
    cursor += e - s

# split final words into utterance lines (gap > 0.6s or sentence end)
lines = []
cur = []
for i, w in enumerate(final_words):
    if cur:
        prev = final_words[i - 1]
        gap = w["s"] - prev["e"]
        if w["clip"] != prev["clip"] or gap > 0.6 or (re.search(r"[.?!]$", prev["w"]) and gap > 0.25) or len(cur) >= 28:
            lines.append(cur)
            cur = []
    cur.append(i)
if cur:
    lines.append(cur)

recs = []
for idxs in lines:
    ws = [final_words[i] for i in idxs]
    if len(ws) < MIN_WORDS:
        continue
    recs.append({
        "tl": ws[0]["tl"], "tl_end": ws[-1]["tl"] + (ws[-1]["e"] - ws[-1]["s"]),
        "clip": ws[0]["clip"], "s": ws[0]["s"], "e": ws[-1]["e"],
        "text": " ".join(w["w"] for w in ws),
        "norm": " ".join(w["n"] for w in ws),
    })


def fmt(t):
    return f"{int(t//60)}:{t%60:05.2f}"


print(f"final lines >= {MIN_WORDS} words: {len(recs)}\n")
hits = 0
for i, a in enumerate(recs):
    for j in range(i + 1, len(recs)):
        b = recs[j]
        if b["tl"] - a["tl"] > WINDOW_S:
            break
        r = difflib.SequenceMatcher(None, a["norm"], b["norm"]).ratio()
        if r >= MIN_RATIO:
            hits += 1
            print(f"CAND #{hits}  sim={r:.2f}  gap={b['tl']-a['tl']:.0f}s")
            print(f"  A [{fmt(a['tl'])}] {CLIPS[a['clip']]} {a['s']:.2f}-{a['e']:.2f}: {a['text']}")
            print(f"  B [{fmt(b['tl'])}] {CLIPS[b['clip']]} {b['s']:.2f}-{b['e']:.2f}: {b['text']}\n")
print(f"total candidates: {hits}")
