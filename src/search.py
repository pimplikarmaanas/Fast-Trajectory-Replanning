from collections import defaultdict

from graph_util import *
import heapq
import time

ADAPTIVE_HEURISTIC_DICT = "adaptive_h"
SEARCH_SUCCESSFUL, SEARCH_FAILED = 1, 0

class Search:
    def __init__(self):
        pass

    def __get_neighbors(self, g: Graph, c: Cell):
        x, y, res = c.position[0], c.position[1], []
        # left
        if x-1 >= 0:
            res.append(g.get_cell((x-1, y)))
        # right
        if x+1 < g.get_dim():
            res.append(g.get_cell((x+1, y)))
        # down
        if y+1 < g.get_dim():
            res.append(g.get_cell((x, y+1)))
        # up
        if y-1 >= 0:
            res.append(g.get_cell((x, y-1)))

        return res

    def __heuristic(self, start: Cell, end: Cell, **kwargs):
        adaptive_h = kwargs.get(ADAPTIVE_HEURISTIC_DICT, None)
        if adaptive_h:
            return adaptive_h[start]

        # manhattan distance
        x1, y1 = start.position[0], start.position[1]
        x2, y2 = end.position[0], end.position[1]

        return abs(x1-x2) + abs(y1-y2)

    def __compute_f(self, cur: Cell, goal: Cell, **kwargs):
        adaptive_h = kwargs.get(ADAPTIVE_HEURISTIC_DICT, None)
        if adaptive_h:
            cur.set_h(self.__heuristic(cur, goal, ADAPTIVE_HEURISTIC_DICT=adaptive_h))
            return cur.get_g() + cur.get_h()

        cur.set_h(self.__heuristic(cur, goal))
        return cur.get_g() + cur.get_h()

    def A_star(self, maze: Graph, start_t: tuple, goal_t: tuple, known_blocks: set, **kwargs):
        start, goal = Cell(position=start_t), Cell(position=goal_t)
        adaptive_h = kwargs.get(ADAPTIVE_HEURISTIC_DICT, None)

        # start and goal are tuples (i, j)
        open_list, closed_list = [start], known_blocks.copy()
        expanded_nodes = 0

        while open_list:
            expanded_nodes += 1
            cur_node = heapq.heappop(open_list)
            closed_list.add(cur_node)

            # terminating condition
            if cur_node == goal:
                path = []

                while cur_node:
                    path.append(cur_node)
                    cur_node = cur_node.get_parent()

                # backtrack
                return SEARCH_SUCCESSFUL, path[::-1], expanded_nodes

            neighbors = self.__get_neighbors(maze, cur_node)

            for child in neighbors:
                child.set_g(cur_node.get_g() + 1)
                if adaptive_h:
                    child.set_f(self.__compute_f(child, goal, ADAPTIVE_HEURISTIC_DICT=adaptive_h))
                else:
                    child.set_f(self.__compute_f(child, goal))

                if child in closed_list:
                    continue

                child.set_parent(cur_node)

                if child in open_list:
                    index = open_list.index(child)
                    if child < open_list[index]:
                        open_list.pop(index)
                    else:
                        continue

                heapq.heappush(open_list, child)

        return SEARCH_FAILED, None, 0

    def repeated_A_star(self, maze: Graph, start_t: tuple, goal_t: tuple):
        start, goal = maze[start_t], maze[goal_t]

        cur = start
        path_taken = [start]
        known_blocks = set()
        expanded_nodes = 0

        while cur != goal:
            status, path, cur_expanded = self.A_star(maze, cur.position, goal_t, known_blocks)
            if status == SEARCH_FAILED:
                return None, None

            expanded_nodes += cur_expanded

            i = 1
            while i < len(path) and not path[i].is_blocked():
                cur = path[i]
                path_taken.append(cur)
                i += 1

            if i < len(path) and path[i].is_blocked():
                known_blocks.add(path[i])

        return path_taken, expanded_nodes

    def adaptive_A_star(self, maze: Graph, start_t: tuple, goal_t: tuple):
        adaptive_dict = defaultdict(int)
        start, goal = maze[start_t], maze[goal_t]

        cur = start
        path_taken = [start]
        known_blocks = set()
        expanded_nodes = 0

        while cur != goal:
            status, path, expanded = self.A_star(maze, cur.position, goal_t, known_blocks, ADAPTIVE_HEURISTIC_DICT=adaptive_dict)
            if status == SEARCH_FAILED:
                return None, None

            _, start_goal_path, _ = self.A_star(maze, start_t, goal_t, known_blocks, ADAPTIVE_HEURISTIC_DICT=adaptive_dict)
            for i, node in enumerate(path):
                start_s_path = len(path) - i - 1
                adaptive_dict[node] = len(start_goal_path) - start_s_path

            expanded_nodes += expanded

            i = 1
            while i < len(path) and not path[i].is_blocked():
                cur = path[i]
                path_taken.append(cur)
                i += 1

            if i < len(path) and path[i].is_blocked():
                known_blocks.add(path[i])

        return path_taken, expanded_nodes
