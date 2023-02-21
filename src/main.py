import runner
from graph_util import Graph

REPEATED_FORWARD_A_STAR = 0
REPEATED_BACKWARD_A_STAR = 1
ADAPTIVE_A_STAR = 2

def main():
    runner.run_search(mode=ADAPTIVE_A_STAR)

if __name__ == "__main__":
    main()