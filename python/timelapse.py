import argparse
from pathlib import Path


def get_info(folder):
    f = sorted(folder.iterdir())[0]
    index = 0
    for i, c in enumerate(f.name):
        if c.isdigit():
            index = i
            break
    endpos = f.name.find(f.suffix)
    filename = str(f.name)[:index] + f"%0{endpos - index}d" + f.suffix
    return f.parent / filename, str(f.name)[index:endpos]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create timelapse video using ffmpeg")
    parser.add_argument("-i", dest="input", metavar="input", type=Path, required=True, help="input folder")
    parser.add_argument("-f", dest="fps", metavar="fps", type=str, default="30", help="frames per second (default: 30)")
    parser.add_argument(
        "-s",
        dest="scale",
        metavar="scale",
        type=str,
        default="1920:1080",
        help="output video size (default: 1920:1080)",
    )
    parser.add_argument(
        "-o",
        dest="output",
        metavar="output",
        type=str,
        default="render.mp4",
        help="output video file (default: render.mp4",
    )

    args = parser.parse_args()

    fmt, start = get_info(Path(args.input))
    ffmpeg_cmd = f"ffmpeg -r {args.fps} -start_number {start} -i {fmt} -c:v libx264 -vf fps={args.fps},scale={args.scale} {args.output}"
    print(ffmpeg_cmd)
