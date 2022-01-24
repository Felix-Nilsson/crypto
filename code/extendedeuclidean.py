def eeuclidean(a, b):
    r = [a, b]
    q = [0, 0]
    s = [1, 0]
    t = [0, 1]

    i = 0
    while True:
        ri = r[i] % r[i + 1]
        qi = int(r[i] / r[i + 1])

        r.append(ri)
        q.append(qi)

        if ri == 0:
            break

        i = i + 1

    for i in range(2, len(r)):
        si = s[i - 2] - q[i] * s[i - 1]
        ti = t[i - 2] - q[i] * t[i - 1]

        s.append(si)
        t.append(ti)

    # matrix = [r,q,s,t]

    print("=====-Ext.Euclidean Table-=====")
    print("r     q     s     t")
    print("-------------------")
    for i in range(len(r)):
        print(r[i], "   ", q[i], "   ", s[i], "   ", t[i])
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

    print("================================")
    print("Best equation:", a, "*", s[-2], "+", b, "*", t[-2], "= 1")
    print("Modular inverse of", r[1], "is", t[-2], "or", t[-2] + r[0])
    print("GCD of", a, "and", b, "is", r[-2])


eeuclidean(42, 25)
# note: breaks in cases like eeuclidean(100,10), maybe since there is no such case of a and b 100a + 10b = 1
# note 2: is there a way to say when there is no integer solutions a and b such that xa + yb = 1,
# for some integers x and y?
