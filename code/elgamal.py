import random
import math


def elgamal_keygen():
    # We pick a random prime p (256<p<1000 for practical purposes and to work with unicode)
    primes = [x for x in range(257, 1000) if is_prime(x)]
    p = random.choice(primes)

    # We find an Abelian group Zp star = {1,2,...,p-1}
    zp = [x for x in range(1, p)]

    # We find a generator g for Zp star
    # such that {g^i | i = 0..p-2} = Zp star

    g = []
    for gen in zp:
        l = []
        for i in range(p - 1):
            l.append(gen ** i % p)

        if sorted(l) == zp:
            g = gen
            break
    x = random.randint(0, p - 1)

    X = g ** x % p
    print("public key = (p,g,X): (" + str(p) + "," + str(g) + "," + str(X) + ")")
    print("private key = x:", x)
    return (p, g, X), x


def is_prime(n):
    # pretty bad, could be improved with 6k +-1 optimization
    # or importing probably
    if n == 0:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


def elgamal_encrypt(pub_key, m):
    p = pub_key[0]
    g = pub_key[1]
    X = pub_key[2]

    y = random.randint(0, p - 1)
    Y = g ** y % p
    K = X ** y % p
    C = m * K % p

    return Y, C


def elgamal_decrypt(priv_key, pub_key, Y, C):
    p = pub_key[0]
    x = priv_key
    K = Y ** x % p
    m = pow(K, -1, p) * C % p

    return m


def elgamal_encrypt_string(m, pub):
    m_ascii = [ord(c) for c in m]

    m_ascii_enc = []
    for c in m_ascii:
        m_ascii_enc.append(elgamal_encrypt(pub, c))
    return m_ascii_enc


def elgamal_decrypt_string(m_enc, priv, pub):
    m_ascii_dec = []
    for c in m_enc:
        Y, C = c
        m_ascii_dec.append(elgamal_decrypt(priv, pub, Y, C))

    m_dec = [chr(c) for c in m_ascii_dec]
    m = ''.join(m_dec)
    return m


print("==- El Gamal Encryption-==")
print("---Alice's keys---")
a_pub, a_priv = elgamal_keygen()  # ([], 13, 2, 11), 7
print("----Bobs keys-----")
b_pub, b_priv = elgamal_keygen()
print("------------------")

# Bob wants to send a message to Alice so he uses her public key for encryption
m = "Hello Alice, this is Bob!"
m_enc = elgamal_encrypt_string(m, a_pub)

print("Bob sends the message: \"" + str(m) + "\"")
print("Using Alice's public key, he encrypted it to:", m_enc)

# Alice receives the message and decrypts using her private key
m_dec = elgamal_decrypt_string(m_enc, a_priv, a_pub)
print("Alice receives it and decrypts it to be: \"" + m_dec + "\"")

if m == m_dec:
    print("The message was recovered successfully")
else:
    print("The message was not recovered")
