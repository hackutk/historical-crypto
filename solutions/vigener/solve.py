# rxorbreak.py
#
# By Joseph Connor
#
# This script reads a hex-encoded repeating-XOR ciphertext on stdin
# and attempts to find the plaintext with basic frequency analysis

from __future__ import division
from string import ascii_uppercase

import sys
import freqs


def enchunk(l, n):
    """Break list into chunks of size n"""
    chunks = []
    for i in xrange(0, len(l), n):
        chunks.append(l[i:i+n])
    return chunks

def rot(msg, n):
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


def vigenere_dec(msg, key):
    k = [ord(c)-ord('A') for c in key.upper()]
    while len(k) < len(msg):
        k += k
    ct = ''
    for c, ki in zip(msg, k):
        ct += rot(c, -ki)
    return ct
    


def try_keylen(keylen, ciphertext):
    """Try and find the most likely key for a given key length"""
    chunks = enchunk(ciphertext, keylen)[:-1]
    key = ''
    # Transpose chunks to get sets of bytes xored with same key byte
    nth_chars = zip(*chunks)

    # Find the most likely key byte for each set
    for nth_char in nth_chars:
        best_k = None
        max_score = 0 

        for k in range(26):
            plaintext = rot(nth_char, -k)
            score = freqs.score_freq(freqs.get_freqs(plaintext))

            if best_k is None or score > max_score:
                best_k = k
                max_score = score

        key += chr(ord('A') + best_k)

    return key 

with open('cipher.txt') as f:
    ciphertext = ''.join(c for c in f.read().upper() if c in ascii_uppercase)

for keylen in range(2, len(ciphertext) // 10):
    k = try_keylen(keylen, ciphertext)
    pt = vigenere_dec(ciphertext, k)
    score = freqs.score_freq(freqs.get_freqs(pt))

    print "Score: %8f      Key length: %3d     Likely key: %s" % (score, len(k), k)
    print "Plaintext: %s" % pt
    print ""
