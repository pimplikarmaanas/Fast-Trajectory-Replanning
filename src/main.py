from graph_util import *
from search import *
import sys, time

# main file
sys.setrecursionlimit(12000)

if __name__ == "__main__":
    m = Maze()
    s = Search()

    test_graphs = m.get_testing_graphs(count=5)
    start_t = time.perf_counter()

    for graph in test_graphs:
        print(f"############# GRAPH {graph.get_label()}")
        repeated_path1, num_expanded1 = s.repeated_A_star(graph, (0, 0), (4, 4))
        print(graph)
        if not repeated_path1:
            print("Path not found using repeated A*...\n")
            continue

        print(repeated_path1)

    end_t = time.perf_counter()
    print(f"Time taken to complete all path test cases: {end_t - start_t}")

    '''
    # TESTING GRAPH THATS SHOWN IN THE ASSIGNMENT PDF
    g = Graph(1, 5)
    g.set_cell_status((1, 2), True)
    g.set_cell_status((2, 2), True)
    g.set_cell_status((3, 2), True)
    g.set_cell_status((2, 3), True)
    g.set_cell_status((3, 3), True)
    g.set_cell_status((4, 3), True)
    print(g)
    '''