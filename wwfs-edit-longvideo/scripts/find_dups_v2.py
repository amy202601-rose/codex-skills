# -*- coding: utf-8 -*-
"""Scan the FINAL v2 kept content for any repeated word n-grams (>=5 words),
which indicates surviving duplicate takes. Reports source positions and the
final-timeline minute:second where each duplicate appears."""
import json, os, re, sys
from collections import defaultdict

SRC_DIR = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC_DIR, "ai_cut")
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
N = 5
STOP_NGRAMS = set()  # filled below for common idioms allowed to repeat


def norm(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


raw_words = []
for idx, clip in enumerate(CLIPS):
    with open(os.path.join(WORK, clip + ".words.json"), encoding="utf-8") as f:
        for w in json.load(f)["words"]:
            n = norm(w["w"])
            if n:
                raw_words.append({"clip": idx, "s": w["s"], "e": w["e"], "w": w["w"], "n": n})

# final pieces (default v2; pass e.g. v3_pieces.txt as argv[1])
PIECES_FILE = sys.argv[1] if len(sys.argv) > 1 else "v2_pieces.txt"
pieces = []
with open(os.path.join(WORK, PIECES_FILE), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((CLIPS.index(m.group(1)), float(m.group(2)), float(m.group(3))))

# words inside final timeline, with final-timeline timestamps
final_words = []
cursor = 0.0
for clip, s, e in pieces:
    for w in raw_words:
        if w["clip"] == clip and w["s"] >= s - 0.01 and w["e"] <= e + 0.01:
            final_words.append({**w, "tl": cursor + (w["s"] - s)})
    cursor += e - s

print(f"final timeline: {cursor/60:.2f} min, {len(final_words)} words")

grams = defaultdict(list)
for i in range(len(final_words) - N + 1):
    key = " ".join(final_words[i + k]["n"] for k in range(N))
    grams[key].append(i)


def fmt(t):
    return f"{int(t//60)}:{t%60:05.2f}"


# group overlapping repeated grams into duplicate regions
hits = {k: v for k, v in grams.items() if len(v) > 1}
flagged = sorted({i for v in hits.values() for i in v})
regions = []
for i in flagged:
    if regions and i <= regions[-1][1] + 2:
        regions[-1][1] = max(regions[-1][1], i + N - 1)
    else:
        regions.append([i, i + N - 1])

# pair up regions with identical text
seen = {}
print("\n=== repeated regions in FINAL output ===")
count = 0
for a, b in regions:
    text = " ".join(final_words[k]["n"] for k in range(a, b + 1))
    w0, w1 = final_words[a], final_words[b]
    line = (f"[final {fmt(w0['tl'])} - {fmt(w1['tl'])}] {CLIPS[w0['clip']]} "
            f"{w0['s']:.2f}-{w1['e']:.2f}  \"{' '.join(final_words[k]['w'] for k in range(a, b+1))}\"")
    key = text[:60]
    seen.setdefault(key, []).append(line)
for key, lines in seen.items():
    if len(lines) > 1:
        count += 1
        print(f"\nDUP #{count}:")
        for l in lines:
            print("  " + l)
# also print singleton regions (repeat partner may differ in wording at edges)
print("\n=== other flagged regions (partner may be reworded) ===")
for key, lines in seen.items():
    if len(lines) == 1:
        print("  " + lines[0])
