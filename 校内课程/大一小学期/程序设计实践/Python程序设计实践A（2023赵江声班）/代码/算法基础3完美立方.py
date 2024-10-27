n=int(input())
lifang=[0]
for i in range(1,n+1):
    lifang.append(i**3)
    for a in range(2,i):
        for b in range(a,i):
            for c in range(b,i):
                if lifang[a]+lifang[b]+lifang[c]==lifang[i]:
                    print('Cube = {}, Triple = ({},{},{})'.format(i,a,b,c))