def dfs(d):
    global m, counts, last
    if d == n:
        if m == 0:
            counts += 1
        return
    pre_last=last
    for i in range(pre_last, m + 1):
        m -= i
        last = i
        dfs(d + 1)
        m += i


t = int(input())
for t0 in range(t):
    m, n = map(int, input().split())
    last, counts = 0, 0
    dfs(0)
    print(counts)
