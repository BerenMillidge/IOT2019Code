def split(iterable, n):
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]

def encodeNum(var: int):
    bits = []
    while var:
        var, b = divmod(var, 2)
        bits.append(bool(b))
    return bits

def decodeNum(bits: list):
    return sum(b * 2**x for x, b in enumerate(bits))


def encodeBytes(var: bytes):
    stream = []
    for byte in var:
        bits = encodeNum(byte)
        padding = 8 - len(bits)
        stream += bits + [False] * padding
    return stream

def decodeBytes(bits: list):
    return bytes(map(decodeNum, split(bits, 8)))


def encodeString(var: str):
    return encodeBytes(var.encode())

def decodeString(bits: list):
    return decodeBytes(bits).decode()

if __name__ == '__main__':
    num = 2345789
    assert decodeNum(encodeNum(num)) == num

    stream = 'Yeeeert'.encode()
    assert decodeBytes(encodeBytes(stream)) == stream

    text = "Here's to six million cows."
    assert decodeString(encodeString(text)) == text
