from heapq import *
from copy import deepcopy
from random import randint
import matplotlib.pyplot as plt
import networkx as nx


# 完善了代码
class Dsu:  # 并查集
    def __init__(self, size):
        size += 1
        self.pa = list(range(size))
        self.size = [1] * size

    def find(self, x):
        if self.pa[x] != x:
            self.pa[x] = self.find(self.pa[x])
        return self.pa[x]

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y:
            return
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.pa[y] = x
        self.size[x] += self.size[y]


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __lt__(self, other):
        return self.w < other.w

    def tran(self):
        return self.u, self.v, self.w


def tuple(e: Edge):
    return e.u, e.v, e.w


class Graph:
    def __init__(self, vnum):
        self.vnum = vnum
        # self.V = {i for i in range(1, vnum)}
        self.Adj = [[] for i in range(vnum + 1)]
        self.enum = 0
        self.E = []
        self.w = [[0] * (vnum + 1)] * (vnum + 1)

    def edge_push(self, u, v, w):
        self.enum += 1
        e = Edge(u, v, w)
        self.E.append(e)
        # self.w[u][v] = self.w[v][u] = w
        # print(u,v,w)
        self.Adj[u].append(e)
        self.Adj[v].append(Edge(v, u, w))


def Kruskal(G: Graph):
    dsu = Dsu(G.vnum)
    A = []
    E = deepcopy(G.E)
    heapify(E)
    while E:
        e = heappop(E)
        if dsu.find(e.u) == dsu.find(e.v):
            # print(f"{e.u},{e.v},{e.w},NO")
            continue
        # print(f"{e.u},{e.v},{e.w},YES")
        dsu.union(e.u, e.v)
        A.append(e)
    return A


def Prim(G, s):
    # n = G.vnum + 1
    w = deepcopy(G.w)
    A = []
    Q = []
    Q.append(1)
    for i in range(1, G.vnum):
        umin, vmin = 0, 0
        wmin = 1000000000000
        for u in Q:
            for j in G.Adj[u]:
                # print(j.u,j.v,j.w)
                v = j.v
                if v in Q:
                    continue
                if j.w < wmin:
                    wmin = j.w
                    umin = u
                    vmin = v
        Q.append(vmin)
        print(umin, vmin)
        A.append(Edge(umin, vmin, wmin))
        # w[vmin][umin] = w[umin][vmin] = 0
    return A


def rand_graph():
    vnum = 10
    wn = 20
    G = Graph(vnum)
    fm = randint(1, 10)
    fz = randint(1, fm)
    dsu = Dsu(vnum)
    for u in range(1, vnum + 1):
        for v in range(u + 1, vnum + 1):
            if (randint(1, fm) <= fz):
                dsu.union(u, v)
                w = randint(1, wn)
                G.edge_push(u, v, w)
    for u in range(2, vnum + 1):
        if dsu.find(u) != dsu.find(1):
            v = randint(1, u - 1)
            dsu.union(u, v)
            w = randint(1, wn)
            G.edge_push(u, v, w)
    return G


def showpic(g):
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, alpha=0.5)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.show()


def generate(s):
    g = nx.Graph()
    for e in s:
        print(tuple(e))
    print()
    g.add_weighted_edges_from([tuple(e) for e in s])
    return g


def test(G: Graph):
    prim = Prim(G, randint(1, G.vnum))
    kruskal = Kruskal(G)
    print("Graph")
    g = generate(G.E)
    print("Prim")
    p = generate(prim)
    print("Kruskal")
    k = generate(kruskal)
    showpic(g)
    showpic(p)
    showpic(k)


if __name__ == "__main__":
    G = rand_graph()
    test(G)
