def dfs():
    global arr
    if arr[0] == '+':
        arr = arr[1:]
        return dfs() + dfs()
    if arr[0] == '-':
        arr = arr[1:]
        return dfs() - dfs()
    if arr[0] == '*':
        arr = arr[1:]
        return dfs() * dfs()
    if arr[0] == '/':
        arr = arr[1:]
        return dfs() / dfs()
    temp = arr[0]
    arr = arr[1:]
    return float(temp)


arr = list(map(str, input().split()))
arr_len = len(arr)
print('{:.6f}'.format(dfs()))
