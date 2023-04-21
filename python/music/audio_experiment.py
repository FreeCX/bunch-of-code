#!/bin/env python3
import functions as fs
import numpy as np
import pyaudio as pa
import pygame

SAMPLE_RATE = 44100
#                      0       1       2      3        4       5       6
#                      до      ре      ми     фа       соль    ля      си
freq_array = np.array([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88])
key_names = ["a", "s", "d", "f", "g", "h", "j"]
key_list = list(map(lambda x: ord(x), key_names))
key_dict = dict([(key, False) for key in key_list])


gen_func = np.sin
gen_func_list = (
    (np.sin, ord("w")),
    (fs.square, ord("e")),
    (fs.saw, ord("r")),
    (fs.triangle, ord("t")),
    (fs.noise, ord("y")),
    (fs.exp_func_01, ord("u")),
    (fs.exp_func_02, ord("i")),
)


def generate_sample(freq, duration, volume):
    amplitude = np.round((2**16) * volume)
    total_samples = np.round(SAMPLE_RATE * duration)
    w = 2.0 * np.pi * freq / SAMPLE_RATE
    k = np.arange(0, total_samples)
    return np.round(amplitude * gen_func(k * w))


def generate_tones(duration):
    tones = []
    for freq in freq_array:
        tone = np.array(generate_sample(freq, duration, 1.0), dtype=np.int16)
        tones.append(tone)
    return tones


if __name__ == "__main__":
    duration_tone = 1 / 64.0
    tones = generate_tones(duration_tone)
    p = pa.PyAudio()
    stream = p.open(format=p.get_format_from_width(width=2), channels=2, rate=SAMPLE_RATE, output=True)
    window_size = 320, 240
    screen = pygame.display.set_mode(window_size)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord("q"):
                    running = False
                if event.key == ord("-"):
                    duration_tone /= 2
                    print("duration_tone =", duration_tone)
                    tones = generate_tones(duration_tone)
                if event.key == ord("="):
                    duration_tone *= 2
                    print("duration_tone =", duration_tone)
                    tones = generate_tones(duration_tone)
                if event.key == ord("1"):
                    freq_array /= 2
                    print("freq_array =", freq_array)
                    tones = generate_tones(duration_tone)
                if event.key == ord("2"):
                    freq_array *= 2
                    print("freq_array =", freq_array)
                    tones = generate_tones(duration_tone)
                for function, key in gen_func_list:
                    if key == event.key:
                        print("gen_function =", function.__name__)
                        gen_func = function
                        tones = generate_tones(duration_tone)
                for index, key in enumerate(key_list):
                    if event.key == key:
                        key_dict[key] = True
            if event.type == pygame.KEYUP:
                for index, key in enumerate(key_list):
                    if event.key == key:
                        key_dict[key] = False
        for index, key in enumerate(key_list):
            if key_dict[key] is True:
                stream.write(tones[index])
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()


# underrun error
# ...
# data = s.recv(CHUNK * WIDTH) # Receive data from peer
# stream.write(data) # Play sound
# free = stream.get_write_available() # How much space is left in the buffer?
# if free > CHUNK # Is there a lot of space in the buffer?
#     tofill = free - CHUNK
#     stream.write(SILENCE * tofill) # Fill it with silence
# #...
