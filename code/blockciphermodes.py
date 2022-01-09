from collections import deque


# https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
# Example of different modes of encryption
# Relies on a reversible encryption function E(k,m) and its decryption function D(k,c)
# Could be any complicated encryption algorithm but for simplicity we choose a caesar cipher

def E(k, m):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    d = deque(letters)
    # -k to rotate +k to the right
    d.rotate(-k)
    letters = list(d)

    s = []
    for c in m:
        pos = char_to_pos(c)
        s.append(letters[pos])

    return "".join(s)


def D(k, m):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = []
    for c in m:
        pos = char_to_pos(c)
        s.append(letters[pos - k])

    return "".join(s)


def pos_to_char(pos):
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[pos]


def char_to_pos(char):
    for i in range(0, 52):
        if char == "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]:
            return i


# ECB, electronic code book mode, is most basic
# M = m1m2...mn and result is C = c1c2...cn
# ci = E(k,mi)
# Considered bad since it has no diffusion, any pattern in m will be a pattern in c
def ECB_encryption(k, m):
    res = []
    for c in m:
        c_i = E(k, c)
        res.append(c_i)

    return "".join(res)


def ECB_decryption(k, c):
    res = []
    for i in c:
        m_i = D(k, i)
        res.append(m_i)
    return "".join(res)


# CBC, cipher block chaining, is an improvement over ECB
# M = m1m2...mn and result is C = c0c1c2...cn
# ci = E(k, mi xor ci-1), c0 = IV
# result will be n+1 in total as its IVc1c2
def CBC_encryption(k, m):
    c0 = 'a'  # IV
    C = [c0]
    M = ['X'] + [c for c in m]

    for i in range(1, len(M)):
        mi = char_to_pos(M[i])
        c_prev = char_to_pos(C[i - 1])


        x = pos_to_char((mi ^ c_prev))

        c_i = E(k, x)
        C.append(c_i)

    C[0] = str(c0)
    return "".join(C)


# Decryption is done via solving encryption for mi
# mi = D(k,ci) xor ci-1
def CBC_decryption(k, c):
    c0 = 'a'  # IV
    C = [c for c in c]

    M = []
    for i in range(1, len(c)):
        c_prev = char_to_pos(C[i - 1])
        decrypted = D(k, C[i])
        mi = char_to_pos(decrypted) ^ c_prev
        M.append(pos_to_char(mi))
    return "".join(M)


# CTR, counter mode generates a new key ki for every cipher ci
# ki = E(k, IV + i), IV appended to i IV || i in reality, but simpler to code IV + i
# ci = mi xor ki
# returns IVc1c2..cn
def CTR_encryption(k, m):
    IV = 'a'

    c = [IV]
    for i in range(len(m)):
        x = char_to_pos(IV) + i
        ki = E(k, pos_to_char(x))
        ci = char_to_pos(ki) ^ char_to_pos(m[i])
        c.append(pos_to_char(ci))

    return "".join(c)


# we again solve for m, mi = ci xor ki
def CTR_decryption(k, c):
    IV = c[0]
    K = [E(k, pos_to_char(char_to_pos(IV) + i)) for i in range(len(c))]

    c = list(c)
    del c[0]

    m = []
    for i in range(len(c)):
        ki = char_to_pos(K[i])
        ci = char_to_pos(c[i])
        m.append(pos_to_char(ki ^ ci))

    return "".join(m)


m = "helloworld"  # m can only contain lowercase letters here
k = 3
print("==- Block Cipher Modes -==")
print("(e,d) = (encrypted, decrypted)")
print("m:", m)
print("--------------------------")
ecb = ECB_decryption(k, m), ECB_decryption(k, ECB_encryption(k, m))
cbc = CBC_encryption(k, m), CBC_decryption(k, CBC_encryption(k, m))
ctr = CTR_encryption(k, m), CTR_decryption(k, CTR_encryption(k, m))

print("ECB (e,d):", ecb[0], ecb[1])
print("success") if ecb[1] == m else print("failure")
print("CBC (e,d):", cbc[0], cbc[1], cbc[1] == m)
print("success") if cbc[1] == m else print("failure")
print("CTR (e,d):", ctr[0], ctr[1], ctr[1] == m)
print("success") if ctr[1] == m else print("failure")
