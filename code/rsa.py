import math
import random


def rsa_keygen():
    primes = [x for x in range(100, 500) if is_prime(x)]

    p, q = random.sample(primes, 2)

    n = p * q

    # In theory we calculate "Carmichaels totient function", lambda(n) but since
    # p and q are always prime, we can "cheat" and lamda(n) is always equal to lcm(p - 1, q - 1)
    # Also its important to pick a large enough p and q so that there exists at least one e

    c = lcm(p - 1, q - 1)

    # choose an e such that 1 < e < c, and e and c are co prime
    # it will be public and used for encryption
    # it is not allowed to have e = d, since d is supposed to be private
    while True:
        e = random.randint(1, c - 1)

        if math.gcd(c, e) == 1 and e != pow(e, -1, c):
            break

    # calculate a d such that it is the modular inverse of e, d = e^-1 mod c
    # it will be the private key exponent
    d = pow(e, -1, c)

    # A modular inverse d of e has the key property that x^ed = x^1 = x

    print("public key = (n,e): (" + str(n) + ", " + str(e) + ")")
    print("private key = d:", d)

    return [(n, e), d]


def rsa_encrypt(m, n, e):
    # can be done using only the public key pair (n,e)
    c = m ** e % n
    return c


def rsa_decrypt(c, n, d):
    # can only be done with the private key d
    # c = m^e and since d is mod.inv. c^d = (m^e)^d = m
    m = c ** d % n
    return m


def is_prime(n):
    # pretty bad, could be improved with 6k +-1 optimization
    # or importing probably
    if n == 0:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def rsa_encrypt_string(m, pub):
    m_unicode = [ord(c) for c in m]
    c = []
    for i in m_unicode:
        c.append(rsa_encrypt(i, pub[0], pub[1]))
    return c


def rsa_decrypt_string(c, priv, pub):
    m_unicode = []
    for i in c:
        m_unicode.append(rsa_decrypt(i, pub[0], priv))

    m = ''.join([chr(x) for x in m_unicode])

    return m


# Alice and Bob wants to use RSA to communicate securely
# so they start by generating their private and public keys
print("==- RSA -==")
print("---Alice's keys---")
a_public, a_private = rsa_keygen()
print("----Bobs keys-----")
b_public, b_private = rsa_keygen()
print("------------------")

# Alice can send Bob a message by using his public key for encryption
m = "Hello Bob! from Alice"

# She encrypts every character and sends bob an array of encrypted characters
# in reality you use some known padding scheme, not an array of characters
m_encrypted = rsa_encrypt_string(m, b_public)

print("Alice's encrypted the message: \"" + str(m) + "\"")
print("She encrypted it to: ", m_encrypted)

# Bob receives m_ascii_enc and only he can decrypt since d is private
# He decrypts every element of the array and joins the array to get m

m_decrypted = rsa_decrypt_string(m_encrypted, b_private, b_public)

print("Bob decrypted it to: \"" + m_decrypted + "\"")
if m == m_decrypted:
    print("The message was recovered successfully")
else:
    print("The message was not recovered")

# problems cases:
# ---Alice's keys---
# public key = (n,e): (5963, 25)
# private key = d: 169
# ----Bobs keys-----
# public key = (n,e): (9409, 61)
# private key = d: 85
# ------------------
# Alice's encrypted the message: Hello Bob! from Alice
# She encrypted it to:  [1293, 4070, 7130, 7130, 8610, 25, 7472, 8610,
# 5918, 3847, 25, 7440, 5120, 8610, 4629, 25, 7832, 7130, 6517, 5961, 4070]
# Bob decrypted it to: ুୢᨰᨰᤐыȧᤐႭළыʬᱼᤐ᳘ыౡᨰÊ↻ୢ

# other issues are that it will sometimes slow down, probably due to some bad pick of n or e
