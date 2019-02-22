import pycom
import time

t = 100

def encode_binary(val):
    return bin(val)[2:]

def blink_val(val):
    binary = encode_binary(val)
    for el in binary:
        if int(el) == 1:
            pycom.rgbled(0xff0000) # red
            time.sleep_ms(t)
        if int(el) == 0:
            pycom.heartbeat(False)
            time.sleep_ms(t)

def blink_str(s):
    print(s)
    for el in s:
        if int(el) == 1:
            pycom.rgbled(0xff0000) # red
            time.sleep_ms(t)
        if int(el) == 0:
            pycom.heartbeat(False)
            time.sleep_ms(t)


pycom.heartbeat(False)
while True:
    """t = 100
    pycom.rgbled(0xff0000) # red
    time.sleep_ms(t)
    pycom.heartbeat(False)
    time.sleep_ms(t)"""
    blink_str("1100")
    #blink_val(2)
    #print(encode_binary(2))
