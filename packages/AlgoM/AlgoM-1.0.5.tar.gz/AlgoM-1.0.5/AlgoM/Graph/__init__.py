#Graph adjacency matrix, undirected, weighted
from heapq import heappop as pop, heappush as push
class Graph:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj
 

    def dist(self, s, e):
        self.vis = set()
        self.dist = [10**18]*self.n
        q = []
        self.dist[s] = 0
        push(q, (0, 0))
        while len(q) > 0:
            d, u = pop(q)
            if u in self.vis:
                continue
            self.vis.add(u)
            for v, w in self.adj[u]:
                new_dist = self.dist[u] + w
                if new_dist < self.dist[v]:
                    self.dist[v] = new_dist
                    push(q, (self.dist[v], v))
        return self.dist[e]
"""
#Directed, weighted, adjacency list
class Graph2:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj



#Strongly connected components (Kosorajus)
n, m = map(int, input().split())
graph = [[] for _ in range(n)]
gr = [[] for _ in range(n)]
for edge in range(m):
  a, b = map(int, input().split())
  graph[a].append(b)
  gr[b].append(a)
stack = []
visited = [False]*(n)
vis = [False]*(n)
connected = [] #this stores a list for each strongly connected component

def DFS(v, curr):
  global vis
  global gr
  vis[v] = True
  connected[curr].append(v)
  for i in gr[v]:
    if not vis[i]:
      DFS(i,curr)

def fillOrder(v):
  global visited
  global stack
  visited[v] = True
  for i in graph[v]:
    if not visited[i]:
      fillOrder(i)
  stack.append(v)
      
   
for i in range(n):
  if not visited[i]:
     fillOrder(i)

curr = -1
while stack:
  i = stack.pop()
  if not vis[i]:
    connected.append([])
    curr += 1
    DFS(i, curr)

num = len(connected)


#----------------------------------------


#Min-cut (Dinic's algorithm)
from collections import deque
n, m = map(int, input().split())
graph = [[0 for _ in range(n)] for _ in range(n)]
org_graph = [[0 for _ in range(n)] for _ in range(n)]
for edge in range(m):
  a, b, c = map(int, input().split())
  graph[a-1][b-1] = c
  org_graph[a-1][b-1] = c

ans = []
def BFS(s, t, parent): 
  visited = [False] *(n) 
  queue= deque()
  queue.append(s) 
  visited[s] = True
  while queue: 
    u = queue.pop() 
    for ind, val in enumerate(graph[u]): 
      if visited[ind] == False and val > 0 : 
        queue.appendleft(ind) 
        visited[ind] = True
        parent[ind] = u 
  
  return True if visited[t] else False

def dfs(graph,s,visited):
  visited[s] = True
  for i in range(len(graph)):
    if graph[s][i]>0 and not visited[i]:
      dfs(graph,i,visited)
  
def minCut(source, sink): 
  global ans
  parent = [-1]*(n) 
  max_flow = 0 # There is no flow initially 
  while BFS(source, sink, parent) : 
    path_flow = float("inf") 
    s = sink 
    while(s != source): 
      path_flow = min(path_flow, graph[parent[s]][s]) 
      s = parent[s] 
      max_flow += path_flow 
      v = sink 
    while(v != source): 
      u = parent[v] 
      graph[u][v] -= path_flow 
      graph[v][u] += path_flow 
      v = parent[v] 
  
  visited = n * [False]
  dfs(graph,source,visited)
 
  for i in range(n): 
    for j in range(n): 
      if graph[i][j] == 0 and org_graph[i][j] > 0 and visited[i]: 
        ans.append([i, j])

minCut(0, n-1)
print(ans)


#----------------------------------------


#Floyd Warshall (adjacency matrix!)
class Graph3:
    INF = float("inf")
    def __init__(self, n, graph):   
        self.graph = graph
        self.ans = [[INF for _ in range(n)] for _ in range(n)]
        
    for k in range(n):
        for i in range(n):
            for j in range(n):
            ans[i][j] = min(ans[i][j], graph[i][k] + graph[k][j]))

#----------------------------------------

#Topological sort 
n, m = map(int, input().split())
graph = [[] for _ in range(n)]
visited = [False for _ in range(n)]
ans = []

for _ in range(m):
  a, b = map(int, input().split())
  graph[a-1].append(b-1)

def topological_sort():
  global visited
  for node in range(n):
    if not visited[node]:
      dfs(node)

def dfs(node):
  global visited
  global ans
  visited[node] = True
  for neigh in graph[node]:
    if visited[neigh] == False:
      dfs(neigh)
  ans.append(node)

topological_sort()
ans.reverse()
print(ans)



#Find cycle
def cycle(v, visited, recStack):
  visited[v] = True
  recStack[v] = True
  for neighbour in graph[v]:
    if visited[neighbour] == False:
      if cycle(neighbour, visited, recStack):
        return True
      elif recStack[neighbour] == True:
        return True

  recStack[v] = False
  return False
 
  def isCyclic():
    visited = [False] * (n)
    recStack = [False] * (n)
    for node in range(n):
      if visited[node] == False:
        if cycle(node,visited,recStack):
          return True
    return False

#----------------------------------------

#Find articulation points/bridges
n, m = map(int, input().split())
low = [0 for _ in range(n)]
num = [-1 for _ in range(n)]
graph = [[] for _ in range(n)]
c = 0
root = 0
root_children = 0
ans = [0 for _ in range(n)]
parent = [0] * n
bridges = []
def find(node):
  global c
  global root_children
  num[node] = c
  c += 1
  low[node] = num[node]
  for neigh in graph[node]:
    if num[neigh] == -1:
      parent[neigh] = node
      if node == root:
        root_children += 1
      find(neigh)
      if low[neigh] >= low[node]:
        ans[node] = 1
    #for bridges
      if low[neigh] > low[node]:
        bridges.append([node, neigh])
      low[node] = min(low[node], low[neigh])
    elif neigh != parent[node]:
      low[node] = min(low[u], num[neigh])


for _ in range(m):
  a, b = map(int, input().split())
  graph[a].append(b)

for u in range(n):
  if num[u] == -1:
    root = u
    root_children = 0
    find(root)
    ans[root] = (root_children > 1)

for i, j in enumerate(ans):
  if j:
    print(i)

"""