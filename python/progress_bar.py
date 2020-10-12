def progress_bar(index, max_value=100):
    from math import ceil
    # 8/8 7/8 6/8 5/8 4/8 3/8 2/8 1/8
    progress_bar = '█▉▊▋▌▍▎▏'
    pb_size = len(progress_bar)
    if index < 0 or index > max_value:
        raise IndexError(f'index ({index}) out of range [0, {max_value}]')
    k = ceil(max_value / pb_size) * pb_size / max_value
    new_index = int(round(index * k))
    full_block_count = new_index // pb_size
    part_block = new_index % pb_size
    if part_block == 0:
        result = progress_bar[0] * full_block_count
    else:
        result = progress_bar[0] * full_block_count + progress_bar[pb_size - part_block]
    space_filler = ' ' * (int(ceil(max_value / pb_size)) - len(result))
    return '|' + result + space_filler + '|'


if __name__ == '__main__':
    from time import sleep

    for i in range(100 + 1):
        print('progress bar', progress_bar(i, max_value=100), end='\r')
        sleep(0.1)
