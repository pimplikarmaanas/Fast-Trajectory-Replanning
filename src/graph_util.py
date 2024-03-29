import multiprocessing
import random
import sys
import inspect
import time

# default dimensions of a graph generated by generate_graph
TEST_GRAPH_DIM = 101

class Cell:
    def __init__(self, parent=None, position=None):
        self.position = position

        self.__blocked = False
        self.__f, self.__g, self.__h = 0, 0, 0

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return str(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        if self.__f == other.get_f():
            return self.__g > other.get_g()
        return self.__f < other.get_f()

    def __hash__(self):
        return hash(self.position)

    def set_f(self, new_f):
        self.__f = new_f

    def set_g(self, new_g):
        self.__g = new_g

    def set_h(self, new_h):
        self.__h = new_h

    def get_f(self):
        return self.__f

    def get_g(self):
        return self.__g

    def get_h(self):
        return self.__h

    def set_blocked(self, status: bool):
        self.__blocked = status

    def is_blocked(self):
        return self.__blocked

class Graph:
    def __init__(self, label: int, len: int):
        self.label = label
        self.__len = len
        self.__graph = []
        for i in range(len):
            row = []
            for j in range(len):
                row.append(Cell(position=(i, j)))
            self.__graph.append(row)

    def __str__(self):
        res = ""
        for i in range(len(self.__graph)):
            for j in range(len(self.__graph[i])):
                if self.__graph[i][j].is_blocked():
                    res += u"{\u25A0}"
                else:
                    res += u" \u25A0 "
            res += "\n"
        return res

    def __getitem__(self, cell: tuple):
        row, col = cell[0], cell[1]
        return self.__graph[row][col]
    
    def __setitem__(self, cell: tuple, val: Cell):
        row, col = cell[0], cell[1]
        self.__graph[row][col] = val
    
    def get_dim(self):
        return len(self.__graph)
    
    def get_label(self):
        return self.label

    def get_cell(self, cell_t: tuple):
        i, j = cell_t[0], cell_t[1]
        return self.__graph[i][j]

    def set_cell_status(self, cell: tuple, status: bool):
        row, col = cell[0], cell[1]
        self.__graph[row][col].set_blocked(status)

class Maze:
    def __init__(self):
        pass

    # private helper function used in get_random_graph
    def __flood_fill(self, g: Graph, cell: Cell, visited: set):
        def random_status():
            r = random.randint(1, 100)
            return True if r <= 25 else False

        def get_neighbors(c: Cell):
            x, y, res = c.position[0], c.position[1], []
            # left
            if x-1 >= 0 and g[(x-1, y)] not in visited:
                res.append(g[(x-1, y)])
            # right
            if x+1 < g.get_dim() and g[(x+1, y)] not in visited:
                res.append(g[(x+1, y)])
            # down
            if y+1 < g.get_dim() and g[(x, y+1)] not in visited:
                res.append(g[(x, y+1)])
            # up
            if y-1 >= 0 and g[(x, y-1)] not in visited:
                res.append(g[(x, y-1)])

            return res
        
        neighbors = get_neighbors(cell)
        if not neighbors:
            return

        for c in neighbors:
            cord = (c.position[0], c.position[1])
            g.set_cell_status(cord, random_status())

            visited.add(c)
            self.__flood_fill(g, c, visited)

    # returns a randomly initialized graph with the passed in label and optional argument "dim"
    def generate_graph(self, label: int, dim=TEST_GRAPH_DIM):
        g = Graph(label, dim)

        start_t = time.perf_counter()

        available_cells = []
        # adding all possible cells to the list
        for i in range(dim):
            for j in range(dim):
                available_cells.append(Cell(position=(i, j)))
        
        visited = set()
        while available_cells:
            chosen_cell = random.choice(available_cells) # randomly chosen cell

            # mark as visited and remove from list
            visited.add(chosen_cell)
            available_cells.remove(chosen_cell)

            c_i, c_j = chosen_cell.position[0], chosen_cell.position[1]
            g.set_cell_status((c_i, c_j), False)

            self.__flood_fill(g, chosen_cell, visited)
            available_cells = list(set(available_cells) - visited)

        end_t = time.perf_counter()
        return g, end_t - start_t            

    def get_testing_graphs(self, *, count: int):
        graphs = []
        start_t = time.perf_counter()

        for i in range(count):
            cur_graph, _ = self.generate_graph(label=i)
            graphs.append(cur_graph)

        end_t = time.perf_counter()
        time_taken = end_t - start_t
        print(f"All graphs generated in {time_taken} seconds.")
        return graphs
