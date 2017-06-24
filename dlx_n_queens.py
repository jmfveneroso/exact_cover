# coding: utf8
import math
import numpy as np

class Cell(object):
  def __init__(self):
    self.U = self.D = self.L = self.R = self
    self.C = None

class HeaderCell(Cell):
  def __init__(self, name):
    super(HeaderCell, self).__init__()
    self.size = 0
    self.name = name

class DlxQueens:
  def __init__(self, n, s_heuristic = False, m_heuristic = False):
    self.n = n
    self.s_heuristic = s_heuristic
    self.header = HeaderCell("H")
    self.nrows = self.ncols = 0
    self.col_list = []
    self.priority = {}
    self.create_column_headers()
    self.create_columns()
    self.solution = {}
    self.num_solutions = 0
    self.subproblems = 0
    self.hidden_cols = 0
    self.hidden_rows = 0
    self.m_heuristic = m_heuristic
    self.values = []
    self.avg = []
    self.sd = []

    for i in range(self.n):
      self.values.append([])
      self.avg.append([])
      self.sd.append([])

  def create_column_headers(self):
    prev = self.header
    for i in range(6 * self.n - 2):
      primary = False
      if i < 2 * self.n:
        primary = True

      cell = HeaderCell(i)
      self.col_list.append(cell)
      if primary:
        prev.R = cell
        cell.L = prev
        prev = cell
      self.ncols += 1

    prev.R = self.header
    self.header.L = prev

  def create_columns(self):
    for i in range(self.n):
      self.priority[i] = abs(i - (self.n - 1) / 2)
      self.priority[self.n + i] = abs(i - self.n - (self.n - 1) / 2)

    for i in range(self.n):
      for j in range(self.n):
        # Linha, coluna, diagonal primária e diagonal secundária.
        row = [i, self.n + j, 2 * self.n + i + j, 5 * self.n - 2 - i + j]
        self.add_row(row)
    self.col_list = None

  def add_row(self, row):
    prev = None
    start = None

    row = sorted(row)

    for ind in row:
      cell = Cell()

      if prev:
        prev.R = cell
        cell.L = prev
      else:
        start = cell

      col = self.col_list[ind]

      last = col.U
      last.D = cell
      cell.U = last
      col.U = cell
      cell.D = col
      cell.C = col
      col.size += 1
      prev = cell

    start.L = cell
    cell.R = start
    self.nrows += 1

  def cover(self, c):
    c.R.L = c.L
    c.L.R = c.R
    self.hidden_cols += 1
    i = c.D
    while i is not c:
      j = i.R
      self.hidden_rows += 1
      while j is not i:
        j.D.U = j.U
        j.U.D = j.D
        j.C.size -= 1
        j = j.R
      i = i.D

  def uncover(self, c):
    i = c.U
    while i is not c:
      j = i.L
      self.hidden_rows -= 1
      while j is not i:
        j.C.size += 1
        j.D.U = j.U.D = j
        j = j.L
      i = i.U
    c.R.L = c.L.R = c
    self.hidden_cols -= 1

  def min_column(self):
    col = self.header.R

    col_min = col
    while col is not self.header:
      if col.size < col_min.size:
        col_min = col
      col = col.R

    col = self.header.R
    max_priority_col = col_min
    while col is not self.header:
      if col.size == col_min.size:
        if self.priority[col.name] < self.priority[max_priority_col.name]:
          max_priority_col = col
      col = col.R

    return max_priority_col

  def search(self, k):
    self.subproblems = self.subproblems + 1


    ### NEW
    # arr = [0,42,25,16,8,4,2,1,0]
    # col = self.header.R
    # num_positioned = 0
    # while col is not self.header:
    #   num_positioned += 1
    #   col = col.R
    # num_positioned = self.n - num_positioned / 2
    # # if num_positioned > 6:

    # # print num_positioned, self.hidden_cols, self.hidden_rows
    # arr = []
    # threshold = self.n ** 2
    # arr.append(0)
    # for i in range(self.n):
    #   x = self.n - i
    #   if (threshold < 4): 
    #     threshold = 0
    #   else: 
    #     threshold -= (3 * math.sqrt(threshold) - 2)
    #   arr.append(threshold)
    # threshold = arr[num_positioned]
    # 
    # if (k == 2):
    #   print self.n ** 2 - self.hidden_rows, threshold

    # if (self.n ** 2 - self.hidden_rows < 1 *  threshold):
    #   # print 64 - self.hidden_rows, threshold
    #   return
    # if (64 - self.hidden_rows < arr[num_positioned]):
    #   print 64 - self.hidden_rows, arr[num_positioned]
    #   return
    ### NEW


    if self.header.R == self.header:
      self.num_solutions += 1
      return

    if self.s_heuristic:
      col = self.min_column()
    else:
      col = self.header.R

    self.cover(col)

    row = col.D
    while row is not col:
      self.solution[k] = row
      j = row.R

      while j is not row:
        self.cover(j.C)
        j = j.R

      if self.m_heuristic:
        if len(self.values[k - 1]) < 1000:
          self.values[k - 1].append(self.hidden_rows)
          self.avg[k - 1] = np.mean(self.values[k - 1])
          self.sd[k - 1] = np.std(self.values[k - 1])
        if (k < 0 or self.hidden_rows <= self.avg[k - 1] + 1 * self.sd[k - 1]):
          self.search(k + 1)
      else:
        self.search(k + 1)

      row = self.solution[k]
      col = row.C
      j = row.L
      while j is not row:
          self.uncover(j.C)
          j = j.L
      row = row.D

    self.uncover(col)

def main():
  import sys
  import time
  n = 8

  s_heuristic = False
  m_heuristic = False

  if sys.argv[1:]:
    n = int(sys.argv[1])

  if sys.argv[2:]:  
    s_heuristic = int(sys.argv[2])

  if sys.argv[3:]:  
    m_heuristic = int(sys.argv[3])

  d = DlxQueens(n, s_heuristic, m_heuristic)

  t0 = time.time()
  d.search(0)
  ms = (time.time() - t0) * 1000

  print "Encontradas", d.num_solutions, "soluções", "em", ms, "ms."
  print "Resolvidos", d.subproblems, "subproblemas."
  print "Efficiency:", d.num_solutions / float(d.subproblems)

if __name__ == "__main__":
  main()
