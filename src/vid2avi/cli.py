import argparse
from pathlib import Path

from ffmpeg import (  # pyright: ignore[reportMissingTypeStubs]
    FFmpeg,
    FFmpegFileNotFound,
    FFmpegInvalidCommand,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Convert video file directories to avi."
    )

    _ = parser.add_argument(
        "-d",
        "--dir",
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
    
    _ = parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: .).",
    )

    _ = parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively process subdirectories (default: False).",
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

    if args.recursive:
        files = [
            f for f in dir.rglob("*") if f.is_file() and (f.suffix.lower() in formats)
        ]
    else:
        files = [
            f for f in dir.iterdir() if f.is_file() and (f.suffix.lower() in formats)
        ]

    output_dir = Path(args.output).absolute() if args.output is not None else None
    if output_dir is not None and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    if len(files) == 0:
        print(f"No files found with the extensions `{'`, `'.join(formats)}`")

    ffmpeg = FFmpeg().option("y")

    for file in files:
        # use output dir if specified, else use original file's dir
        output_dir = output_dir if output_dir is not None else file.parent.absolute()
        try:
            fp = str(output_dir / file.stem) + ".avi"
            ff = ffmpeg.input(file).output(fp, {"codec:v": "mjpeg"})
            _ = ff.execute()
            print(file, "converted to", fp)
        except FFmpegFileNotFound as e:
            print("An exception has occurred!")
            print("- Message from ffmpeg:", e.message)
            print("- Arguments to execute ffmpeg:", e.arguments)
        except FFmpegInvalidCommand as e:
            print("An exception has occurred!")
            print("- Message from ffmpeg:", e.message)
            print("- Arguments to execute ffmpeg:", e.arguments)


if __name__ == "__main__":
    main()
