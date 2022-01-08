import random

# Alice and Bob agree on a modulus p and a base g
def diffiehellman(g, p):
    # Alice picks a secret key a (<100 for practical purposes)
    a = random.randint(0,100)

    # And generates a public key A
    A = (g ** a) % p

    # Bob picks a secret key b (<100 for practical purposes)
    b = random.randint(0,100)

    # And generates a public key B
    B = (g ** b) % p

    # Bob sends B to Alice
    # She generates K_A (or just K) which is their shared key
    K_A = (B ** a) % p

    # Alice sends A to Bob
    # He generates K_B (or just K) which is their shared key
    K_B = (A ** b) % p

    # They should always be the same if done correctly
    if K_A == K_B:
        print("Secret shared number is:", K_A)

print("==- Diffie-Hellman Key Exchange -==")
diffiehellman(5, 23)
