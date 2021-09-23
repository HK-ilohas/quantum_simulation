from random import randint
from math import gcd
import csv


def order(a, N):
    for i in range(1, N):
        if pow(a, i, N) == 1:
            return i


data = []

for N in range(3, 100000):
    order_counts = 0
    while True:
        a = randint(2, N-1)
        if gcd(a, N) != 1:
            data.append([N, False, order_counts])
            break
        t = pow(a, (N-1)//2, N)
        if t != 1 and t != N - 1:
            data.append([N, False, order_counts])
            break
        elif t == 1:
            continue
        else:
            ord_a = order(a, N)
            order_counts += 1
            if ord_a == N - 1:
                data.append([N, True, order_counts])
                break


with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
