from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

l, w = 4, 8
area = l * w
rocks = [(3, 2), (2, 4), (1, 6), (4, 4)]
nums = len(rocks)
have = [False for i in range(nums)]


class Node:
    def __init__(self, colored=0, map=None, use=None):
        global nums
        self.colored = colored
        self.used = [False for i in range(nums)]
        if map is not None:
            self.map = map
        else:
            self.map = []
        if use != None:
            self.used[use] = True
        # (x0,x1,y1,y2)

    def __add__(self, other):
        return Node(colored=self.colored + other.colored, map=self.map + other.map)

    def print(self):
        print(self.colored, self.map)

    def show(self):
        grid = np.zeros((l, w), dtype=int)
        for n, m in enumerate(self.map):
            for i in range(m[0], m[1]):
                for j in range(m[2], m[3]):
                    grid[i, j] = n + 1
        plt.imshow(grid, cmap='magma', interpolation='nearest', extent=(0, w, 0, l))
        plt.colorbar()
        plt.grid()
        plt.title('rate:' + str(res.colored / area * 100) + '%')
        plt.savefig(r'res.png')
        plt.show()



def dfs(color: int, x0: int, x1: int, y0: int, y1: int) -> Node:
    global have, nums
    max_node = Node()
    have0 = deepcopy(have)
    if color <= nums:
        for i in range(nums):
            if have[i]:
                continue
            if rocks[i][0] <= x1 - x0 and rocks[i][1] <= y1 - y0:
                have0[i] = have[i] = True
                x, y = x0 + rocks[i][0], y0 + rocks[i][1]
                # print(x,y)

                node = Node(colored=rocks[i][0] * rocks[i][1], map=[(x0, x, y0, y)], use=i)
                nodes = [(x, x1, y0, y), (x, x1, y0, y1),
                         (x0, x, y, y1), (x0, x1, y, y1)]
                for j in range(4):
                    node1 = dfs(color + 1, nodes[j][0], nodes[j][1], nodes[j][2], nodes[j][3])
                    for i in range(nums):
                        if node1.used[i]:
                            have[i] = True
                    have[j] = True
                    node2 = dfs(color + 1, nodes[3 - j][0], nodes[3 - j][1], nodes[3 - j][2], nodes[3 - j][3])
                    node3 = node1 + node2 + node
                    if node3.colored > max_node.colored:
                        max_node = deepcopy(node3)
                    have = deepcopy(have0)
                have0[i] = have[i] = False
    # print(color, x0, x1, y0, y1)
    # max_node.print()
    return max_node


res = dfs(1, 0, l, 0, w)
print(res.colored / area)
res.show()
