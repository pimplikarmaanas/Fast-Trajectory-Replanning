import runner
from graph_util import Graph

REPEATED_FORWARD_A_STAR = 0
REPEATED_BACKWARD_A_STAR = 0
ADAPTIVE_A_STAR = 0

def main():
    g = Graph(1, 5)
    g.set_cell_status((1, 2), True)
    g.set_cell_status((2, 2), True)
    g.set_cell_status((3, 2), True)
    g.set_cell_status((2, 3), True)
    g.set_cell_status((3, 3), True)
    g.set_cell_status((4, 3), True)

    runner.run_search(g, 5, (4, 2), (4, 4))

if __name__ == "__main__":
    main()