from graph_util import Graph, Cell, Search
import sys, time

# main file
sys.setrecursionlimit(12000)

if __name__ == "__main__":
    s = Search()
    test_graphs = s.get_testing_graphs(count=50)