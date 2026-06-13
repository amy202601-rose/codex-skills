# -*- coding: utf-8 -*-
"""Locate remaining dead runs (>0.6s below -44dB) inside final pieces."""
import os, pickle, re, sys

sys.stdout.reconfigure(encoding="utf-8")
WORK = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\ai_cut"
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
HOP = 0.01
FLOOR = -44.0

with open(os.path.join(WORK, "envelopes.pkl"), "rb") as f:
    envs = pickle.load(f)

pieces = []
with open(os.path.join(WORK, "v3_pieces.txt"), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((CLIPS.index(m.group(1)), float(m.group(2)), float(m.group(3))))

cursor = 0.0
for c, s, e in pieces:
    env = envs[c]
    run_start = None
    t = s
    while t < e:
        i = int(t / HOP)
        quiet = env[i] <= FLOOR if 0 <= i < len(env) else True
        if quiet and run_start is None:
            run_start = t
        elif not quiet and run_start is not None:
            if t - run_start > 0.6:
                fs = cursor + (run_start - s)
                print(f"dead {t-run_start:.2f}s  final {int(fs//60)}:{fs%60:05.2f}  src {CLIPS[c]} {run_start:.2f}-{t:.2f}")
            run_start = None
        t += HOP
    cursor += e - s
