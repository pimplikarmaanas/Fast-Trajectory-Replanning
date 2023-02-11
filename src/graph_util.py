import random
from typing import NewType

class cell:
    def __init__(self):
        self.__blocked = False

    def __str__(self):
        return str(self.__blocked)

    def set_blocked(self, status: bool):
        self.__blocked = status

class graph:
    def __init__(self, len: int):
        self.__graph = []
        for i in range(len):
            self.__graph.append([])
            for j in range(len):
                self.__graph[i].append(cell())
    
    def __str__(self):
        res = ""
        for i in range(len(self.__graph)):
            for j in range(len(self.__graph[i])):
                res += f"|{self.__graph[i][j]}| "
            res += "\n"
        return res

    def __getitem__(self, cell: tuple):
        row, col = cell[0], cell[1]
        return self.__graph[row][col]
    
    def __setitem__(self, cell: tuple, val: cell):
        row, col = cell[0], cell[1]
        slef.__graph[row][col] = val
    
    def get_dim(self):
        return len(self.__graph)

class search:
    def __init__(self):
        pass

    # private helper function used in get_random_graph
    def __flood_fill(self, g: graph, cell: tuple, visited: set):
        def get_neighbors(cell: tuple):
            x, y, res = cell[0], cell[1], []
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if(i != x and j != y and -1 < i < g.get_dim() and -1 < j < g.get_dim()
                        and (i, j) not in visited):
                        res.append((i, j))
            return res
        
        neighbors = get_neighbors(cell)
        if not neighbors:
            return

        # add more code
        # needs to recursively call itself until the given cell's neighbor list is empty

    # returns a randomly initialized graph of size
    def get_random_graph(self, *, dim: int=None):
        # to make it insanely clear that the dimensions of the graph is whats being passed as the param
        if not dim:
            raise Exception("No dimension entered. Pass the dimension of the graph as a keyword parameter \"dim\".")

        g = graph(dim)

        available_cells = []
        # adding all possible cells to the list
        for i in range(dim):
            for j in range(dim):
                available_cells.append((i,j))
        
        visited = set()
        while available_cells:
            chosen_cell = random.choice(available_cells) # randomly chosen cell

            # mark as visited and remove from list
            visited.add(chosen_cell)
            available_cells.remove(chosen_cell)
            
            g[(chosen_cell)].set_blocked(False)

            self.__flood_fill(g, chosen_cell, visited)

            # dont remove or infinite loop for now
            break

        return g

    def forward_a(self, graph, initial, goal):
        pass

    def backward_a(self, graph, initial, goal):
        pass