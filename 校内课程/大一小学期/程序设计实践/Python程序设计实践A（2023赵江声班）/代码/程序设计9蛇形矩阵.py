n, m = map(int, input().split(' '))
arr = [[0] * m for _ in range(n)]
i = j = 0
left, right, up, down = 1, 2, 3, 4
d = right
arr[0][0] = 1
num = 2

while num <=n * m:
    if d == left:
        if j == 0:
            d = up
        elif arr[i][j-1] != 0:
            d = up
        else:
            j -= 1
            arr[i][j] = num
            num += 1
    elif d == right:
        if j == m - 1 :
            d = down
        elif arr[i][j+1] != 0:
            d = down
        else:
            j += 1
            arr[i][j] = num
            num += 1
    elif d == up:
        if i == 0:
            d = right
        elif arr[i-1][j] != 0:
            d = right
        else:
            i -= 1
            arr[i][j] = num
            num += 1
    elif d == down:
        if i == n - 1:
            d = left
        elif arr[i+1][j] != 0:
            d = left
        else:
            i += 1
            arr[i][j] = num
            num += 1

for i in range(0, n):
    for j in range(0, m - 1):
        print(arr[i][j], end=' ')
    print(arr[i][m - 1])
