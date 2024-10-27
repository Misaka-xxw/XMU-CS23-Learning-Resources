t, n = map(int, input().split())
arr = list(map(int, input().split()))
arr.sort()
m2, r = 0, n - 1
while m2 < r:
    if arr[m2] + arr[r] < t:
        m2 += 1
    elif arr[m2] + arr[r] > t:
        r -= 1
    else:
        print(m2, r)
        m2 += 1
