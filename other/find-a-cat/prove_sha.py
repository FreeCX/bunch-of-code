alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def as_text(value):
    result = ''
    for index in range(0, len(value), 2):
        block = int(value[index:index + 2], 16)
        symbol = chr(block)
        result += symbol if symbol in alphabet else '-'
    return result

print(as_text(input('Input hash: ')))
