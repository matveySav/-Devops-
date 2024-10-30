import sys

def count_divisors(x):
    c = 0
    s = 1
    if x**0.5 == int(x**0.5) and x != 1:
        c+=1
        s = 0
    for i in range(1,int(x**0.5)+s):
        if x % i == 0:
            c += 2
    print(f'Number {x} has {c} divisors')
    return c

if __name__ == "__main__":
    count_divisors(int(sys.argv[1]))
