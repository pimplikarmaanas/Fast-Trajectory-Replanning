from graph_util import *
from search import *
import sys, time

# main file
sys.setrecursionlimit(12000)

if __name__ == "__main__":
    # m = Maze()
    # test_graphs = m.get_testing_graphs(count=50)
    s = Search()

    g = Graph(1, 5)
    cost, path = s.A_star(g, (0, 0), (4, 4))
    print(path)
    print("costs: ", cost)