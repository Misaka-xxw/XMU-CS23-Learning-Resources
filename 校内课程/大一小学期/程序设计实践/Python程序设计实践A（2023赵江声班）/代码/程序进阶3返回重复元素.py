arr = input().split()
#print(arr)

counts = {}
dups =[]

for ele in arr:
    counts[ele] = counts.get(ele,0) + 1     #从字典counts里找一个ele并返回键值，找不到返回0
    if (counts[ele] > 1 ) and (ele not in dups):
        dups.append(ele)

print(" ".join(dups))


'''

arr2=[]
first=True
for i in arr:
    if arr.count(i)!=1:
        arr2.append(i)
        while i in arr:
            arr.remove(i)
for i in arr2:
    if first:
        print(i, end='')
        first = False
    else:
        print('', i, end='')
'''
'''
# arr.sort()
arr2 = list(set(arr))
print(arr2)
first = True
for i in arr:
    if i not in arr2:
        if first:
            print(i, end='')
            first = False
        else:
            print('', i, end='')
'''