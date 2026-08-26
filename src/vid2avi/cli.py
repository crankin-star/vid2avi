import argparse
from pathlib import Path

from ffmpeg import FFmpeg  # pyright: ignore[reportMissingTypeStubs]


def build_parser():
    parser = argparse.ArgumentParser(description="Convert video files.")

    _ = parser.add_argument(
        "dir",
        type=Path,
        default=".",
        help="Directory containing the video files.",
    )

    _ = parser.add_argument(
        "-f",
        "--formats",
        nargs="+",
        default=[".mts", ".mp4"],
        help="File extensions to process (default: .mts .mp4).",
    )

    return parser


def main():
    parser = build_parser()

    args = parser.parse_args()

    if args.dir is None:
        dir = Path(".")
    else:
        dir = args.dir

    formats = {
        format if format.startswith(".") else "." + format for format in args.formats
    }

    files = [f for f in dir.iterdir() if f.is_file() and f.suffix.lower() in formats]

    if len(files) == 0:
        print(f"No files found with the extensions `{'`, `'.join(formats)}`")

    ffmpeg = FFmpeg().option("y")

    for file in files:
        ff = ffmpeg.input(file).output(
            str(file.parent / file.stem) + ".avi", {"codec:v": "mjpeg"}
        )
        ff.execute()


if __name__ == "__main__":
    main()
