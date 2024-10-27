s = input()
arr=list(s)
#print(arr)
first = True
for i in arr:
    if arr.count(i)== 1:
        if first:
            print(i, end='')
            first = False
        else:
            print('', i, end='')
'''
#arr.sort()
arr2=set(arr)
first=True
for i in arr2:
    if arr.count(i)==1:
        if first:
            print(i,end='')
            first=False
        else:
            print('',i,end='')
'''
