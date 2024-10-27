casenum=1
while True:
    p,e,i,d=map(int,input().split())
    if p==-1 and e==-1 and i==-1 and d==-1:
        break
    for result in range(1,21253):
        if (result+d)%23==p%23 and (result+d)%28==e%28 and (result+d)%33==i%33:
            print('Case {}: the next triple peak occurs in {} days.'.format(casenum, result))
            casenum+=1
            break