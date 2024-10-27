def fun(n):
    if n==1:
        print('{:d} is not prime'.format(n))
        return
    for i in range(2,n):
        if n%i==0:
            print('{:d} is not prime'.format(n))
            return
    print('{:d} is prime'.format(n))

n=int(input())
a = []
for i in range(0, n):
    temp=int(input())
    a.append(temp)
for i in a:
    fun(i)