def text_to_code(text, separator="-", blocks=4, block_size=4, round_count=32):
    iter_by = lambda iterator, count: [iterator[index : index + count] for index in range(0, len(iterator), count)]
    squash = lambda x: (x & 0xFF) ^ ((x >> 8) & 0xFF) ^ ((x >> 16) & 0xFF) ^ ((x >> 24) & 0xFF)
    base = [0xC9, 0x4F, 0x69, 0x72, 0x11, 0xFE, 0xA0, 0x42, 0x93, 0x21, 0x57, 0x37, 0x77, 0x23, 0xCC, 0x7D]
    alphabet = "Y31NTSCVBGAXHLUEWR2PQKMJ8O67ID90F45Z"
    magic_number = len(alphabet)
    text_len = len(text)
    if text_len < magic_number:
        text += alphabet[: magic_number - text_len]
    cycle_index = 0
    s_blocks = [0 for _ in range(block_size * blocks)]
    for index, c in enumerate(map(ord, text)):
        for _ in range(round_count):
            for jndex, b in enumerate(base):
                c ^= b * (index + 1) * (jndex + 1)
            c <<= 1
            s_blocks[cycle_index] += c
            s_blocks[cycle_index] &= 0xFFFFFFFF
            cycle_index += 1
            cycle_index %= blocks * block_size
    result = []
    for block in iter_by(s_blocks, block_size):
        result.append("".join(map(lambda x: alphabet[squash(x) % len(alphabet)], block)))
    return separator.join(result)


if __name__ == "__main__":
    print(text_to_code("deadbeef", blocks=4, block_size=8))
