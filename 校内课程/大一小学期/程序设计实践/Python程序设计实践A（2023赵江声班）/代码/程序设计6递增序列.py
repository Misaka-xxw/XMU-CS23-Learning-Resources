a = []
for i in range(0, 4):
    temp=int(input())
    a.append(temp)


def fun(n):
    for i in range(1, n):
        print(i, end=' ')
    if n != 0:
        print(n, end='')
    print()


for i in a:
    fun(i)