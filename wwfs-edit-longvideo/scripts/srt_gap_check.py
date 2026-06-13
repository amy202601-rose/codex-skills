# -*- coding: utf-8 -*-
"""Wallace's caption-gap method: parse a JianYing-recognized SRT of the CUT
timeline; any audible region without a caption = residue the recognizer
couldn't form words from (orphan fragments, breaths with voice, mumbles).
Usage: python srt_gap_check.py <exported.srt> [min_gap=0.40]"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
WORK = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\ai_cut"
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
SRT = sys.argv[1]
MIN_GAP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.40


def ts2s(ts):
    h, m, rest = ts.split(":")
    s, ms = rest.replace(".", ",").split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


with open(SRT, encoding="utf-8-sig") as f:
    content = f.read()
cues = []
for block in re.split(r"\n\s*\n", content.strip()):
    lines = block.strip().splitlines()
    if len(lines) < 2:
        continue
    tl = lines[1] if "-->" in lines[1] else lines[0]
    m = re.search(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)", tl)
    if not m:
        continue
    text = " ".join(lines[2:] if "-->" in lines[1] else lines[1:])
    cues.append((ts2s(m.group(1)), ts2s(m.group(2)), text))

pieces = []
with open(os.path.join(WORK, "v3_pieces.txt"), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((m.group(1), float(m.group(2)), float(m.group(3))))


def tl_to_src(tl):
    cur = 0.0
    for clip, s, e in pieces:
        if tl < cur + (e - s):
            return clip, s + (tl - cur)
        cur += e - s
    return None, None


def fmt(t):
    return f"{int(t//60)}:{t%60:05.2f}"


print(f"cues: {len(cues)}, checking gaps >= {MIN_GAP}s\n")
n = 0
for (s1, e1, t1), (s2, e2, t2) in zip(cues, cues[1:]):
    gap = s2 - e1
    if gap >= MIN_GAP:
        n += 1
        clip, src = tl_to_src(e1)
        print(f"GAP {gap:.2f}s  final {fmt(e1)} - {fmt(s2)}  (src {clip} {src:.2f})")
        print(f'   before: "...{t1[-40:]}"')
        print(f'   after:  "{t2[:40]}..."\n')
print(f"caption gaps found: {n}")
