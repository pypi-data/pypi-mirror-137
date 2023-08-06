#Segment tree for sum; 0-indexed; all intervals are inclusive
import math
class SegmentTreeSum:
    def __init__(self, n, arr):
        self.t = [0 for _ in range(4*n)]
        self.n = n
        self.arr = arr
        self.build(arr, 1, 0, n-1)

    def build(self, a, v, tl, tr):
        if (tl == tr):
            self.t[v] = a[tl]
        else:
            tm = (tl + tr) // 2
            self.build(a, v*2, tl, tm)
            self.build(a, v*2+1, tm+1, tr)
            self.t[v] = self.t[v*2] + self.t[v*2+1]

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
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
    
    
#Segment tree for max; also has find first element greater than x query; inclusive and 0-indexed
class SegmentTreeMax:
    def __init__(self, n, arr):
        self.t = [0 for _ in range(4*n)]
        self.n = n
        self.arr = arr
        self.build(arr, 1, 0, n-1)
    def build(self, a, v, tl, tr):
        if (tl == tr):
            self.t[v] = a[tl]
        else:
            tm = (tl + tr) // 2
            self.build(a, v*2, tl, tm)
            self.build(a, v*2+1, tm+1, tr)
            self.t[v] = max(self.t[v*2], self.t[v*2+1])

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
        tm = (tl + tr) // 2
        return max(self.query(v*2, tl, tm, l, min(r, tm)), self.query(v*2+1, tm+1, tr, max(l, tm+1), r))


    def update(self, v, tl, tr, pos, new_val):
        if tl == tr:
            self.t[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, new_val)
            else:
                self.update(v*2+1, tm+1, tr, pos, new_val)
                self.t[v] = max(self.t[v*2], self.t[v*2+1])
    def first_greater(self,v, lv, rv, l, r, x): 
        if lv > r or rv < l:
            return -1
        if l <= lv and rv <= r:
            if self.t[v] <= x:
                return -1
            while lv != rv:
                mid = lv + (rv-lv) // 2
                if self.t[2*v] > x:
                    v = 2*v
                    rv = mid
                else:
                    v = 2*v+1
                    lv = mid +1
            return lv
        mid = lv +(rv-lv) // 2
        rs = self.first_greater(2*v, lv, mid, l, r, x)
        if rs != -1:
            return rs
        return self.first_greater(2*v+1, mid+1, rv, l, r, x)


#same as above but min 
class SegmentTreeMin:
    def __init__(self, n, arr):
        self.t = [0 for _ in range(4*n)]
        self.n = n
        self.arr = arr
        self.build(arr, 1, 0, n-1)

    def build(self, a, v, tl, tr):
        if (tl == tr):
            self.t[v] = a[tl]
        else:
            tm = (tl + tr) // 2
            self.build(a, v*2, tl, tm)
            self.build(a, v*2+1, tm+1, tr)
            self.t[v] = max(self.t[v*2], self.t[v*2+1])

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.t[v]
        tm = (tl + tr) // 2
        return max(self.query(v*2, tl, tm, l, min(r, tm)), self.query(v*2+1, tm+1, tr, max(l, tm+1), r))


    def update(self, v, tl, tr, pos, new_val):
        if tl == tr:
            self.t[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, new_val)
            else:
                self.update(v*2+1, tm+1, tr, pos, new_val)
                self.t[v] = max(self.t[v*2], self.t[v*2+1])

    

#Sparse table for minimum on a segment (without updates, O(1) queries O(nlog(n)) build; inclusive intervals
class SparseTable:
    def __init__(self, arr, n):
        self.lookup = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(0, n):
            self.lookup[i][0] = arr[i]
        j = 1
        while (1 << j) <= n:
            i = 0
            while (i + (1 << j) - 1) < n:
                if (self.lookup[i][j - 1] <
                    self.lookup[i + (1 << (j - 1))][j - 1]):
                    self.lookup[i][j] = self.lookup[i][j - 1]
                else:
                    self.lookup[i][j] = self.lookup[i + (1 << (j - 1))][j - 1]
                i += 1
            j += 1       
    #Returns minimum of arr[L..R] in constant time 
    def query(self, L, R):
        j = int(math.log2(R - L + 1))
        if self.lookup[L][j] <= self.lookup[R - (1 << j) + 1][j]:
            return self.lookup[L][j]
        else:
            return self.lookup[R - (1 << j) + 1][j]