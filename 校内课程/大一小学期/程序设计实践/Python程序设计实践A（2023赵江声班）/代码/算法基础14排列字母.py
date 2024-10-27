word = input()
n = len(word)
have_put = [False] * (n + 1)
nums = []
word=list(word)

def quicksort(start, end):
    if start >= end:
        return
    temp, left, right = start, start, end
    while left < right:
        while left < right and ord(word[right]) >= ord(word[temp]):
            right -= 1
        while left < right and ord(word[left]) <= ord(word[temp]):
            left += 1
        word[left], word[right] = word[right], word[left]
    word[temp], word[right] = word[right], word[temp]
    quicksort(start, left - 1)
    quicksort(right + 1, end)


quicksort(0, n - 1)


def dfs(d):
    if (d == n):
        print(''.join(nums))
    for i in range(0, n):
        if not have_put[i]:
            nums.append(word[i])
            have_put[i] = True
            dfs(d + 1)
            nums.pop()
            have_put[i] = False


dfs(0)
