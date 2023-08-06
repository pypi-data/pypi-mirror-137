import struct


def string_to_raw(s):
    return bytes(s, 'utf8')


def float_to_raw(f):
    return struct.pack('<d', f)


def int_to_raw(i):
    if i == 0:
        return None

    remainder = i
    bts = bytearray()
    if remainder > 0:
        bts.append(0)
    else:
        bts.append(255)
        remainder = -remainder

    while remainder > 0:
        bts.append(remainder % 256)
        remainder //= 256

    return bytes(bts)


def bool_to_raw(b):
    bts = bytearray()
    if b:
        bts.append(255)
    return bytes(bts)
