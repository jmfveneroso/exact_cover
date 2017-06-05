# coding: utf8

"""Implementação do problema das N rainhas com base no algoritmo descrito por Dijkstra
em Structured Programming (1972).
"""

class BacktrackingQueens:
  def __init__(self, n, silent = True):
    self.n = n
    self.y = [None] * n            # Índice da rainha na coluna.
    self.row = [0] * n             # Array booleano das linhas.
    self.up =  [0] * (2 * n - 1)   # Array booleano das diagonais principais. 
    self.down = [0] * (2 * n - 1)  # Array booleano das diagonais secundárias. 
    self.num_found = 0             # Numero de soluções encontradas.
    self.silent = silent           # Não imprime as soluções se for verdadeiro.
    self.subproblems = 0           # Número de subproblemas resolvidos.

  def safe(self, x, y):
    return not self.row[y] and not self.up[x-y] and not self.down[x+y]

  def place(self, x, y):
    self.y[x] = y
    self.row[y] = 1
    self.up[x-y] = 1
    self.down[x+y] = 1

  def remove(self, x, y):
    self.y[x] = None
    self.row[y] = 0
    self.up[x-y] = 0
    self.down[x+y] = 0

  # Recursão principal.
  def solve(self, x = 0):
    self.subproblems = self.subproblems + 1
    if (x == self.n):
      self.display()

    for y in range(self.n):
      if self.safe(x, y):
        self.place(x, y)
        self.solve(x + 1)
        self.remove(x, y)

  def display(self):
    self.num_found = self.num_found + 1
    if self.silent:
      return
    print '+-' + '--' * self.n + '+'
    for y in range(self.n-1, -1, -1):
      print '|',
      for x in range(self.n):
        if self.y[x] == y:
          print "Q",
        else:
          print ".",
      print '|'
    print '+-' + '--'*self.n + '+'

def main():
  import sys
  import time
  silent = 0
  n = 8

  if sys.argv[1:2] == ['-n']:
    silent = 1
    del sys.argv[1]

  if sys.argv[1:]:
    n = int(sys.argv[1])

  q = BacktrackingQueens(n)
  q.silent = silent

  t0 = time.time()
  q.solve()
  ms = (time.time() - t0) * 1000
  print "Encontradas", q.num_found, "soluções", "em", ms, "ms."
  print "Resolvidos", q.subproblems, "subproblemas.", 

if __name__ == "__main__":
  main()
