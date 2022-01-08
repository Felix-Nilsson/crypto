import random

#Task 1: Generate a table of powers
#Def Generator: An element g such that {g^i | i = 0,1,...p-2} = Zp*
def tables(p):
    zpstar = {i for i in range(1, p)}
    print(zpstar,"Z")

    #for g in range(1, p):

    s = []
    g = 16

    for i in range(p-1): #range(x) = 0..x-1
        x = (g**i) % p
        s.append(x)

    s = set(s)
    print(s, g, s == zpstar, len(s))

def check_five_pairs():
    s = [1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18] #eg z2*, z3* or z4* or z16*

    for i in range(5):
        a = random.choice(s)
        b = random.choice(s)

        ans = a*b % 23

        print(a, '*', b, '=', a*b, "% 23 =", ans , ans in s)

#tables(23)
check_five_pairs()