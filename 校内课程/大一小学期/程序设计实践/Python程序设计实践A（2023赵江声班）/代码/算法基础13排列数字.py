n = 0
have_put = [False] * 9
nums = []


def dfs(d):
    if (d == n):
        print(' '.join(nums),'')
    for i in range(1, n + 1):
        if not have_put[i]:
            nums.append(str(i))
            have_put[i] = True
            dfs(d + 1)
            nums.pop()
            have_put[i] = False


n = int(input())
dfs(0)
