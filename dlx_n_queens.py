# coding: utf8

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
  def __init__(self, n, s_heuristic = False):
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
        self.add_row(row, already_sorted=True)
    self.col_list = None

  def add_row(self, row, already_sorted=False):
    prev = None
    start = None

    if not already_sorted:
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
    i = c.D
    while i is not c:
      j = i.R
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
      while j is not i:
        j.C.size += 1
        j.D.U = j.U.D = j
        j = j.L
      i = i.U
    c.R.L = c.L.R = c

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
    # return col_min

  def search(self, k):
    self.subproblems = self.subproblems + 1

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

  if sys.argv[1:]:
    n = int(sys.argv[1])

  s_heuristic = False
  d = DlxQueens(n, s_heuristic)

  t0 = time.time()
  d.search(0)
  ms = (time.time() - t0) * 1000

  print "Encontradas", d.num_solutions, "soluções", "em", ms, "ms."
  print "Resolvidos", d.subproblems, "subproblemas.", 

if __name__ == "__main__":
  main()
