# -*- coding: utf-8 -*-
"""
v3 build: same keep_final.json selection as v2, plus audio-driven pause
compression to kill breath gaps (气口):
  - piece edges snap to real speech boundaries (silences.json from ffmpeg)
  - every internal silence longer than MAX_PAUSE is compressed to ~TARGET_PAUSE
  - optional DROP_RANGES for retakes confirmed after review
Outputs v3_pieces.txt + a JianYing draft named AI精剪_TFSA_v3_*.
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")

SRC_DIR = r"C:\Users\Lihao Wang\Desktop\Youtube素材、"
WORK = os.path.join(SRC_DIR, "ai_cut")
DRAFT_ROOT = os.path.expandvars(r"%USERPROFILE%\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft")
DRAFT_NAME = "AI精剪_TFSA_0613_v3n"
CLIPS = ["C0022.MP4", "C0023.MP4", "C0024.MP4", "C0025.MP4", "C0026.MP4"]
CLIP_DUR = {"C0022.MP4": 974.474, "C0023.MP4": 385.886, "C0024.MP4": 102.603,
            "C0025.MP4": 190.691, "C0026.MP4": 309.309}
PAD_START, PAD_END = 0.15, 0.25
MERGE_GAP = 1.2

# pause compression — Wallace's rules (2026-06-12):
# 1) After a COMPLETE SENTENCE: kill near-zero-dB tails and the inhale before
#    the next sentence (inhale sits right before speech onset → resume 0.05s
#    before the word and it's gone).
# 2) MID-SENTENCE small pauses (0.2-0.5s) are natural speech rhythm — leave
#    them alone; only compress real stalls (>0.7s), and gently.
# Sentence ends are detected from transcript punctuation (.?!), with a >1.0s
# gap as fallback for missing punctuation.
MAX_PAUSE = 0.30      # sentence-end gaps longer than this get compressed...
KEEP_TAIL = 0.14      # ...keeping this much after the last word (word decay)
KEEP_LEAD = 0.05      # ...and this much before the next word (inhale lives here — keep tight)
MID_MAX_PAUSE = 0.70  # mid-sentence: only compress stalls longer than this
MID_KEEP_TAIL = 0.15
MID_KEEP_LEAD = 0.08
EDGE_TAIL = 0.14      # piece end: max trailing silence kept
EDGE_LEAD = 0.05      # piece start: max leading silence kept

SENT_PUNCT = (".", "?", "!")


def is_sentence_end(word_text, gap):
    return word_text.rstrip("\"')]}").endswith(SENT_PUNCT) or gap > 1.0

# confirmed retakes to drop, as (clip_name, src_start, src_end).
# Found by round-trip QC (transcribe the rendered cut, scan stutters) 2026-06-11.
DROP_RANGES = [
    ("C0022.MP4", 55.30, 58.45),    # false start "I've been a financial planner... over..." (retake at 58.58)
    ("C0022.MP4", 145.07, 145.50),  # dangling "and" before a cut ("returns." ends 145.06 — start after it)
    ("C0022.MP4", 643.90, 645.62),  # "So if we, so if," double false start ("so if we flip" at 645.72)
    ("C0022.MP4", 871.70, 872.00),  # dangling "so" after "It's a pattern" ("pattern." ends 871.66)
    ("C0022.MP4", 879.50, 881.13),  # "so and this" false start (keeper at 881.23)
    ("C0023.MP4", 125.95, 126.43),  # "It's not" false start before "Not every brokerage"
    ("C0026.MP4", 98.10, 99.08),    # first "like a" of "like a like a 70 to 80%"
    ("C0026.MP4", 107.50, 109.69),  # "And, and then if you are," false start (keeper at 109.75)
    # round-2 QC findings (transcription variance surfaces different misses each run)
    # REVERTED: ("C0022.MP4", 404.58, 404.95) "cash, cash" — the two words are
    # adjacent with no gap; cutting clipped the second one and created a worse
    # "can be can be" artifact. It's an emphasis bridge, leave it.
    ("C0022.MP4", 657.38, 659.36),  # dangling "so" + first "that's entire" (keeper at 659.42)
    ("C0023.MP4", 329.70, 331.36),  # drawn-out "Well," restart (keeper "well" at 331.46)
    # suspect-word scan (overlong words in original transcript hide merged retakes;
    # verified by verbatim re-transcription with filler prompt)
    ("C0022.MP4", 16.00, 18.21),    # "So your TF— so your," double false start (keeper "so your TFSA" at 18.29)
    ("C0022.MP4", 193.00, 194.96),  # "the difference, and the," double false start (keeper "and the difference" at 195.04)
    ("C0022.MP4", 215.50, 217.30),  # "so in the past," false start + keeper's detached "so [0.5s pause]" (Wallace: cut it; sentence starts at "in the past few years" 217.38)
    ("C0022.MP4", 265.40, 269.79),  # "at number three what / what's your" double false start (keeper at 269.87)
    ("C0022.MP4", 768.90, 770.48),  # "but here's that," false start (keeper "but here's the part" at 770.56)
    ("C0022.MP4", 776.70, 780.70),  # "so if this, if, okay, so if CRA likes, okay, if, okay," stumble (keeper "if CRA looks" at 780.78)
    ("C0022.MP4", 787.55, 788.70),  # "like, uh," filler before "professionally"
    ("C0022.MP4", 951.60, 953.29),  # "the first thing," false start (keeper at 953.37)
    ("C0023.MP4", 76.60, 78.08),    # "second thing is," false start (keeper "and the second thing is" at 78.16)
    ("C0024.MP4", 33.45, 34.59),    # dead pause hidden inside bogus "15" word timestamps
    ("C0025.MP4", 15.10, 17.45),    # "The hack number, the hack number two," double false start (keeper at 17.53)
    ("C0026.MP4", 21.40, 22.91),    # "and on the same account," self-correction (keeper "and on the same amount" at 22.99)
    # round-4 QC (verbatim prompt exposes stutters plain transcription smoothed over)
    ("C0022.MP4", 33.90, 34.68),    # first "And," of "And, and the bank" (keeper at 34.76)
    ("C0025.MP4", 31.05, 31.39),    # first "where" of "where where the capital gains" (keeper at 31.47)
    ("C0026.MP4", 281.20, 281.94),  # first "So if" of CTA "So if, so if you think" (keeper at 282.02)
    # round-5 QC
    ("C0025.MP4", 169.60, 170.33),  # "And it—" restart ("It costs you nothing" at 170.41)
    ("C0026.MP4", 285.47, 285.81),  # first "and" of "hit the like and, and subscribe" (keeper at 285.89)
    # round-6 QC
    ("C0022.MP4", 139.40, 139.95),  # first "or" of "right or, or something balanced" ("right?" ends 139.38)
    ("C0022.MP4", 764.80, 765.08),  # first "on" of "take on, on that kind of obligation" ("take" ends 764.78)
    # round-7 QC
    ("C0023.MP4", 141.33, 141.71),  # "is you—" restart ("You can hold US listed stocks" at 141.79)
    # round-10: dead air blocked from energy cutting by bogus word spans
    ("C0022.MP4", 708.41, 709.04),  # 0.86s dead pause in "Because [pause] there are limits"
    ("C0022.MP4", 793.63, 796.72),  # "and they can re—" false start hidden in bogus "-classify" span (keeper "and they can re-classify" at 796.80)
    # round-13 QC
    ("C0022.MP4", 651.12, 651.60),  # first "on" of "zero tax on, on the 240,000" (keeper at 651.68)
    # round-15: dangling "and" after "rest of your life" left behind by the
    # 193-195 false-start cut (energy end-trim will resnap to "life")
    ("C0022.MP4", 189.60, 190.50),
    # round-16 (Wallace's JianYing caption-gap method): trailing connectives
    # left from deleted retake openings — captions show gaps there
    ("C0022.MP4", 204.80, 205.40),  # pause+breath after "maybe even more." ("more." ends 204.74; the reported trailing "so" was a transcription hallucination)
    ("C0022.MP4", 238.72, 239.40),  # trailing "So" after "they could do more"
    # round-17: JianYing SRT cross-check findings (all in Whisper-verbatim
    # dropout zones — the second recognizer sees what the first can't)
    ("C0022.MP4", 284.30, 285.12),  # clipped "and" fragment before "number four" (captioned as "there")
    ("C0022.MP4", 480.30, 480.68),  # clipped "so" head before "the difference" ("so the diff" relic)
    ("C0025.MP4", 34.40, 41.20),    # take 1 of "So the highest volatility, the highest growth potential investments"
    ("C0025.MP4", 80.85, 82.93),    # "So just flip it." (keeper: "So you can just flip it, where's probably...")
    ("C0026.MP4", 243.30, 247.45),  # early ending take "And that's it ×2. That's the entire game. Five blocks."
]

WIDTH, HEIGHT, FPS = 3840, 2160, 30


def norm(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


raw_words = []
for idx, clip in enumerate(CLIPS):
    with open(os.path.join(WORK, clip + ".words.json"), encoding="utf-8") as f:
        for w in json.load(f)["words"]:
            n = norm(w["w"])
            if n:
                raw_words.append({"clip": idx, "s": w["s"], "e": w["e"], "w": w["w"], "n": n})

lines = []
cur = []
for i, w in enumerate(raw_words):
    if cur:
        prev = raw_words[i - 1]
        gap = w["s"] - prev["e"]
        new_clip = w["clip"] != prev["clip"]
        sent_end = re.search(r"[.?!]$", prev["w"]) and gap > 0.25
        if new_clip or gap > 0.6 or sent_end or len(cur) >= 28:
            lines.append(cur)
            cur = []
    cur.append(i)
if cur:
    lines.append(cur)

with open(os.path.join(WORK, "lines.json"), encoding="utf-8") as f:
    ref = json.load(f)
assert len(lines) == len(ref), f"line count mismatch {len(lines)} vs {len(ref)}"

with open(os.path.join(WORK, "keep_final.json"), encoding="utf-8") as f:
    keeps = json.load(f)["keeps"]

with open(os.path.join(WORK, "silences.json"), encoding="utf-8") as f:
    silences = json.load(f)


def find_phrase(norms, phrase, occ):
    toks = phrase.split()
    hits = [i for i in range(len(norms) - len(toks) + 1) if norms[i:i + len(toks)] == toks]
    if not hits:
        return None
    return hits[-1] if occ == "last" else hits[0]


ranges = []
problems = []
for k in keeps:
    idxs = lines[k["id"]]
    ws = [raw_words[i] for i in idxs]
    norms = [w["n"] for w in ws]
    a, b = 0, len(ws) - 1
    if "from" in k:
        pos = find_phrase(norms, k["from"], k.get("occ", "first"))
        if pos is None:
            problems.append(f"L{k['id']}: from-phrase NOT FOUND: {k['from']}")
        else:
            a = pos
    if "to" in k:
        toks = k["to"].split()
        pos = None
        for i in range(len(norms) - len(toks), a - 1, -1):
            if norms[i:i + len(toks)] == toks:
                pos = i + len(toks) - 1
                break
        if pos is None:
            problems.append(f"L{k['id']}: to-phrase NOT FOUND: {k['to']}")
        else:
            b = pos
    ranges.append((ws[0]["clip"], ws[a]["s"], ws[b]["e"], k["id"]))

if problems:
    print("PHRASE PROBLEMS:")
    for p in problems:
        print(" ", p)
    raise SystemExit(1)

merged = []
for c, s, e, lid in ranges:
    if merged and merged[-1][0] == c and s - merged[-1][2] <= MERGE_GAP:
        merged[-1][2] = e
    else:
        merged.append([c, s, e])

# pad, clamp, fix overlap (same as v2)
padded = []
for c, s, e in merged:
    s = max(0.0, s - PAD_START)
    e = min(CLIP_DUR[CLIPS[c]], e + PAD_END)
    if padded and padded[-1][0] == c and s < padded[-1][2]:
        s = padded[-1][2]
    if e - s > 0.05:
        padded.append([c, s, e])

# apply confirmed retake drops
drops = [(CLIPS.index(n), a, b) for n, a, b in DROP_RANGES]
dropped = []
for c, s, e in padded:
    cuts = sorted([(max(s, a), min(e, b)) for dc, a, b in drops if dc == c and a < e and b > s])
    cur_s = s
    for a, b in cuts:
        if a - cur_s > 0.05:
            dropped.append([c, cur_s, a])
        cur_s = max(cur_s, b)
    if e - cur_s > 0.05:
        dropped.append([c, cur_s, e])

# --- pause compression: word gaps decide, audio silences refine cut points ---
pieces = []
n_edge_trims = n_pause_cuts = 0
trimmed_time = 0.0
for c, s, e in dropped:
    sils = [(a, b) for a, b in silences[CLIPS[c]] if b > s and a < e]
    # words inside the piece — their boundaries are hard limits for edge trims
    # (silencedetect misses soft speech like a quiet "So", so it alone may cut
    # into a word; Whisper word times win)
    in_words = [w for w in raw_words
                if w["clip"] == c and w["s"] >= s - 0.15 and w["e"] <= e + 0.15]
    first_ws = in_words[0]["s"] if in_words else None
    last_we = in_words[-1]["e"] if in_words else None
    # snap edges to speech (audio-based, clamped to word boundaries)
    new_s, new_e = s, e
    for a, b in sils:
        if a <= s and b > s:                      # silence overlaps piece start
            cand = min(b - EDGE_LEAD, e)
            if first_ws is not None:
                cand = min(cand, first_ws - 0.08)
            if cand > new_s:
                trimmed_time += cand - new_s
                new_s = cand
                n_edge_trims += 1
        if a < e and b >= e:                      # silence overlaps piece end
            cand = max(a + EDGE_TAIL, s)
            if last_we is not None:
                cand = max(cand, last_we + 0.12)
            if cand < new_e:
                trimmed_time += new_e - cand
                new_e = cand
                n_edge_trims += 1
    if new_e - new_s <= 0.05:
        continue
    in_words = [w for w in in_words if w["s"] >= new_s - 0.01 and w["e"] <= new_e + 0.01]
    subs = []
    cur_s = new_s
    for wa, wb in zip(in_words, in_words[1:]):
        gap = wb["s"] - wa["e"]
        sent_end = is_sentence_end(wa["w"], gap)
        if gap <= (MAX_PAUSE if sent_end else MID_MAX_PAUSE):
            continue
        tail = KEEP_TAIL if sent_end else MID_KEEP_TAIL
        lead = KEEP_LEAD if sent_end else MID_KEEP_LEAD
        # pure word-boundary cuts: the inhale sits right before the next word's
        # onset, so resuming at wb.s - lead removes it. Do NOT widen the
        # resume point using silencedetect — breath noise ends "silence" early
        # and would re-include the inhale.
        cut_a, cut_b = wa["e"] + tail, wb["s"] - lead
        if cut_b - cut_a > 0.05 and cut_a > cur_s and cut_b < new_e:
            subs.append([c, cur_s, cut_a])
            cur_s = cut_b
            n_pause_cuts += 1
            trimmed_time += cut_b - cut_a
    if new_e - cur_s > 0.05:
        subs.append([c, cur_s, new_e])
    pieces.extend(subs)

# --- energy-envelope dead-air removal (Wallace's 0-dB rule) ---
# Word timestamps lie (bogus multi-second words) and silencedetect lies
# (breath noise). The RMS envelope is ground truth: trim every piece end back
# to the last actually-audible moment, and cut internal true-silence runs.
import pickle, struct, subprocess

ENERGY_FLOOR = -44.0   # below this = dead air (room tone sits lower)
HOP = 0.01             # envelope resolution, seconds
DEAD_MIN = 0.40        # sentence-end silent runs longer than this get cut
MID_DEAD_MIN = 0.70    # mid-sentence: natural micro-pauses stay
TAIL_KEEP = 0.12       # keep after last audible moment
LEAD_KEEP = 0.05

# per-clip word index for sentence-boundary lookup in the energy pass
import bisect

word_ends = {}
word_texts = {}
word_starts = {}
for ci in range(len(CLIPS)):
    ws = [w for w in raw_words if w["clip"] == ci]
    word_ends[ci] = [w["e"] for w in ws]
    word_texts[ci] = [w["w"] for w in ws]
    word_starts[ci] = [w["s"] for w in ws]


# Quiet word tails (fricatives, trailing vowels: "returns", "do.", "Because")
# drop below the energy floor before the word actually ends — an unclamped
# energy cut chops them mid-word. Clamp every energy cut point to word
# boundaries: a kept-audio END inside a word extends past it; a RESUME point
# inside a word pulls back before it.
def clamp_keep_end(c, t):
    # extension capped at 0.40s: real quiet tails are short; a bogus
    # multi-second word must NOT block dead-air removal
    i = bisect.bisect_right(word_starts[c], t) - 1
    if i >= 0 and word_starts[c][i] <= t < word_ends[c][i]:
        return min(word_ends[c][i] + 0.06, t + 0.40)
    return t


def clamp_resume(c, t):
    i = bisect.bisect_right(word_starts[c], t) - 1
    if i >= 0 and word_starts[c][i] < t <= word_ends[c][i]:
        return max(word_starts[c][i] - 0.04, t - 0.40)
    return t


def sentence_end_before(c, t, run_len):
    i = bisect.bisect_right(word_ends[c], t + 0.05) - 1
    if i < 0:
        return True
    return is_sentence_end(word_texts[c][i], run_len)

env_cache = os.path.join(WORK, "envelopes2.pkl")   # (dB, zero-crossings) per 10ms
if os.path.exists(env_cache):
    with open(env_cache, "rb") as f:
        envs = pickle.load(f)
else:
    import math
    envs = {}
    SRr = 16000
    win = int(SRr * HOP)
    for ci, clip in enumerate(CLIPS):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error",
                            "-i", os.path.join(SRC_DIR, clip),
                            "-vn", "-ar", str(SRr), "-ac", "1", "-f", "s16le", "-"],
                           capture_output=True, check=True)
        n = len(r.stdout) // 2
        samples = struct.unpack(f"<{n}h", r.stdout[:n * 2])
        env = []
        for i in range(0, n - win, win):
            w = samples[i:i + win]
            rms = (sum(x * x for x in w) / win) ** 0.5
            db = 20 * math.log10(max(rms, 1) / 32768)
            zc = sum(1 for a, b in zip(w, w[1:]) if (a < 0) != (b < 0))
            env.append((db, zc))
        envs[ci] = env
        print(f"envelope {clip}: {len(env)} frames")
    with open(env_cache, "wb") as f:
        pickle.dump(envs, f)


# Speech detection = frame taxonomy + REGION GROWING (2026-06-12 final):
#   strong voice    db > -30
#   sibilant        db > -48 and ZCR >= 38      ("s/z" fricatives)
# Soft word tails ("-ble" of "gamble": -30..-38dB, ZCR 21-36) share the
# breath's frame signature, so frames alone can't separate them. Continuity
# can: a word tail is ATTACHED to strong voice (no silence between), a breath
# is always preceded by a dip. Speech regions grow rightward through
# continuous > -42dB audio; isolated blobs (breaths) never join.
def speech_mask(c, s, e):
    """Return (frames, mask, i0) for piece [s,e]: mask[k] True = speech."""
    env = envs[c]
    i0, i1 = int(s / HOP), int(e / HOP) + 1
    fr = [env[i] if 0 <= i < len(env) else (-90.0, 0) for i in range(i0, i1)]
    mask = [db > -30.0 or (db > -48.0 and zc >= 38) for db, zc in fr]
    for k in range(1, len(fr)):
        if not mask[k] and mask[k - 1] and fr[k][0] > -42.0:
            mask[k] = True
    return fr, mask, i0


def blob_trim(fr, i0, t_from, t_to):
    """Shorten the keep-margin (t_from, t_to) to just before the first
    audible (-40dB+) blob inside it — that blob is a breath, not speech."""
    k0 = max(0, int(t_from / HOP) - i0 + 1)
    k1 = min(len(fr), int(t_to / HOP) - i0 + 1)
    for k in range(k0, k1):
        # breath signature = audible AND mid ZCR; voiced decay tails
        # ("gamble"'s fading -l, ZCR 2-18) are NOT blobs and stay
        if fr[k][0] > -40.0 and fr[k][1] >= 21:
            return max(t_from + 0.02, (i0 + k) * HOP - 0.01)
    return t_to


# frame-level audibility (for tail-extension + verification): anything above
# -40dB, or a quiet sibilant, counts as audible
def loud(c, t):
    env = envs[c]
    i = int(t / HOP)
    if not (0 <= i < len(env)):
        return False
    db, zc = env[i]
    return db > -40.0 or (db > -48.0 and zc >= 38)


energy_pieces = []
n_end_trims = n_dead_cuts = 0
energy_removed = 0.0
for c, s, e in pieces:
    fr, mask, i0 = speech_mask(c, s, e)

    def tt(k):
        return (i0 + k) * HOP

    speech_idx = [k for k, m in enumerate(mask) if m]
    if not speech_idx:
        continue
    # 1) end trim: last speech frame + TAIL_KEEP, breath blobs in the margin cut off
    last = speech_idx[-1]
    new_e = min(e, blob_trim(fr, i0, tt(last) + HOP, tt(last) + TAIL_KEEP))
    new_e = max(new_e, tt(last) + HOP)
    if e - new_e > 0.02:
        n_end_trims += 1
        energy_removed += e - new_e
    # 2) start trim: first speech frame - LEAD_KEEP
    first = speech_idx[0]
    new_s = max(s, clamp_resume(c, tt(first) - LEAD_KEEP))
    if new_s - s > 0.02:
        energy_removed += new_s - s
    if new_e - new_s <= 0.05:
        continue
    # 3) internal dead runs (mask-based, margins blob-trimmed)
    subs = []
    cur = new_s
    prev_k = None
    for k in speech_idx:
        if prev_k is not None and k - prev_k > 1:
            run_start, run_end = tt(prev_k) + HOP, tt(k)
            if run_end > new_e or run_start < new_s:
                prev_k = k
                continue
            run_len = run_end - run_start
            sent = sentence_end_before(c, run_start, run_len)
            min_run = DEAD_MIN if sent else MID_DEAD_MIN
            tail = TAIL_KEEP if sent else MID_KEEP_TAIL
            lead = LEAD_KEEP if sent else MID_KEEP_LEAD
            if run_len > min_run:
                a = blob_trim(fr, i0, run_start + 0.02, clamp_keep_end(c, run_start + tail))
                b = clamp_resume(c, run_end - lead)
                if b - a > 0.05 and a > cur and b < new_e:
                    subs.append([c, cur, a])
                    cur = b
                    n_dead_cuts += 1
                    energy_removed += b - a
        prev_k = k
    if new_e - cur > 0.05:
        subs.append([c, cur, new_e])
    energy_pieces.extend(subs)
pieces = energy_pieces
print(f"energy pass: {n_end_trims} end trims, {n_dead_cuts} dead-air cuts, {energy_removed:.1f}s removed")

# NOTE: the former auto tail-extension pass is REMOVED. Its job (restoring
# energy-clipped word tails) is fully covered by region-growing speech
# detection, and it twice re-captured the onset of deliberately dropped
# words ("so"/"So" retake openers sitting 0.01s after the previous word).

# verification A: no piece boundary may land inside a word (clipped-word check)
def word_at(c, t):
    i = bisect.bisect_right(word_starts[c], t) - 1
    if i >= 0 and word_starts[c][i] < t - 0.02 and t + 0.02 < word_ends[c][i]:
        return word_texts[c][i], word_starts[c][i], word_ends[c][i]
    return None


clipped = []
for c, s, e in pieces:
    for t, kind in ((s, "head"), (e, "tail")):
        hit = word_at(c, t)
        if hit:
            clipped.append(f'{CLIPS[c]} {kind}@{t:.2f} inside "{hit[0]}" {hit[1]:.2f}-{hit[2]:.2f}')
print(f"clipped-word boundaries: {len(clipped)}")
for x in clipped[:20]:
    print("  " + x)

# verification B: no remaining dead run >= DEAD_MIN inside any piece
worst = 0.0
for c, s, e in pieces:
    t = s
    run = 0.0
    while t < e:
        run = run + HOP if not loud(c, t) else 0.0
        worst = max(worst, run)
        t += HOP
print(f"longest remaining dead run inside pieces: {worst:.2f}s (must be < {MID_DEAD_MIN}s)")

total = sum(e - s for c, s, e in pieces)
print(f"keeps: {len(keeps)} -> merged {len(merged)} -> after drops {len(dropped)} -> final {len(pieces)} pieces")
print(f"edge trims: {n_edge_trims}, pause cuts: {n_pause_cuts}, time removed vs v2: {trimmed_time:.1f}s")
print(f"final duration: {total:.1f}s ({total/60:.2f} min)")

with open(os.path.join(WORK, "v3_pieces.txt"), "w", encoding="utf-8") as f:
    for c, s, e in pieces:
        f.write(f"{CLIPS[c]}  {s:8.2f} - {e:8.2f}  ({e-s:6.2f}s)\n")

import pyJianYingDraft as draft
from pyJianYingDraft import trange, TrackType

folder = draft.DraftFolder(DRAFT_ROOT)
script = folder.create_draft(DRAFT_NAME, WIDTH, HEIGHT, fps=FPS, allow_replace=True)
script.add_track(TrackType.video)
materials = {i: draft.VideoMaterial(os.path.join(SRC_DIR, c)) for i, c in enumerate(CLIPS)}

US = 1_000_000
cursor = 0
for c, s, e in pieces:
    dur = int(round((e - s) * US))
    seg = draft.VideoSegment(materials[c], trange(cursor, dur),
                             source_timerange=trange(int(round(s * US)), dur))
    script.add_segment(seg)
    cursor += dur

script.save()
print(f"DRAFT SAVED: {DRAFT_NAME} ({cursor/US/60:.2f} min, {len(pieces)} segments)")
