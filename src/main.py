from graph_util import *
from search import *
import sys, time

# main file
sys.setrecursionlimit(12000)

def get_random_pos():
    dim = TEST_GRAPH_DIM
    return random.randint(0, dim-1), random.randint(0, dim-1)

if __name__ == "__main__":
    m = Maze()
    s = Search()

    test_graphs = m.get_testing_graphs(count=20)
    start_t = time.perf_counter()

    avg_node_imp, avg_time_imp = 0, 0
    paths_found = 0

    set_test_dim(20)

    for graph in test_graphs:
        c_start, c_goal = get_random_pos(), get_random_pos()

        print(f"############# GRAPH {graph.get_label()}")
        repeated_path1, num_expanded1, duration1 = s.repeated_A_star(graph, c_start, c_goal)
        if not repeated_path1:
            print("Path not found using repeated A*...\n")
            continue
        # print(f"Found a path! Time taken: {duration1}")
        # print(f"Path: {repeated_path1}")

        repeated_path2, num_expanded2, duration2 = s.adaptive_A_star(graph, c_start, c_goal)
        if not repeated_path2:
            print("Path not found using adaptive A*...\n")
            continue
        # print(f"Found a path! Time taken: {duration2}")
        # print(f"Path: {repeated_path2}")

        time_imp, node_imp = (duration1 - duration2)/duration1, (num_expanded1 - num_expanded2)/num_expanded1
        print(f"Adaptive A* expanded {node_imp: .2%} less nodes and improved time by {time_imp: .2%}\n")
        paths_found += 1
        avg_node_imp += node_imp
        avg_time_imp += time_imp

    end_t = time.perf_counter()
    print(f"Time taken to complete all path test cases: {end_t - start_t}")
    if paths_found:
        avg_node_imp /= paths_found
        avg_time_imp /= paths_found
        print(f"On average, Adaptive A* expanded {avg_node_imp: .2%} less nodes and improved time by {time_imp: .2%}")


    '''
    g = Graph(1, 5)
    g[(1, 2)].set_blocked(True)
    g[(2, 2)].set_blocked(True)
    g[(3, 2)].set_blocked(True)
    g[(2, 3)].set_blocked(True)
    g[(3, 3)].set_blocked(True)
    g[(4, 3)].set_blocked(True)
    '''