from graph_util import *
import heapq

class Wrapper:
    def __init__(self, cord: tuple, f: int):
        self.__cord = cord
        self.__f = f

    def get_cord(self):
        return self.__cord

    def get_f(self):
        return self.__f
    
    def __hash__(self):
        return hash(self.__cord)

    def __lt__(self, other):
        return self.__f < other.get_f()
    
    def __eq__(self, other):
        return self.__cord == other.__cord

class Search:
    def __init__(self):
        pass

    def __get_neighbors(self, maze: Maze, cell: tuple):
        x, y, res = cell[0], cell[1], []
        # left
        if x-1 >= 0 and (x-1, y):
            res.append((x-1, y))
        # right
        if x+1 < maze.get_dim():
            res.append((x+1, y))
        # down
        if y+1 < maze.get_dim():
            res.append((x, y+1))
        # up
        if y-1 >= 0:
            res.append((x, y-1))

        return res

    def __heuristic(self, start: tuple, end: tuple):
        # manhattan distance
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]

        return abs(x1-x2) + abs(y1-y2)

    def __compute_f(self, g: int, cur: tuple, goal: tuple):
        return (g + 1) + self.__heuristic(cur, goal)

    def A_star(self, maze: Maze, start: tuple, goal: tuple):
        # start and goal are tuples (i, j)
        path = []
        open_list, closed_list = [Wrapper(start, 0)], set()

        while open_list:
            cur_node = heapq.heappop(open_list)
            closed_list.add(cur_node.get_cord())

            path.append(cur_node.get_cord())
            g = len(path) + 1

            # terminating condition
            if cur_node.get_cord() == goal:
                print("Reached goal!")
                return g, path
            
            neighbors = self.__get_neighbors(maze, cur_node.get_cord())
            
            print(f"neighbors of {cur_node.get_cord()} are {neighbors}")
            for child in neighbors:
                if child in closed_list:
                    continue

                child_f = self.__compute_f(g, child, goal)
                child_wrapper = Wrapper(child, child_f)

                if child_wrapper in set(open_list):
                    index = open_list.index(child_wrapper)
                    if child_wrapper.get_f() < open_list[index].get_f():
                        open_list.pop(index)
                    else:
                        continue

                print(f"Adding {child_wrapper.get_cord()}")
                heapq.heappush(open_list, child_wrapper)
        
        print("Could not reach goal...")
        return g, path

    