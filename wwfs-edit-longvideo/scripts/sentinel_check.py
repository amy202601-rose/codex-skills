# -*- coding: utf-8 -*-
"""Verify sentence-final sentinel words survived the aggressive end trims."""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
WORK = r"C:\Users\Lihao Wang\Desktop\Youtube素材、\ai_cut"
with open(os.path.join(WORK, "v3_qc.wav.words.json"), encoding="utf-8") as f:
    qc = json.load(f)["words"]
text = " ".join(w["w"] for w in qc)
print(f"total words: {len(qc)}")
for sentinel in ["Canada", "tolerable", "fine", "about", "sabotaging", "decade",
                 "obligation", "derivatives", "letter", "gamble", "captured"]:
    hits = len(re.findall(sentinel, text, re.I))
    print(f"  {sentinel}: {hits}x")

idx = [i for i, w in enumerate(qc) if "license" in w["w"].lower()]
for i in idx:
    ctx = " ".join(w["w"] for w in qc[max(0,i-5):i+8])
    print(f'[{qc[i]["s"]:.1f}s] ...{ctx}...')
