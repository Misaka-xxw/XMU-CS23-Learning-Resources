from copy import deepcopy
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt


class how(Enum):
    origin = 0
    horizon = 1
    vertical = 2


def debug(d):
    for i in range(1, l + 1):
        for j in range(1, w + 1):
            print(f[d][i][j], end=' ')
        print()
    print()


def input_init():
    global l, w, area, rockL, rockW, rockV, nums, f, method
    nums = int(input('请输入你想要分割的石材数。如果输入是0的话进入案例模式：'))
    if nums == 0:
        l, w = 4, 8  # 长，宽
        rockL = [3, 2, 1, 4]
        rockW = [2, 4, 6, 4]
        nums = len(rockL)
    else:
        l = int(input('请输入总石材长度：'))
        w = int(input('请输入总石材宽度：'))
        rockL, rockW = [], []
        for i in range(nums):
            length, width = map(int, input(f'请输入石材{i + 1}的长度和宽度,用空格分隔: ').split())
            rockL.append(length)
            rockW.append(width)
    area = l * w
    rockV = [rockL[i] * rockW[i] for i in range(nums)]
    sorted_data = sorted(zip(rockV, rockL, rockW), reverse=True)
    rockV, rockL, rockW = zip(*sorted_data)
    f = [[0 for a in range(w + 1)] for b in range(l + 1)]
    method = [[[] for a in range(w + 1)] for b in range(l + 1)]


def solve():
    for i in range(rockL[0], l + 1):
        for j in range(rockW[0], w + 1):
            f[i][j] = rockV[0]
            method[i][j].append((0, how.origin))

    for chose in range(1, nums):
        for i in range(l, rockL[chose]-1, -1):
            for j in range(w, rockW[chose]-1, -1):
                lastmethod = deepcopy(method[i][j])
                s = f[i - rockL[chose]][j] + rockV[chose]
                t = f[i][j - rockW[chose]] + rockV[chose]
                if s > f[i][j] and s >= t:
                    f[i][j] = s
                    method[i][j] = deepcopy(lastmethod) + [(chose, how.horizon)]
                elif t > f[i][j] and t > s:
                    f[i][j] = t
                    method[i][j] = deepcopy(lastmethod) + [(chose, how.vertical)]

    print("最大利用率:%.2f%%" % (f[l][w] * 100 / (l * w)))
    grid = np.zeros((l, w), dtype=int)
    x, y = 0, 0
    steps = {
        how.origin: (0, 0),
        how.horizon: (1, 0),
        how.vertical: (0, 1)
    }
    for color, a in enumerate(method[l][w]):
        x, y = x + steps[a[1]][0] * rockL[a[0]], y + steps[a[1]][1] * rockW[a[0]]
        for i in range(x, x + rockL[a[0]]):
            for j in range(y, y + rockW[a[0]]):
                grid[i, j] = color + 1

    print('切割情况：')
    print(grid)
    plt.imshow(grid, cmap='magma', interpolation='nearest', extent=(0, w, 0, l))
    plt.colorbar()
    plt.grid()
    plt.title("maximum rate:%.2f%%" % (f[l][w] * 100 / (l * w)))
    plt.savefig(r'res.png')
    plt.show()


if __name__ == '__main__':
    input_init()
    solve()
