#!/bin/env python3
# from sys import stdout
import pyaudio as pa
import numpy as np

SAMPLE_RATE = 44100
FREQ = 330.0
DOT_LENGTH = 0.25
DASH_LENGTH = 3 * DOT_LENGTH
PAUSE_LENGTH = DOT_LENGTH
LONG_PAUSE_LENGTH = 3 * DOT_LENGTH
WORD_PAUSE_LENGTH = 7 * DOT_LENGTH

MORSE_DICT = {
    "а": ".-",
    "б": "-...",
    "в": ".--",
    "г": "--.",
    "д": "-..",
    "ё": ".",
    "е": ".",
    "ж": "...-",
    "з": "--..",
    "и": "..",
    "й": ".---",
    "к": "-.-",
    "л": ".-..",
    "м": "--",
    "н": "-.",
    "о": "---",
    "п": ".--.",
    "р": ".-.",
    "с": "...",
    "т": "-",
    "у": "..-",
    "ф": "..-.",
    "х": "....",
    "ц": "-.-.",
    "ч": "---.",
    "ш": "----",
    "щ": "--.-",
    "ъ": "--.--",
    "ы": "-.--",
    "ь": "-..-",
    "э": "..-..",
    "ю": "..--",
    "я": ".-.-",
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": "......",
    ",": ".-.-.-",
    ":": "---...",
    ";": "-.-.-.",
    ")": "-.--.-",
    "(": "-.--.-",
    "'": ".----.",
    "-": "-....-",
    "\\": "-..-.",
    "/": "-..-.",
    "!": "..--..",
    "?": "--..--",
    " ": " ",
    "@": ".--.-.",
}


def generate_sample(freq, duration, volume):
    amplitude = np.round((2**16) * volume)
    total_samples = np.round(SAMPLE_RATE * duration)
    w = 2.0 * np.pi * freq / SAMPLE_RATE
    k = np.arange(0, total_samples)
    return np.array(np.round(amplitude * np.sin(k * w)), dtype=np.uint16)


dot_signal = generate_sample(FREQ, DOT_LENGTH, 1.0)
dash_signal = generate_sample(FREQ, DASH_LENGTH, 1.0)
pause_signal = np.zeros(SAMPLE_RATE * PAUSE_LENGTH, dtype=np.uint16)
long_pause_signal = np.zeros(SAMPLE_RATE * LONG_PAUSE_LENGTH, dtype=np.uint16)
word_pause_signal = np.zeros(SAMPLE_RATE * WORD_PAUSE_LENGTH, dtype=np.uint16)


def morse(text, stream):
    result = " ".join(map(lambda x: MORSE_DICT[x], text.lower()))
    print("Morse code is", result)
    # print('Morse code is `', end='')
    # stdout.flush()
    last_char = result[0]
    for character in result:
        # print(character, end='')
        # stdout.flush()
        if character == ".":
            stream.write(dot_signal)
        elif character == "-":
            stream.write(dash_signal)
        elif character == " ":
            last_char = character
            stream.write(word_pause_signal)
            continue
        if last_char == character:
            stream.write(pause_signal)
        else:
            stream.write(long_pause_signal)
        last_char = character
    # print('`')


if __name__ == "__main__":
    p = pa.PyAudio()
    stream = p.open(format=p.get_format_from_width(width=2), channels=2, rate=SAMPLE_RATE, output=True)
    while True:
        line = input("Input text > ").strip()
        if len(line) == 0:
            break
        morse(line, stream)
    stream.stop_stream()
    stream.close()
    p.terminate()
