from audio_experiment import generate_sample, SAMPLE_RATE
from collections import defaultdict
from time import sleep
import pyaudio as pa
import numpy as np

P1 = 16

music_list = [
    ("c5", 8),
    ("h4", 8),
    ("P", P1),
    ("h4", 8),
    ("a4", 16),
    ("g4", 16),
    ("P", P1),
    ("h4", 8),
    ("a4", 8),
    ("P", P1),
    ("a4", 8),
    ("P", P1),
    ("a4", 8),
    ("g4", 8),
    ("f4", 8),
    ("e4", 8),
    ("P", P1),
    ("g4", 8),
    ("f4", 8),
    ("P", P1),
    ("e4", 8),
    ("e4", 8),
    ("g4", 8),
    ("f4", 8),
    ("P", P1),
    ("e4", 8),
    ("d4", 8),
    ("c4", 8),
    ("h3", 8),
    ("P", P1),
    ("a5", 8),
    ("c6", 8),
    ("e5", 8),
    ("h5", 8),
    ("P", P1),
    ("h5", 8),
    ("a5", 16),
    ("g5", 16),
    ("P", P1),
    ("h5", 8),
    ("c5", 8),
    ("e5", 8),
    ("a5", 8),
    ("P", P1),
    ("a5", 8),
    ("P", P1),
    ("a5", 8),
    ("a4", 8),
    ("c5", 8),
    ("e5", 8),
    ("g4", 8),
    ("g5", 8),
    ("f4", 8),
    ("f5", 8),
    ("e4", 8),
    ("e5", 8),
    ("P", P1),
    ("g5", 8),
    ("d5", 8),
    ("a4", 8),
    ("f5", 8),
    ("P", P1),
    ("e5", 8),
    ("c5", 8),
    ("e5", 8),
    ("g5", 8),
    ("d5", 8),
    ("f5", 8),
    ("P", P1),
    ("e4", 8),
    ("g4", 8),
    ("h4", 8),
    ("e5", 8),
    ("d5", 8),
    ("c5", 8),
    ("h4", 8),
]


class Music:
    def __init__(self, stream, duration):
        self.stream = stream
        self.notes = Music.generate_notes(duration)
        self.duration = duration

    def generate_notes(duration):
        notes = {
            "C0": 16.352,
            "D0": 18.354,
            "E0": 20.602,
            "F0": 21.827,
            "G0": 24.500,
            "A0": 27.500,
            "H0": 30.868,
            "C1": 32.703,
            "D1": 36.708,
            "E1": 41.203,
            "F1": 43.654,
            "G1": 48.999,
            "A1": 55.000,
            "H1": 61.735,
            "C2": 65.406,
            "D2": 73.416,
            "E2": 82.407,
            "F2": 87.307,
            "G2": 97.999,
            "A2": 110.00,
            "H2": 123.47,
            "C3": 130.81,
            "D3": 146.83,
            "E3": 164.81,
            "F3": 174.61,
            "G3": 196.00,
            "A3": 220.00,
            "H3": 246.94,
            "C4": 261.63,
            "D4": 293.66,
            "E4": 329.63,
            "F4": 349.23,
            "G4": 392.00,
            "A4": 440.00,
            "H4": 493.88,
            "C5": 523.25,
            "D5": 587.33,
            "E5": 659.26,
            "F5": 698.46,
            "G5": 783.99,
            "A5": 880.00,
            "H5": 987.77,
            "C6": 1046.5,
            "D6": 1174.7,
            "E6": 1318.5,
            "F6": 1396.9,
            "G6": 1568.0,
            "A6": 1760.0,
            "H6": 1975.5,
            "C7": 2093.0,
            "D7": 2349.3,
            "E7": 2637.0,
            "F7": 2793.8,
            "G7": 3136.0,
            "A7": 3520.0,
            "H7": 3951.1,
            "C8": 4186.0,
            "D8": 4698.6,
            "E8": 5274.0,
            "F8": 5587.7,
            "G8": 6271.9,
            "A8": 7040.0,
            "H8": 7902.1,
        }
        result = defaultdict(np.array)
        for (note, freq) in notes.items():
            result[note] = np.array(generate_sample(freq, duration, 1.0), dtype=np.int16)
        return result

    # duration -- обратная длина ноты (1/8 -- 8, 1/16 -- 16)
    def play_note(self, note, duration):
        if note.upper() == "P":
            sleep(1 / duration)
        else:
            note = self.notes.get(note.upper())
            if note is not None:
                len_d = len(note) / duration
                self.stream.write(note[:len_d])


if __name__ == "__main__":
    p = pa.PyAudio()
    stream = p.open(format=p.get_format_from_width(width=2), channels=2, rate=SAMPLE_RATE, output=True)
    music = Music(stream, 8)
    for conf in music_list:
        music.play_note(*conf)
    sleep(1)
    stream.stop_stream()
    stream.close()
    p.terminate()
