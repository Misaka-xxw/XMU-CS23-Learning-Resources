n = int(input())
number = []

for i in range(n):
    temp = list(map(int, input().split()))
    number.append(temp[1:])
for i in range(n):
    number[i].sort()
    print(' '.join(map(str, number[i])))