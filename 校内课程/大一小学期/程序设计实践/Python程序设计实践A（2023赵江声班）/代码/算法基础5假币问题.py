n = int(input())
leftright_list = []
condition_list = []

for t in range(n):
    leftright, condition = [], []
    for i in range(3):
        s1, s2, s3 = map(str, input().split())
        leftright.append([s1, s2])
        condition.append(s3)
    leftright_list.append(leftright)
    condition_list.append(condition)

for t in range(n):
    leftright = leftright_list[t]
    condition = condition_list[t]
    noteven = []
    coins = dict(zip('ABCDEFGHIJKL', [0] * 12))

    for i in range(3):
        if condition[i] == "even":
            for j in range(2):
                for k in range(len(leftright[i][j])):
                    coins[leftright[i][j][k]] = 2
        else:
            noteven.append(i)

    truewrongcoin, heavy_or_light = None, None

    for dickey in range(ord('A'), ord('L') + 1):
        if coins[chr(dickey)] != 2:
            tempcoins = dict(zip('ABCDEFGHIJKL', [2] * 12))
            heavy_or_light_list = [1, 3]
            for temp_hol in heavy_or_light_list:
                tempcoins[chr(dickey)] = temp_hol
                rightsuppose = True

                for i in noteven:
                    sums = [0] * 2
                    for j in range(2):
                        for k in range(len(leftright[i][j])):
                            sums[j] += tempcoins[leftright[i][j][k]]

                    if (condition[i] == "up" and sums[0] > sums[1]) or (condition[i] == "down" and sums[0] < sums[1]):
                        pass
                    else:
                        rightsuppose = False
                        break

                if rightsuppose:
                    truewrongcoin = chr(dickey)
                    if temp_hol == 3:
                        heavy_or_light = "heavy"
                    else:
                        heavy_or_light = "light"
                    break

    print("{} is the counterfeit coin and it is {}.".format(truewrongcoin, heavy_or_light))
'''
truewrongcoin, heavy_or_light = None, None
endfor=False

for i in noteven:
    for j in range(0, 2):
        for k in range(0, len(leftright[i][j])):
            if tempcoins[leftright[i][j][k]]!=1:
                if condition[i] == "up" and j == 1 or condition[i] == "down" and j == 0:
                    wrongcoin = 3
                else:
                    wrongcoin = 2
                tempcoins = coins
                tempcoins[leftright[i][j][k]] = wrongcoin
                if len(noteven)==2:
                    tempnoteven=noteven
                    tempnoteven.pop(i)
                    i2=tempnoteven[0]
                    for c in range(0, len(leftright[i][j])):
                        for b in range(0,2):
                            if b!=j and c!=k:
'''
