def read_int_64(buf, offset):
    
    value = buf[offset + 7] & 0x7F
    
    for i in range(6, -1, -1):
        value *= 256
        value += buf[offset + i]
        
    if buf[offset + 7] & 0x80 != 0:
        value *= -1
    
    return value
