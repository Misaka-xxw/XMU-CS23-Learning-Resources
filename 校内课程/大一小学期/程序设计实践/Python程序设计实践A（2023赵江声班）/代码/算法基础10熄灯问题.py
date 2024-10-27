n = int(input())


def change(i, j):
    arr[i][j] = 1 - arr[i][j]


def push(i, j):
    change(i, j)
    if i > 0:
        change(i - 1, j)
    if i < 4:
        change(i + 1, j)
    if j > 0:
        change(i, j - 1)
    if j < 5:
        change(i, j + 1)


for t in range(n):
    arr0 = []
    for i in range(5):
        temp = list(map(int, input().split()))
        arr0.append(temp)

    arr = [[0] * 6 for x in range(5)]
    button = []

    for k in range(1 << 6):
        for i in range(5):
            for j in range(6):
                arr[i][j] = arr0[i][j]

        button = [[0] * 6 for x in range(5)]

        for j in range(6):
            if (1 << j) & k:
                button[0][j] = 1
                push(0, j)

        for i in range(1, 5):
            for j in range(6):
                if arr[i - 1][j]:
                    button[i][j] = 1
                    push(i, j)

        allclose = True
        for j in range(6):
            if arr[4][j]:
                allclose = False
                break

        if allclose:
            print('PUZZLE #{}'.format(t + 1))
            for i in range(5):
                print(' '.join(str(x) for x in button[i]), '')
            break
