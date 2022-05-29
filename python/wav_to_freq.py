# https://habr.com/ru/post/438448/
import struct as st
import numpy as np
import argparse

one_2pi = 1.0 / (2.0 * 3.141592653589793)


def sine(freq, sample_rate, t=1.0, volume=1.0):
    return np.round((128.0 * np.sin(one_2pi * freq * sample_rate * t) + 127.0) * volume)


def write_wav(output, sample_rate, data):
    bit_per_sample = 8
    byte_per_sample = 1
    num_channels = 1
    wav_size = st.pack("<I", data.shape[0] + 44 - 8)
    fmt_chunk_size = st.pack("<I", 16)
    audio_format = st.pack("<H", 1)
    byte_rate = st.pack("<I", sample_rate * num_channels * byte_per_sample)
    sample_aligment = st.pack("<H", num_channels * byte_per_sample)
    num_channels = st.pack("<H", num_channels)
    sample_rate = st.pack("<I", sample_rate)
    bit_depth = st.pack("<H", bit_per_sample)
    header = (
        b"RIFF"
        + wav_size
        + b"WAVEfmt "
        + fmt_chunk_size
        + audio_format
        + num_channels
        + sample_rate
        + byte_rate
        + sample_aligment
        + bit_depth
        + b"data"
    )
    with open(output, "wb") as f:
        f.write(header)
        f.write(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wav to freq converter")
    parser.add_argument("-i", "--input", help="input wav file", default=None)
    parser.add_argument("-o", "--output", help="output freq file", default=None)
    parser.add_argument("-d", "--chunk", type=int, help="split data by chunks", default=100)
    parser.add_argument("-c", "--count", type=int, help="output count of freqs", default=3)
    parser.add_argument("-l", "--lower", type=int, help="lower freq", default=1000)
    parser.add_argument("-n", "--numb", type=int, help="lower border of freq", default=300)
    parser.add_argument("-s", "--sample_rate", type=int, help="input file sample rate", default=44100)
    parser.set_defaults(handler=lambda args: parser.print_help())
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        exit()

    data = np.fromfile(args.input, np.uint8)[44:]
    step = args.sample_rate // args.chunk
    freq_data = []
    for start in range(0, data.shape[0], step):
        signal = data[start : start + step]
        N = signal.shape[0]
        secs = N / float(args.sample_rate)
        Ts = 1.0 / args.sample_rate
        t = np.arange(0, secs, Ts)
        FFT = np.abs(np.fft.fft(signal))
        FFT_side = FFT[np.arange(N // 2)]
        freqs = np.fft.fftfreq(signal.size, Ts)
        freqs_side = freqs[np.arange(N // 2)].astype(np.int)
        abs_FFT_side = np.abs(FFT_side[freqs_side > args.lower])
        freqs_side = freqs_side[freqs_side > args.lower]

        freq_block = []
        for _ in range(args.count):
            index = abs_FFT_side.argmax()
            if abs_FFT_side[index] > args.numb:
                freq_block.append(int(freqs_side[index]))
            else:
                freq_block.append(0)
            abs_FFT_side = np.delete(abs_FFT_side, index)
            freqs_side = np.delete(freqs_side, index)
        freq_data.append((step, freq_block))

    if args.output:
        music = []
        f = open(f"{args.output}.freq", "w")
        f.write("# dt freq_1 freq_2 ... freq_N\n")
        for step, freqs in freq_data:
            freq_join = " ".join(map(str, freqs))
            f.write(f"{step} {freq_join}\n")
            for freq in freqs:
                duration = int(step // len(freqs))
                signal = sine(freq, args.sample_rate, t=np.arange(duration))
                music.extend(signal)
        f.close()
        music = np.array(music, dtype=np.uint8)
        write_wav(f"{args.output}.wav", args.sample_rate, music)
