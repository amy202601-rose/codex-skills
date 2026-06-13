# -*- coding: utf-8 -*-
"""Calibrate dB + zero-crossing-rate thresholds on known regions:
- C0022 23.4-24.3: "Canada." vowel decay + the breath blip (should be DEAD)
- C0022 144.5-145.3: "returns." with trailing s fricative (should be SPEECH)"""
import math, struct, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\C0022.MP4"
SR = 16000
WIN = SR // 100  # 10ms

for T0, T1, label in [(23.3, 24.3, "Canada + breath blip"), (144.5, 145.4, "returns + s tail")]:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error",
                        "-ss", str(T0), "-to", str(T1), "-i", SRC,
                        "-vn", "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"],
                       capture_output=True, check=True)
    n = len(r.stdout) // 2
    s = struct.unpack(f"<{n}h", r.stdout[:n * 2])
    print(f"=== {label} ({T0}-{T1}) ===")
    print("time    dB     ZCR/frame")
    for i in range(0, n - WIN, WIN):
        w = s[i:i + WIN]
        rms = (sum(x * x for x in w) / WIN) ** 0.5
        db = 20 * math.log10(max(rms, 1) / 32768)
        zc = sum(1 for a, b in zip(w, w[1:]) if (a < 0) != (b < 0))
        t = T0 + i / SR
        if db > -60:
            print(f"{t:6.2f}  {db:6.1f}  {zc:3d}")
    print()
