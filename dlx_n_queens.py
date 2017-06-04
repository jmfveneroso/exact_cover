import random
import numpy as np

class Algorithm_X:
    """
    Callable object implementing the Algorithm X.
    """

    def __init__(self, matrix, callback, choose_min=True):
        """
        Creates an Algorithm_X object that solves the problem
        encoded in matrix.
        :param matrix: The DL_Matrix instance.
        :param callback: The callback called on every solution. callback has to
                         be a function receiving a dict argument
                         {row_index: linked list of the row}, and can return a
                         bool value. The solver keeps going on until the
                         callback returns a True value.
        :param choose_min: If True, the column with the minimum number of 1s is
                           chosen at each iteration, if False a random column is
                           chosen.
        """
        self.sol_dict = {}
        self.stop = False
        self.matrix = matrix
        self.callback = callback
        self.choose_min = choose_min

    def __call__(self):
        # Start the search
        self._search(0)

    def _search(self, k):
        if self.matrix.header.R == self.matrix.header:
            # matrix is empty, solution found
            if self.callback(self._create_sol(k)):
                self.stop = True
            return

        if self.choose_min:
            col = self.matrix.min_column()
        else:
            col = self.matrix.random_column()

        # cover column col
        self.matrix.cover(col)
        row = col.D

        while row is not col:
            self.sol_dict[k] = row
            j = row.R

            # cover the columns pointed by the 1s in the chosen row
            while j is not row:
                self.matrix.cover(j.C)
                j = j.R

            self._search(k + 1)
            if self.stop:
                return

            # uncover columns
            row = self.sol_dict[k]
            col = row.C
            j = row.L
            while j is not row:
                self.matrix.uncover(j.C)
                j = j.L
            row = row.D

        self.matrix.uncover(col)

    def _create_sol(self, k):
        # creates a solution from the inner dict
        sol = {}
        for key, row in self.sol_dict.items():
            if key >= k:
                continue
            tmp_list = []
            start = row
            tmp_list.append(row.C.name)
            row = row.R
            while row is not start:
                tmp_list.append(row.C.name)
                row = row.R
            sol[row.indexes[0]] = tmp_list
        return sol










class CannotAddRowsError(Exception):
    pass


class EmptyDLMatrix(Exception):
    pass


class Cell:
    """
    Inner cell, storing 4 pointers to neighbors, a pointer to the column header
    and the indexes associated.
    """
    __slots__ = list("UDLRC") + ["indexes"]

    def __init__(self):
        self.U = self.D = self.L = self.R = self
        self.C = None
        self.indexes = None

    def __str__(self):
        return "Node: {}".format(self.indexes)


class HeaderCell(Cell):
    """
    Column Header cell, a special cell that stores also a name and a size
    member.
    """
    __slots__ = ["size", "name"]

    def __init__(self, name):
        super(HeaderCell, self).__init__()
        self.size = 0
        self.name = name


class DL_Matrix:
    """
    Dancing Links sparse matrix implementation.
    It stores a circular doubly linked list of 1s, and another list
    of column headers. Every cell points to its upper, lower, left and right
    neighbors in a circular fashion.
    """

    def __init__(self, columns):
        """
        Creates a DL_Matrix.
        :param columns: it can be an integer or an iterable. If columns is an
                        integer, columns columns are added to the matrix,
                        named C0,...,CN where N = columns -1. If columns is an
                        iterable, the number of columns and the names are
                        deduced from the iterable, else TypeError is raised.
                        The iterable may yield the names, or a tuple
                        (name,primary). primary is a bool value that is True
                        if the column is a primary one. If not specified, is
                        assumed that the column is a primary one.
        :raises TypeError, if columns is not a number neither an iterable.
        """
        self.header = HeaderCell("H")
        self.nrows = self.ncols = 0
        self.col_list = []
        self._create_column_headers(columns)

    def _create_column_headers(self, columns):
        if isinstance(columns, int):
            columns = int(columns)
            column_names = ("C{}".format(i) for i in range(columns))
        else:
            try:
                column_names = iter(columns)
            except TypeError:
                raise TypeError("Argument is not valid")

        prev = self.header
        # links every column in a for loop
        for name in column_names:
            if isinstance(name, tuple):
                name, primary = name
            else:
                primary = True
            cell = HeaderCell(name)
            cell.indexes = (-1, self.ncols)
            self.col_list.append(cell)
            if primary:
                prev.R = cell
                cell.L = prev
                prev = cell
            self.ncols += 1

        prev.R = self.header
        self.header.L = prev

    def add_sparse_row(self, row, already_sorted=False):
        """
        Adds a sparse row to the matrix. The row is in format
        [ind_0, ..., ind_n] where 0 <= ind_i < dl_matrix.ncols.
        If called after end_add is executed, CannotAddRowsError is raised.
        :param row: a sequence of integers indicating the 1s in the row.
        :param already_sorted: True if the row is already sorted,
                               default is False. Use it for performance
                               optimization.
        :raises CannotAddRowsError if end_add was already called.
        """
        if self.col_list is None:
            raise CannotAddRowsError()

        prev = None
        start = None

        if not already_sorted:
            row = sorted(row)

        for ind in row:
            cell = Cell()
            cell.indexes = (self.nrows, ind)

            if prev:
                prev.R = cell
                cell.L = prev
            else:
                start = cell

            col = self.col_list[ind]
            # link the cell with the previous one and with the right column
            # cells.
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

    def end_add(self):
        """
        Called when there are no more rows to be inserted. Not strictly
        necessary, but it can save some memory.
        """
        self.col_list = None

    def min_column(self):
        """
        Returns the column header of the column with the minimum number of 1s.
        :return: A column header.
        :raises: EmptyDLMatrix if the matrix is empty.
        """
        col = self.header.R
        if col is self.header:
            raise EmptyDLMatrix()

        col_min = col

        while col is not self.header:
            if col.size < col_min.size:
                col_min = col
            col = col.R

        return col_min

    def random_column(self):
        """
        Returns a random column header. (The matrix header is never returned)
        :return: A column header.
        :raises: EmptyDLMatrix if the matrix is empty.
        """
        col = self.header.R
        if col is self.header:
            raise EmptyDLMatrix()

        n = random.randint(0, self.ncols - 1)

        for _ in range(n):
            col = col.R

        if col == self.header:
            col = col.R
        return col

    def __str__(self):
        names = []
        m = np.zeros((self.nrows, self.ncols), dtype=np.uint8)
        col = self.header.R
        rows, cols = set(), []

        while col is not self.header:
            cols.append(col.indexes[1])
            names.append(col.name)
            cell = col.D
            while cell is not col:
                ind = cell.indexes
                rows.add(ind[0])
                m[ind] = 1
                cell = cell.D
            col = col.R

        m = m[list(rows)][:, cols]
        return "\n".join([", ".join(names), str(m)])

    def cover(self, c):
        """
        Covers the column c by removing the 1s in the column and also all
        the rows connected to them.
        :param c: The column header of the column that has to be covered.
        """
        # print("Cover column", c.name)
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
        """
        Uncovers the column c by readding the 1s in the column and also all
        the rows connected to them.
        :param c: The column header of the column that has to be uncovered.
        """
        # print("Uncover column", c.name)
        i = c.U
        while i is not c:
            j = i.L
            while j is not i:
                j.C.size += 1
                j.D.U = j.U.D = j
                j = j.L
            i = i.U
        c.R.L = c.L.R = c


#
# N-queens solver using Dancing Links.
#

def get_names(N):
    for i in range(N):
        yield "R{}".format(i)
    for i in range(N):
        yield "F{}".format(i)
    for i in range(2 * N - 1):
        yield "A{}".format(i), False  # secondary column
    for i in range(2 * N - 1):
        yield "B{}".format(i), False  # secondary column


def compute_row(i, j, N):
    # R is 0 .. N-1
    # F is N .. 2*N-1
    # A is 2*N .. 4*N - 2
    # B is 4*N - 1 .. 6*N - 3
    return [i, N + j, 2 * N + i + j, 5 * N - 2 - i + j]


class PrintFirstSol:
    def __init__(self, N):
        self.N = N

    def __call__(self, sol):
        pos = [0] * self.N
        for v in sol.values():
            v.sort()
            c, r = map(int, [v[2][1:], v[3][1:]])
            pos[r] = c
        for i in range(self.N):
            r = [" "] * self.N
            r[pos[i]] = "O"
            inner = "|".join(r)
            print("|{}|".format(inner))
        print()
        return True


class Print_Sol_Count:
    def __init__(self):
        self.count = 0

    def __call__(self, _):
        self.count += 1


if __name__ == "__main__":
    N = 13

    d = DL_Matrix(get_names(N))

    for i in range(N):
        for j in range(N):
            row = compute_row(i, j, N)
            d.add_sparse_row(row, already_sorted=True)
    d.end_add()

    p = PrintFirstSol(N)
    Algorithm_X(d, p)()
