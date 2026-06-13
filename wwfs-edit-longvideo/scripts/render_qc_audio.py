# -*- coding: utf-8 -*-
"""Render the final timeline AUDIO from v3_pieces.txt (16kHz mono wav) so the
result can be re-transcribed as a round-trip QC of the actual cut."""
import os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC, "ai_cut")
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
PIECES_FILE = sys.argv[1] if len(sys.argv) > 1 else "v3_pieces.txt"
OUT_WAV = os.path.join(WORK, PIECES_FILE.replace("_pieces.txt", "") + "_qc.wav")

pieces = []
with open(os.path.join(WORK, PIECES_FILE), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"(C\d+\.MP4)\s+([\d.]+)\s*-\s*([\d.]+)", line)
        if m:
            pieces.append((m.group(1), float(m.group(2)), float(m.group(3))))

tmp_dir = os.path.join(WORK, "qc_tmp")
os.makedirs(tmp_dir, exist_ok=True)
list_path = os.path.join(tmp_dir, "concat.txt")
with open(list_path, "w", encoding="utf-8") as lf:
    for i, (clip, s, e) in enumerate(pieces):
        seg = os.path.join(tmp_dir, f"p{i:04d}.wav")
        if not os.path.exists(seg):
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                            "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", os.path.join(SRC, clip),
                            "-vn", "-ar", "16000", "-ac", "1", seg], check=True)
        lf.write(f"file 'p{i:04d}.wav'\n")
        if i % 40 == 0:
            print(f"{i}/{len(pieces)}", flush=True)

subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "concat", "-safe", "0", "-i", list_path, OUT_WAV], check=True)
print(f"rendered {OUT_WAV}")
