def myprint(n, x, y):
    print(n, ':', x, '->', y, sep='')


def dfs(n, from0, pass0, to0):
    if n == 1:
        myprint(n, from0, to0)
    else:
        dfs(n - 1, from0, to0, pass0)
        myprint(n, from0, to0)
        dfs(n - 1, pass0, from0, to0)


n, a, b, c = map(str, input().split())
n = int(n)
dfs(n, a, b, c)
