# -*- coding: utf-8 -*-
"""RMS probe of the rendered final audio (v3_qc.wav) for a given window —
20ms resolution, shows exactly what the ear hears at a boundary."""
import math, struct, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
WAV = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\ai_cut\v3_qc.wav"
T0 = float(sys.argv[1]) if len(sys.argv) > 1 else 4.5
T1 = float(sys.argv[2]) if len(sys.argv) > 2 else 7.5
SR = 16000

r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error",
                    "-ss", str(T0), "-to", str(T1), "-i", WAV,
                    "-f", "s16le", "-"], capture_output=True, check=True)
n = len(r.stdout) // 2
samples = struct.unpack(f"<{n}h", r.stdout[:n * 2])
WIN = SR // 50
for i in range(0, n - WIN, WIN):
    w = samples[i:i + WIN]
    rms = (sum(x * x for x in w) / WIN) ** 0.5
    db = 20 * math.log10(max(rms, 1) / 32768)
    t = T0 + i / SR
    print(f"{t:6.2f}  {db:6.1f}  {'#' * max(0, int((db + 62) / 2))}")
