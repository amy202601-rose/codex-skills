# -*- coding: utf-8 -*-
"""Peak-normalize a video's audio before editing.

The script raises the audio so the detected max peak lands near target dB
(default -1 dB). It copies video streams and re-encodes audio only.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


KNOWN_FFMPEG = [
    r"C:\Program Files (x86)\Tubedown\Resource\ffmpeg.exe",
    r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
]


def find_ffmpeg(explicit: str | None) -> str:
    candidates = []
    if explicit:
        candidates.append(explicit)
    from_path = shutil.which("ffmpeg")
    if from_path:
        candidates.append(from_path)
    candidates.extend(KNOWN_FFMPEG)

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise SystemExit("ffmpeg not found. Install ffmpeg or pass --ffmpeg <path>.")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def detect_max_volume(ffmpeg: str, source: Path) -> float:
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-i",
        str(source),
        "-af",
        "volumedetect",
        "-vn",
        "-sn",
        "-dn",
        "-f",
        "null",
        os.devnull,
    ]
    proc = run(cmd)
    text = proc.stderr + "\n" + proc.stdout
    match = re.search(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", text)
    if not match:
        raise SystemExit("Could not detect max_volume from ffmpeg output.")
    return float(match.group(1))


def default_output(source: Path) -> Path:
    return source.with_name(f"{source.stem}.normalized{source.suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize video audio peak before cutting."
    )
    parser.add_argument("source", help="Input video path")
    parser.add_argument("--output", "-o", help="Output video path")
    parser.add_argument(
        "--target-peak",
        type=float,
        default=-1.0,
        help="Target max peak in dB. Default: -1.0",
    )
    parser.add_argument("--ffmpeg", help="Explicit ffmpeg.exe path")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output if it already exists",
    )
    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"Input video not found: {source}")
    output = Path(args.output) if args.output else default_output(source)
    if output.exists() and not args.force:
        raise SystemExit(f"Output already exists, pass --force to replace: {output}")

    ffmpeg = find_ffmpeg(args.ffmpeg)
    max_volume = detect_max_volume(ffmpeg, source)
    gain = args.target_peak - max_volume

    print(f"max_volume={max_volume:.2f} dB")
    print(f"target_peak={args.target_peak:.2f} dB")
    print(f"gain={gain:.2f} dB")

    cmd = [
        ffmpeg,
        "-y" if args.force else "-n",
        "-hide_banner",
        "-i",
        str(source),
        "-map",
        "0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-af",
        f"volume={gain:.3f}dB",
        "-movflags",
        "+faststart",
        str(output),
    ]
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        return proc.returncode
    print(f"normalized_video={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
