# -*- coding: utf-8 -*-
"""Probe SOURCE clip dB+ZCR frames for a window (10ms)."""
import math, struct, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\C0022.MP4"
T0 = float(sys.argv[1]); T1 = float(sys.argv[2])
SR = 16000
WIN = SR // 100
r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error",
                    "-ss", str(T0), "-to", str(T1), "-i", SRC,
                    "-vn", "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"],
                   capture_output=True, check=True)
n = len(r.stdout) // 2
s = struct.unpack(f"<{n}h", r.stdout[:n * 2])
for i in range(0, n - WIN, WIN):
    w = s[i:i + WIN]
    rms = (sum(x * x for x in w) / WIN) ** 0.5
    db = 20 * math.log10(max(rms, 1) / 32768)
    zc = sum(1 for a, b in zip(w, w[1:]) if (a < 0) != (b < 0))
    sp = "SPEECH" if (db > -30 or (db > -48 and zc >= 38) or (db > -38 and zc <= 20)) else "dead"
    print(f"{T0 + i/SR:7.2f}  {db:6.1f}  zcr{zc:4d}  {sp}")
