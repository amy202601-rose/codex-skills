"""Patch-render changed B-roll intervals and concatenate with an existing edit.

This is a template. Copy it into the working project and adapt:
- PROJECT_SCRIPT: module containing BASE_VIDEO, OUTPUT, INTERVALS, SCENES, etc.
- CHANGED_INTERVALS: intervals to re-render from source.
- NEW_OUTPUT: final patched MP4.

The module is expected to expose MoviePy-compatible helpers like the ones used in
the finance evidence B-roll workflow: active_interval, BUILD_SECONDS, SCENES,
shifted, smooth, FPS, BASE_VIDEO, OUTPUT.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from moviepy import VideoClip, VideoFileClip


PROJECT_SCRIPT = "edit_a01_varied_finance_broll"
PROJECT_DIR = Path.cwd()
WORK_DIR = Path(r"C:\tmp\finance_broll_patch_segments")
NEW_OUTPUT = PROJECT_DIR / "patched_broll_output.mp4"
CHANGED_INTERVALS = [
    # (5.5, 13.0),
]


def ffmpeg_cut(ffmpeg: str, source: Path, start: float, end: float, out: Path, fps: int) -> None:
    cmd = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{start:.3f}",
        "-to",
        f"{end:.3f}",
        "-i",
        str(source),
        "-r",
        str(fps),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(out),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    sys.path.insert(0, str(PROJECT_DIR))
    project = importlib.import_module(PROJECT_SCRIPT)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    source_render = VideoFileClip(str(project.BASE_VIDEO))
    current = VideoFileClip(str(project.OUTPUT))
    duration = current.duration
    fps = int(project.FPS)

    segments: list[Path] = []
    cursor = 0.0
    index = 0

    def render_changed(start: float, end: float, out: Path) -> None:
        seg_duration = end - start

        def frame(local_t: float):
            t = start + local_t
            src = source_render.get_frame(t)
            active = project.active_interval(t)
            if not active:
                return src
            scene_start, scene_end, kind = active
            elapsed = t - scene_start
            progress = elapsed / project.BUILD_SECONDS[kind]
            broll = project.SCENES[kind](src, progress)
            broll = project.shifted(broll, elapsed)
            fade = min(project.smooth(elapsed / 0.30), project.smooth((scene_end - t) / 0.30))
            result = src.astype(np.float32) * (1 - fade) + np.asarray(broll).astype(np.float32) * fade
            return np.clip(result, 0, 255).astype(np.uint8)

        clip = VideoClip(frame, duration=seg_duration).with_fps(fps)
        if current.audio:
            clip = clip.with_audio(current.audio.subclipped(start, end))
        clip.write_videofile(
            str(out),
            fps=fps,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            bitrate="5500k",
            preset="veryfast",
            threads=4,
            logger=None,
        )
        clip.close()

    for start, end in CHANGED_INTERVALS:
        if start > cursor + 0.02:
            path = WORK_DIR / f"{index:03d}_copy_{cursor:.3f}_{start:.3f}.mp4"
            ffmpeg_cut(ffmpeg, Path(project.OUTPUT), cursor, start, path, fps)
            segments.append(path)
            index += 1

        path = WORK_DIR / f"{index:03d}_changed_{start:.3f}_{end:.3f}.mp4"
        render_changed(start, end, path)
        segments.append(path)
        index += 1
        cursor = end

    if cursor < duration - 0.02:
        path = WORK_DIR / f"{index:03d}_copy_{cursor:.3f}_{duration:.3f}.mp4"
        ffmpeg_cut(ffmpeg, Path(project.OUTPUT), cursor, duration, path, fps)
        segments.append(path)

    concat_file = WORK_DIR / "concat.txt"
    concat_file.write_text("".join(f"file '{str(p).replace(chr(92), '/')}'\n" for p in segments), encoding="utf-8")
    subprocess.run(
        [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(NEW_OUTPUT)],
        check=True,
    )

    source_render.close()
    current.close()
    print(NEW_OUTPUT)


if __name__ == "__main__":
    main()
