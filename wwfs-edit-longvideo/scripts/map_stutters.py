# -*- coding: utf-8 -*-
"""Map QC-transcript findings (final-timeline times) back to source clip times
and print the QC words around each spot, so cut ranges can be chosen on real
(re-transcribed) word boundaries rather than the original VAD-filtered ones."""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
WORK = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\ai_cut"
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]

# final-timeline spots to inspect (start_sec, end_sec, label)
SPOTS = [
    (15, 25, "financial planner retake"),
    (60, 65, "and and"),
    (310, 316, "so if so if"),
    (461, 466, "so so"),
    (483, 488, "many many"),
    (589, 594, "not not"),
    (978, 984, "like a like a"),
    (985, 990, "and and #2"),
]

pieces = []
with open(os.path.join(WORK, "v3_pieces.txt"), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((m.group(1), float(m.group(2)), float(m.group(3))))

with open(os.path.join(WORK, "v3_qc.wav.words.json"), encoding="utf-8") as f:
    qc_words = json.load(f)["words"]


def tl_to_src(tl):
    cursor = 0.0
    for clip, s, e in pieces:
        if tl < cursor + (e - s):
            return clip, s + (tl - cursor)
        cursor += e - s
    return None, None


def fmt(t):
    return f"{int(t//60)}:{t%60:05.2f}"


for a, b, label in SPOTS:
    print(f"=== {label} (final {fmt(a)} - {fmt(b)}) ===")
    for w in qc_words:
        if a <= w["s"] <= b:
            clip, src = tl_to_src(w["s"])
            print(f'  final {fmt(w["s"])}  src {clip} {src:7.2f}  "{w["w"]}"')
    print()
