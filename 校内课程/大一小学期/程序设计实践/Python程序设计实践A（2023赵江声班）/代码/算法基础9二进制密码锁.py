a = input()
b = input()
lock0 = []
len_of_lock = len(a)
for i in range(len_of_lock):
    lock0.append(int(a[i]) ^ int(b[i]))
if len_of_lock>1:
    solve = False
    mincount = 0
    for start in range(0, 2):
        lock = [0] * len_of_lock
        for i in range(len_of_lock):
            lock[i] = lock0[i]
        count = 0
        if start:
            lock[0] = 1 - lock[0]
            lock[1] = 1 - lock[1]
            count += 1
        for i in range(1, len_of_lock - 1):
            if lock[i - 1]:
                lock[i] = 1 - lock[i]
                lock[i + 1] = 1 - lock[i + 1]
                count+=1
        if lock[len_of_lock-2]:
            lock[len_of_lock-1]=1-lock[len_of_lock-1]
            count+=1
        if lock[len_of_lock - 1] == 0:
            if solve:
                mincount = min(count, mincount)
            else:
                mincount = count
                solve = True
    if solve:
        print(mincount)
    else:
        print('impossible')
