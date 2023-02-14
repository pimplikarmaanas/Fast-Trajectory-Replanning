from graph_util import *
from search import *
import sys, time

# main file
sys.setrecursionlimit(12000)

if __name__ == "__main__":
    m = Maze()
    # test_graphs = m.get_testing_graphs(count=50)

    g = Graph(1, 5)
    g[(1, 2)].set_blocked(True)
    g[(2, 2)].set_blocked(True)
    g[(3, 2)].set_blocked(True)
    g[(2, 3)].set_blocked(True)
    g[(3, 3)].set_blocked(True)
    g[(4, 3)].set_blocked(True)
    
    s = Search()
    repeated_path = s.repeated_A_star(g, (4, 2), (4, 4))
    print(repeated_path)