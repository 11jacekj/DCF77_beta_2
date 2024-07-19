def decode_bits(bits, start, end):
    return int(''.join(map(str, bits[start:end])), 2)

def decode_time(bits):
    minutes = decode_bits(bits, 21, 25) + decode_bits(bits, 25, 28) * 10
    hours = decode_bits(bits, 29, 33) + decode_bits(bits, 33, 35) * 10
    return hours, minutes

def decode_date(bits):
    day = decode_bits(bits, 36, 40) + decode_bits(bits, 40, 42) * 10
    month = decode_bits(bits, 45, 49) + decode_bits(bits, 49, 50) * 10
    year = 2000 + decode_bits(bits, 50, 54) + decode_bits(bits, 54, 58) * 10
    return day, month, year