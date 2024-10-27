n = int(input())
arr = [0 for i in range(0, n)]


def dfs(row):
    if row == n:
        for i in range(0, n):
            # print(arr[i],end='')
            for j in range(0, n):
                if j == arr[i]:
                    print('Q', end='')
                if j != arr[i]:
                    print('.', end='')
            print('')
        print('')
        return
    for j in range(0, n):
        put_queen = True
        for i in range(0, row):  # 竖着没皇后
            if j == arr[i] or i + arr[i] == row + j or i + j == row + arr[i]:
                put_queen = False
                break
        if put_queen:
            arr[row] = j
            dfs(row + 1)


dfs(0)
