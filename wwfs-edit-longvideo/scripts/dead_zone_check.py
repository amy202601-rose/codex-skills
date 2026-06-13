# -*- coding: utf-8 -*-
"""Energy envelope for the two regions where verbatim Whisper heard almost
nothing despite original transcript claiming words (C0022 752-760, 790-804)."""
import math, struct, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\C0022.MP4"
SR = 16000

for T0, T1, label in [(751.0, 761.0, "naked-options region"), (790.0, 804.5, "reclassify region")]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error",
                        "-ss", str(T0), "-to", str(T1), "-i", SRC,
                        "-vn", "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"],
                       capture_output=True, check=True)
    n = len(r.stdout) // 2
    samples = struct.unpack(f"<{n}h", r.stdout[:n * 2])
    WIN = SR // 10  # 100ms
    print(f"=== {label} {T0}-{T1} ===")
    bursts = []
    in_b = False
    for i in range(0, n - WIN, WIN):
        w = samples[i:i + WIN]
        rms = (sum(x * x for x in w) / WIN) ** 0.5
        db = 20 * math.log10(max(rms, 1) / 32768)
        t = T0 + i / SR
        loud = db > -38
        if loud and not in_b:
            bursts.append([t, t + 0.1])
            in_b = True
        elif loud:
            bursts[-1][1] = t + 0.1
        elif in_b and t - bursts[-1][1] > 0.25:
            in_b = False
    for a, b in bursts:
        if b - a >= 0.15:
            print(f"  speech {a:7.2f} - {b:7.2f}  ({b-a:.2f}s)")
    print()
