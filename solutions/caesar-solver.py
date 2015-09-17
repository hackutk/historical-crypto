def caesar(msg, n):
    """Performs a caesar cipher encryption"""
    lets = 'abcdefghijklmnopqrstuvwxyz'
    r = ''
    for c in msg:
        if c.lower() not in lets:
            r += c
        else:
            if c in lets:
                r += chr(((ord(c) - ord('a') + n) % 26) + ord('a'))
            else:
                r += chr(((ord(c) - ord('A') + n) % 26) + ord('A'))
    return r


msg = raw_input("ciphertext: ")

# just print every possibility, and use your eyes to spot which one looks correct
for n in range(1, 26):
    print("%2d: %s" % (n, caesar(msg, n)))
