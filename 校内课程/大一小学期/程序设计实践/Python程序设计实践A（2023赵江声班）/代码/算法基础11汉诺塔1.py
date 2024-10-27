def myprint(x, y):
    print(x, '->', y, sep='')


def dfs(n, from0, pass0, to0):
    if n == 1:
        myprint(from0,to0)
    else:
        dfs(n-1,from0,to0,pass0)
        myprint(from0,to0)
        dfs(n-1,pass0,from0,to0)

n=int(input())
dfs(n,'A','B','C')