def nextstep(n):
    if n==0:
        print('2(0)',end='')
        return
    if n == 1:
        print('2',end='')
        return
    print('2(', end='')
    dfs(n)
    print(')', end='')
    return


def dfs(n):
    # print('the num',n)
    if n == 0:
        print('0', end='')
        return
    if n == 1:
        print('2(0)', end='')
        return
    arr = []
    i_append = 0
    while n:
        if n & 1:
            arr.append(i_append)
        i_append += 1
        n //= 2
    arr_len = len(arr)
    nextstep(arr[arr_len - 1])
    for i in range(arr_len - 2, -1, -1):
        print('+', end='')
        nextstep(arr[i])


n = int(input())
dfs(n)
