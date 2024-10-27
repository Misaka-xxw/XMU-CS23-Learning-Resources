n = int(input())
first=True
for i in range(2,n+1):
    isPrime = True
    for j in range(2,i):
        if i % j == 0:
            isPrime=False
            break
    if isPrime:
        if first:
            print(i, end='')
            first = False
        else:
            print('',i, end='')
