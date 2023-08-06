#Segment tree for sum; 0-indexed; all intervals are inclusive
class SegmentTreeSum:
    def __init__(self, n, arr):
        self.t = [0 for _ in range(4*n)]
        self.n = n
        self.arr = arr

    def build(self, a, v, tl, tr):
        if (tl == tr):
            t[v] = a[tl]
        else:
            tm = (tl + tr) // 2
            self.build(a, v*2, tl, tm)
            self.build(a, v*2+1, tm+1, tr)
            self.t[v] = self.t[v*2] + self.t[v*2+1]

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return t[v]
        tm = (tl + tr) // 2
        return self.query(v*2, tl, tm, l, min(r, tm)) + self.query(v*2+1, tm+1, tr, max(l, tm+1), r)


    def update(self, v, tl, tr, pos, new_val):
        if tl == tr:
            self.t[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, new_val)
            else:
                self.update(v*2+1, tm+1, tr, pos, new_val)
                self.t[v] = self.t[v*2] + self.t[v*2+1]
    

 """"   
 #---------------------------------------------------   
    

#Segment tree for max; also has find first element greater than x query; inclusive and 0-indexed

n = int(input())
arr = [int(i) for i in input().split()]
t = [0 for _ in range(4*n)]
def build(a, v, tl, tr):
  if (tl == tr):
    t[v] = a[tl]
  else:
    tm = (tl + tr) // 2
    build(a, v*2, tl, tm)
    build(a, v*2+1, tm+1, tr)
    t[v] = max(t[v*2], t[v*2+1])

def query(v, tl, tr, l, r):
  if l > r:
    return 0
  if l == tl and r == tr:
    return t[v]
  tm = (tl + tr) // 2
  return max(query(v*2, tl, tm, l, min(r, tm)), query(v*2+1, tm+1, tr, max(l, tm+1), r))


def update(v, tl, tr, pos, new_val):
  if tl == tr:
    t[v] = new_val
  else:
    tm = (tl + tr) // 2
    if pos <= tm:
      update(v*2, tl, tm, pos, new_val)
    else:
      update(v*2+1, tm+1, tr, pos, new_val)
    t[v] = max(t[v*2], t[v*2+1])

def first_greater(v, lv, rv, l, r, x): 
  if lv > r or rv < l:
    return -1
  if l <= lv and rv <= r:
    if t[v] <= x:
      return -1
    while lv != rv:
      mid = lv + (rv-lv) // 2
      if t[2*v] > x:
        v = 2*v
        rv = mid
      else:
        v = 2*v+1
        lv = mid +1
    return lv
  mid = lv +(rv-lv) // 2
  rs = first_greater(2*v, lv, mid, l, r, x)
  if rs != -1:
    return rs
  return first_greater(2*v+1, mid+1, rv, l, r, x)


build(arr, 1, 0, n-1)
print(first_greater(1, 0, n-1, 2, n-1, 0))



 #---------------------------------------------------   



#same as above but min 
n = int(input())
arr = [int(i) for i in input().split()]
t = [0 for _ in range(4*n)]
def build(a, v, tl, tr):
  if (tl == tr):
    t[v] = a[tl]
  else:
    tm = (tl + tr) // 2
    build(a, v*2, tl, tm)
    build(a, v*2+1, tm+1, tr)
    t[v] = max(t[v*2], t[v*2+1])

def query(v, tl, tr, l, r):
  if l > r:
    return 0
  if l == tl and r == tr:
    return t[v]
  tm = (tl + tr) // 2
  return max(query(v*2, tl, tm, l, min(r, tm)), query(v*2+1, tm+1, tr, max(l, tm+1), r))


def update(v, tl, tr, pos, new_val):
  if tl == tr:
    t[v] = new_val
  else:
    tm = (tl + tr) // 2
    if pos <= tm:
      update(v*2, tl, tm, pos, new_val)
    else:
      update(v*2+1, tm+1, tr, pos, new_val)
    t[v] = max(t[v*2], t[v*2+1])

    
 #---------------------------------------------------   


#Sparse table for minimum on a segment (without updates, O(1) queries O(nlog(n)) build; inclusive intervals
import math
def buildSparseTable(arr, n):
    for i in range(0, n):
        lookup[i][0] = arr[i]
    j = 1
    while (1 << j) <= n:
        i = 0
        while (i + (1 << j) - 1) < n:
            if (lookup[i][j - 1] <
                lookup[i + (1 << (j - 1))][j - 1]):
                lookup[i][j] = lookup[i][j - 1]
            else:
                lookup[i][j] = lookup[i + (1 << (j - 1))][j - 1]
            i += 1
        j += 1       
 
# Returns minimum of arr[L..R] in constant time 
def query(L, R):
    j = int(math.log2(R - L + 1))
    if lookup[L][j] <= lookup[R - (1 << j) + 1][j]:
        return lookup[L][j]
    else:
        return lookup[R - (1 << j) + 1][j]
"""