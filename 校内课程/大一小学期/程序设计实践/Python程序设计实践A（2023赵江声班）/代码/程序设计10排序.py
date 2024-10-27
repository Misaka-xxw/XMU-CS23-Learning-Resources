n = int(input())
arr = n * [0]
haveput = (n + 1) * [False]
huiche=0

def fun(m):
    if m == n:
        for i in range(0, n-1):
            print(arr[i],end=' ')
        print(arr[n-1], end='')
        print()
    for i in range(1, n + 1):
        if not haveput[i]:
            arr[m] = i
            haveput[i] = True
            fun(m + 1)
            haveput[i] = False


fun(0)
'''
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
'''