from graph_util import *
import heapq

class Wrapper:
    def __init__(self, cord: tuple, g: int, f: int):
        self.__total_cost = g
        self.__cord = cord
        self.__f = f
        self.__parent = None

    def get_cord(self):
        return self.__cord

    def get_f(self):
        return self.__f

    def get_g(self):
        return self.__total_cost

    def get_parent(self):
        return self.__parent
    
    def set_parent(self, parent):
        self.__parent = parent

    def __hash__(self):
        return hash(self.__cord)

    def __lt__(self, other):
        return self.__f < other.get_f()
    
    def __eq__(self, other):
        return self.__cord == other.__cord

class Search:
    def __init__(self):
        pass

    def __get_neighbors(self, maze: Graph, cell: tuple):
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
        return (g + 1), (g + 1) + self.__heuristic(cur, goal)

    def A_star(self, maze: Graph, start: tuple, goal: tuple, known_blocks: set):
        # start and goal are tuples (i, j)
        open_list, closed_list = [Wrapper(start, 0, 0)], known_blocks.copy()
        
        while open_list:
            cur_node = heapq.heappop(open_list)

            closed_list.add(cur_node.get_cord())
            cur_g = cur_node.get_g()

            # terminating condition
            if cur_node.get_cord() == goal:
                path = []

                while cur_node:
                    path.append(cur_node.get_cord())
                    cur_node = cur_node.get_parent()

                # backtrack
                return path[::-1]
            
            neighbors = self.__get_neighbors(maze, cur_node.get_cord())
            
            for child in neighbors:
                child_g, child_f = self.__compute_f(cur_node.get_g(), child, goal)

                child_wrapper = Wrapper(child, child_g, child_f)
                child_wrapper.set_parent(cur_node)

                if child in closed_list:
                    continue

                if child_wrapper in open_list:
                    index = open_list.index(child_wrapper)
                    if child_wrapper.get_f() < open_list[index].get_f():
                        open_list.pop(index)
                    else:
                        continue

                heapq.heappush(open_list, child_wrapper)
        
        return None

    def repeated_A_star(self, maze: Graph, start: tuple, goal: tuple):
        cur = start
        path_taken = []
        known_blocks = set()
        
        while cur != goal:
            # print("Known blocks: ", known_blocks)
            path = self.A_star(maze, cur, goal, known_blocks)
            # print(f"currently on {cur}, projected path: {path}")

            if not path:
                print("Can't get to end state.")
                print("Path taken so far: ", path_taken)
                return None

            i = 1            
            while i < len(path) and not maze[path[i]].is_blocked():
                known_blocks.add(cur)
                cur = path[i]
                path_taken.append(cur)
                i += 1

            if i < len(path) and maze[path[i]].is_blocked():
                # print(f"Added {path[i]} to the known blocks")
                known_blocks.add(path[i])

        return path_taken