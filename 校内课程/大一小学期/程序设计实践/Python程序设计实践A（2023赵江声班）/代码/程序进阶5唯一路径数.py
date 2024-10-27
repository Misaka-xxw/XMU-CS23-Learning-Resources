x, y = map(int, input().split())


def fun(i, j):
    if i == x and j == y:
        return 1
    if j == y:
        return fun(i + 1, j)
    if i == x:
        return fun(i, j + 1)
    return fun(i + 1, j) + fun(i, j + 1)


print(fun(1, 1))
#动态规划