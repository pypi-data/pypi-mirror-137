import math
import sys
sys.setrecursionlimit(10**6)


#Undirected, unweighted, 1-indexed
class Tree:
    def __init__(self, n, tree):
        self.n = n
        self.tree = tree
        self.log = log = math.ceil(math.log(n, 2))
        self.memo = [[-1 for i in range(log + 1)] for j in range(n+1)]
        self.lev = [0 for i in range(n + 1)]
        self.dfs(1, 1, self.memo, self.lev, log, tree)
        self.size = [0 for _ in range(n+1)]

    def dfs(self, u, p):
        self.memo[u][0] = p
        for i in range(1, self.log + 1):
            self.memo[u][i] = self.memo[self.memo[u][i - 1]][i - 1]
            
        for v in self.tree[u]:
            if v != p:
                self.lev[v] = self.lev[u] + 1
                self.dfs(v, u)
 
    def lca(self, u, v):
        if self.lev[u] < self.lev[v]:
            u, v = v, u
        for i in range(self.log, -1, -1):
            if (self.lev[u] - pow(2, i)) >= self.lev[v]:
                u = self.memo[u][i]   
        if u == v:
            return v
        for i in range(self.log, -1, -1):
            if self.memo[u][i] != self.memo[v][i]:
                u = self.memo[u][i]
                v = self.memo[v][i]    
        return self.memo[u][0]

    def get_dist(self, u, v):
        lc = self.lca(u, v)
        ans = self.lev[u] + self.lev[v] - (2 * self.lev[lc])
        return ans


    def find(self, u, p):
        self.size[u] = 1
        for v in self.tree[u]:
            if v != p:
                self.find(v, u)
                self.size[u] += self.size[v]

    def centroid(self, u, p, sz):
        for v in self.tree[u]:
            if p != v:
                if self.size[v] * 2 > sz:
                    return self.centroid(v, u, sz)
        return u

    def get_centroid(self):
        self.find(1, -1) 
        ans = self.centroid(1, -1, self.n)




