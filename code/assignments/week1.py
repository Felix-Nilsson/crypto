from collections import deque


def pos_to_char(pos):
    return "abcdefghijklmnopqrstuvwxyz"[pos]


def char_to_pos(char):
    for i in range(0, 25):
        if char == "abcdefghijklmnopqrstuvwxyz"[i]:
            return i


def xor(a, b):
    if a != b:
        return "1"
    return "0"


def sub_cipher(k, m):
    c = ""
    for char in m:
        pos = char_to_pos(char)
        c += k[pos]
    return c


def vigenere(k, m):
    long_k = ""
    while len(long_k) < len(m):
        long_k += k
    if len(long_k) > len(m):
        diff = len(long_k) - len(m)
        long_k = long_k[:-diff]

    c = ""
    print(long_k, m)
    for i in range(len(m)):
        c += pos_to_char((char_to_pos(m[i]) + char_to_pos(long_k[i])) % 26)
    return c


def LFSR(rounds, state):
    q = deque()

    for bit in state:
        q.appendleft(bit)

    c = ""
    for i in range(rounds):
        new_bit = xor(xor(q[11], q[8]), q[4])
        print(new_bit, q)
        q.appendleft(new_bit)
        c += q.pop()

    return c


# Problem 1
# print(sub_cipher("jnwfzcyksdoulavmbxhqertgpi","cryptography"))
# >>> wxpmqvyxjmkp

# Problem 2
# print(vigenere("secret", "cryptography"))
# >>> uvagxhyvcglr

# Problem 9

# a)
# print("010111100010")
print(LFSR(15, "010111100010"))
# >>> 010111100010101

# b)
# print(LFSR(15,"000000000000"))
# >>> 000000000000000
