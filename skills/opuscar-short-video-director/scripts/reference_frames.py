#!/usr/bin/env python3
"""Extract timestamped, mobile-scale reference or proof frames from a local video."""
import argparse
import io
import json
import math
from pathlib import Path
import subprocess
import sys


def run(command):
    return subprocess.run(command, check=True, capture_output=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="Output PNG or JPEG contact sheet")
    parser.add_argument("--start", type=float, default=0, help="First cue in seconds")
    parser.add_argument("--step", type=float, default=2, help="Seconds between cues")
    parser.add_argument("--count", type=int, default=12, help="Maximum number of frames")
    args = parser.parse_args()
    if not args.video.is_file():
        parser.error("video must be a local file")
    if (not math.isfinite(args.start) or args.start < 0 or
            not math.isfinite(args.step) or args.step <= 0 or not 1 <= args.count <= 64):
        parser.error("start must be nonnegative, step positive, and count between 1 and 64")
    if args.out.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        parser.error("output must be PNG or JPEG")
    if args.out.exists():
        parser.error("output already exists")
    try:
        from PIL import Image, ImageDraw

        video = str(args.video.resolve())
        data = json.loads(run([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration,avg_frame_rate:format=duration",
            "-of", "json", video,
        ]))
        stream = data["streams"][0]
        duration = float(stream.get("duration", data.get("format", {}).get("duration", "nan")))
        if not math.isfinite(duration) or duration <= args.start:
            raise ValueError("video duration unavailable, or start is outside the video")
        cues = [args.start + i * args.step for i in range(args.count)
                if args.start + i * args.step < duration]
        columns = min(4, len(cues))
        width, height = 320, 360
        sheet = Image.new("RGB", (width * columns, (height + 24) * math.ceil(len(cues) / columns)), "#191919")
        draw = ImageDraw.Draw(sheet)
        captured = []
        for cue in cues:
            raw = run([
                "ffmpeg", "-v", "error", "-ss", f"{cue:.6f}", "-i", video,
                "-map", "0:v:0", "-an", "-frames:v", "1", "-vf",
                f"scale={width}:{height}:force_original_aspect_ratio=decrease",
                "-c:v", "png", "-f", "image2pipe", "-",
            ])
            if not raw:
                continue
            frame = Image.open(io.BytesIO(raw)).convert("RGB")
            x = len(captured) % columns * width
            y = len(captured) // columns * (height + 24)
            sheet.paste(frame, (x + (width - frame.width) // 2, y + (height - frame.height) // 2))
            draw.text((x + 8, y + height + 4), f"Cue {cue:.3f}s", fill="white")
            captured.append(round(cue, 6))
        if not captured:
            raise ValueError("no frame available at or after the requested cues")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        rows = math.ceil(len(captured) / columns)
        sheet.crop((0, 0, sheet.width, rows * (height + 24))).save(args.out)
        print(json.dumps({
            "image": str(args.out), "requested_cues_seconds": cues, "captured_cues_seconds": captured,
            "source": stream, "duration_seconds": duration, "review": "sampled frames only",
        }, indent=2))
        return 0
    except (OSError, IndexError, KeyError, ImportError, ValueError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr.decode(errors="replace").strip() if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        print(f"Reference frame extraction failed: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
