from PIL import Image, UnidentifiedImageError
import subprocess as sp
import numpy as np
import argparse


class ffmpeg:
    def __init__(self, fps, size, output):
        self.cmd_out = [
            "ffmpeg",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-video_size",
            f"{size[1]}x{size[0]}",
            "-r",
            str(fps),
            "-i",
            "-",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-profile:v",
            "high",
            "-crf",
            "18",
            "-coder",
            "1",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            "scale=iw:-2",
            "-movflags",
            "+faststart",
            "-g",
            "30",
            "-bf",
            "2",
            "-y",
            str(output),
        ]
        self.pipe = sp.Popen(self.cmd_out, stdin=sp.PIPE, bufsize=3 * size[0] * size[1])

    def push(self, frame):
        self.pipe.stdin.write(frame)

    def __del__(self):
        self.pipe.stdin.close()
        self.pipe.wait()

        if self.pipe.returncode != 0:
            raise sp.CalledProcessError(self.pipe.returncode, self.cmd_out)


def load_image(file, scale):
    try:
        image = Image.open(file)
        if scale > 1:
            new_size = (round(image.size[0] / scale), round(image.size[1] / scale))
            image = image.resize(new_size, Image.LANCZOS)
        result = np.array(image.convert("RGB"), dtype=np.float)
        size = result.shape
        return result.reshape((size[1] * size[0] * size[2],)), size
    except UnidentifiedImageError:
        print(f"[error]: cannot open {file} file")
        exit()


def alpha_range(start, stop, step):
    v_up = np.arange(start, stop + step, step)
    v_down = np.arange(stop, start - step, -step)
    return list(v_up) + list(v_down)


def blend(i1, i2, alpha):
    out = np.zeros_like(i1)
    out[:] = i1[:] * alpha + i2[:] * (1.0 - alpha)
    return out.astype(np.uint8).tobytes()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="make simple 2.5D video")
    parser.add_argument("-i", dest="input", metavar="image", type=str, nargs=2, required=True, help="input images")
    parser.add_argument(
        "-f", dest="frame", metavar="frame", type=int, default=30, help="frames per second (default: 30)"
    )
    parser.add_argument(
        "-t", dest="transition", metavar="seconds", type=int, default=3, help="transition time (default: 3)"
    )
    parser.add_argument("-s", dest="scale", metavar="scale", type=float, default=1, help="scale factor (default: 1)")
    parser.add_argument(
        "-o",
        dest="output",
        metavar="output",
        type=str,
        default="render.mp4",
        help="output video file (default: render.mp4",
    )

    args = parser.parse_args()

    if args.scale < 1:
        print(f"[error]: scale factor cannot be less than 1")
        exit()

    i1, size = load_image(args.input[0], args.scale)
    i2, _ = load_image(args.input[1], args.scale)

    render = ffmpeg(fps=args.frame, size=size, output=args.output)
    step = 2.0 / (args.frame * args.transition)
    for alpha in alpha_range(0, 1, step):
        render.push(blend(i1, i2, alpha))
