import pycom
import time

def split(iterable, n):
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]

def encode_str(string):
    bits = []
    stream = list(string.encode())
    for b in stream:
        b = [bool((b & (2**x)) << x) for x in range(8)]
        bits += b

    return bits

def decode_str(bits):
    stream = []
    for b in split(bits, 8):
        num = sum([b[x] * (2**x) for x in range(8)])
        stream.append(num)
    return bytes(stream).decode()

def encode_int(val):
   return [bool(int(q)) for q in bin(val)[2:]]

def transmit(code, freq=240):
    dt = 1000 // freq
    last_bit = 0
    for bit in code:
        col = 0xff0000*last_bit + 0x00ff00*bit
        last_bit = bit
        pycom.rgbled(col)
        time.sleep_ms(dt)

def transmit_loop(code, freq):
    try:
        while True:
            transmit(code, freq)
            print('Sent')
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    pycom.heartbeat(False)
    # string as a proxy for cow-related bytes
    HEADER = "Moo"
    ID = "1$5$"
    # two-byte temperature
    TEMP_DATA = "tm" * 24
    FOOTER = "\0\0\0\0"
    MSG = HEADER + ID + TEMP_DATA + FOOTER
    transmit_loop(
        encode_str(MSG),
        freq=60
    )
