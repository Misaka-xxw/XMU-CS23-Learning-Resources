import numpy as np
import matplotlib.pyplot as plt


def ok(sl, sw, k) -> bool:
    global w, l, grid, rockL, rockW
    if sl + rockL[k] >l or sw + rockW[k] > w:
        return False
    for i in range(sl, sl + rockL[k]):
        for j in range(sw, sw + rockW[k]):
            if grid[i][j] > 0:
                return False
    return True


def paint(sl, sw, k):
    global w, l, grid, rockL, rockW, res, color
    for i in range(sl, sl + rockL[k]):
        for j in range(sw, sw + rockW[k]):
            grid[i][j] = color
    res += rockV[k]
    color += 1


def nextRock(k):
    for i in range(l):
        for j in range(w):
            if ok(i, j, k):
                return i, j
    return False


def input_init():
    global l, w, area, rockL, rockW, rockV, nums, color, grid, res
    color = 1
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
    grid = [[0 for a in range(w)] for b in range(l)]
    res=0


def solve():
    global l, w, grid, res, nums
    for i in range(nums):
        j = nextRock(i)
        if j:
            paint(j[0], j[1], i)
    print("最大利用率:%.2f%%" % (res * 100 / (l * w)))
    print('切割情况：')
    grid = np.array(grid)
    print(grid)
    plt.imshow(grid, cmap='magma', interpolation='nearest', extent=(0, w, 0, l))
    plt.colorbar()
    plt.grid()
    plt.title("maximum rate:%.2f%%" % (res * 100 / (l * w)))
    plt.savefig(r'res.png')
    plt.show()


if __name__ == '__main__':
    input_init()
    solve()
    # 大错特错，还是dp好
