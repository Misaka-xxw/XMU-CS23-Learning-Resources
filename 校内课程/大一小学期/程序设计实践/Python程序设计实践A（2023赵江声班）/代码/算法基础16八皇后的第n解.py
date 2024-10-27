n = 8
arr = [0 for i in range(0, n + 1)]
result = []


def dfs(row):
    if row > n:
        result.append(arr[1:])
        return
    for j in range(1, n + 1):
        put_queen = True
        for i in range(1, row):  # 竖着没皇后
            if j == arr[i] or i + arr[i] == row + j or i + j == row + arr[i]:
                put_queen = False
                break
        if put_queen:
            arr[row] = j
            dfs(row + 1)


count = 1
dfs(1)
m = int(input())
for i in range(0, m):
    x = int(input())
    print(''.join(map(str, result[x - 1])))
