t, n = map(int, input().split())
arr = list(map(int, input().split()))
arr.sort()
m2, r = 1, n - 1
for l in range(0, n - 2):
    m2 = l + 1
    r = n - 1 - l
    while m2 < r:
        if arr[l] + arr[m2] + arr[r] < t:
            m2 += 1
        elif arr[l] + arr[m2] + arr[r] > t:
            r -= 1
        else:
            print(arr[l], arr[m2], arr[r])
            m2 += 1
