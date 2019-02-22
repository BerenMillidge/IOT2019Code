import bitstream as bit

def encodeTemps(temps) -> bytes:
    # encodes (celcius) readings as bytes
    # stores a single byte to nearest 0.25 degree
    # -10 -> 54 °c
    return bytes([ int((t+10)*4) for t in temps ])

def decodeTemps(temps) -> list:
    return [t/4 - 10 for t in list(temps)]

class CowMessage:
    def __init__(self, cowID: bytes, dayNum: int, temp: list):
        self.cowID = cowID
        self.dayNum = dayNum
        self.temp = temp

    @property
    def message(self):
        msg = b'Moo'
        msg += self.cowID
        msg += bytes([self.dayNum % 256])
        msg += encodeTemps(self.temp)
        msg += bytes([0]*4)
        return msg

    def transmit(self):
        msg = self.message
        for bit in msg:
            print(bit)

    @classmethod
    def fromMessage(cls, msg):
        m, o, o, a, b, c, d, day, *tmp, _, _, _, _ = msg
        assert m+o+o == b'Moo'
        cowID = a+b+c+d
        day = list(day)[0]
        temps = decodeTemps(tmp)
        return cls(cowID, day, temp)
