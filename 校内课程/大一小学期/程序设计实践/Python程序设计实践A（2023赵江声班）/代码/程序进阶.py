n = input()
j = 0
isempty=False
for i in range(0, len(n)):
    isempty=False
    if n[i] == ' ':
        isempty=True
        if j == 0:
            print(n[i - 1::-1],end='')
        else:
            print('', n[i - 1:j:-1],end='')
        j = i
if not isempty:
    print('', n[len(n)-1:j:-1])
