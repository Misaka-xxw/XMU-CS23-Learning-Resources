t, n = map(int, input().split())
arr = list(map(int, input().split()))
arr.sort()
m2, r = 1, n - 1
for l in range(0, n - 3):
    for m1 in range(l + 1, n - 2):
        m2 = m1 + 1
        r = n - 1
        while m2 < r:
            if arr[l] + arr[m1] + arr[m2] + arr[r] < t:
                m2 += 1
            elif arr[l] + arr[m1] + arr[m2] + arr[r] > t:
                r -= 1
            elif arr[l] + arr[m1] + arr[m2] + arr[r] == t:
                print(arr[l],arr[m1], arr[m2], arr[r])
                m2 += 1
                r-=1
