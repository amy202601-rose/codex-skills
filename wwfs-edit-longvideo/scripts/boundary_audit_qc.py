# -*- coding: utf-8 -*-
"""Boundary audit using the ROUND-TRIP QC transcript (real rendered audio):
for every piece junction, print the QC words spanning it and flag danglers.
This is what the ear actually hears at each cut."""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
WORK = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\ai_cut"
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
DANGLERS = {"and", "so", "but", "or", "the", "a", "an", "to", "of", "with",
            "like", "if", "because", "that", "for", "is", "are", "was"}

pieces = []
with open(os.path.join(WORK, "v3_pieces.txt"), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((CLIPS.index(m.group(1)), float(m.group(2)), float(m.group(3))))

with open(os.path.join(WORK, "v3_qc.wav.words.json"), encoding="utf-8") as f:
    qc = json.load(f)["words"]


def norm(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


def fmt(t):
    return f"{int(t//60)}:{t%60:05.2f}"


junctions = []
cursor = 0.0
for c, s, e in pieces[:-1]:
    cursor += e - s
    junctions.append(cursor)

flags = 0
for jt in junctions:
    before = [w for w in qc if w["s"] < jt - 0.02]
    after = [w for w in qc if w["s"] >= jt - 0.02]
    bw = [w["w"] for w in before[-5:]]
    aw = [w["w"] for w in after[:5]]
    last = norm(bw[-1]) if bw else ""
    flag = ""
    # dangler = junction word is a connective AND doesn't end the sentence
    if last in DANGLERS and bw and not bw[-1].rstrip('"\')').endswith((".", "?", "!", ",")):
        flag = "  <<< DANGLER"
        flags += 1
    if flag:
        print(f"[{fmt(jt)}] ...{' '.join(bw)}  |||  {' '.join(aw)}...{flag}")
print(f"\ndangler flags: {flags}  (junctions: {len(junctions)})")
