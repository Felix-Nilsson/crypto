import random
from sympy import poly
from sympy.abc import x
from collections import deque


# small second degree example of Shamirs secret sharing
def shamir_generate(p, s):  # p = participants, secret

    # start by generating 2nd degree polynomial with f(0) = s
    a, b = random.sample(range(1, 100), 2)
    y = poly(a * (x ** 2) + b * x + s)

    # generate p points that lies on the polynomial
    points = []
    for i in range(p):
        xi = random.randint(1, 100)  # needs to not pick same x multiple times
        yi = y(xi)

        points.append((xi, yi))

    # print(y)

    # return and distribute a point to every participant
    print("secret polynomial:", y)
    print("secret:", s)
    print("points:", points)
    return points


def shamir_reconstruct(three_points):
    # three out of p of them will need to collaborate to find the secret

    xs = [i[0] for i in three_points]
    ys = [i[1] for i in three_points]

    # create linear combinations that line up with x values such that x:comb
    # for xs = [1,3,5] we need 1:[3,5] , 3:[1,5], 5:[1,3] ie x not in comb

    pairs = lin_comb(xs)

    temp = deque(pairs)
    temp.rotate(2)
    pairs = list(temp)

    res = 0
    # print(xs, pairs)

    # interpolates the original curve with Lagrange polynomials
    # f(x) = sum of y_i*delta_i(x) for i in xs
    # delta_i(x) being formed from the ith pair (f,s) , delta_i(x) = -f/(i-f) * -s/(i-s)
    for i in range(3):
        idx = xs[i]
        f, s = pairs[i]

        delta = ((-f) / (idx - f)) * ((-s) / (idx - s))
        res += delta * ys[i]

    return round(res)


# produces a list of linear combinations of a list
# ie every possible pair (x,y) where x,y are elements in l, note (x,y) = (y,x)
def lin_comb(l):
    pairs = []

    for i in range(len(l)):
        if i + 1 >= len(l):
            pairs.append((l[0], l[-1]))
        else:
            pairs.append((l[i], l[i + 1]))

    return pairs


m = 11

print("==- Shamirs Secret Sharing -==")
print("Generating shares...")
shares = shamir_generate(5, m)
print(shares)

three_shares = random.sample(shares, 3)
print("participants:", three_shares)

print("Reconstructing secret...")
secret = shamir_reconstruct(three_shares)
print("recovered secret:", secret)

if secret == m:
    print("Secret recovered successfully")

# needs modulus, prints and comments
# could be scaled up to n degrees, but constructing deltas would be harder
