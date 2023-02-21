# Fast-Trajectory-Replanning

This program was coded on Python 3.10.7 on MacOS Ventura 13.0.

To compile and run main.py, run the command on the terminal without the quotes: "python3 main.py"

The following functions are available:

1. repeated_vs_adaptive_statistics(graph_count):
    @param graph_count - number of graphs to be tested. Defaulted to 50 graphs.

    This function generates graphs with dimension 101x101 and runs repeated forward A* and adaptive A* on each graph.
    It then takes the average time and average number of nodes expanded, and compares the two.

2. forward_vs_backward_statistics(graph_count):
    @param graph_count - number of graphs to be tested. Defaulted to 50 graphs.

    Similar to the repeated_vs_adaptive_statistics, it compares repeated forward A* and repeated backwards A* on each graph,
    and compares the statistics for the two.

3. run_demo(mode):
    @param mode - mode pertaining to the search algorithm. Defaulted to ADAPTIVE_A_STAR.

    Options for the mode:
        - ADAPTIVE_A_STAR
        - REPEATED_FORWARD_A_STAR
        - REPEATED_BACKWARD_A_STAR
    
    The demo graph is the same as figure 3 (page 4) on the assignment pdf.
    Runs the search algorithm on the demo graph and then visualizes it using a pygame window.

4. run_search(graph, dim, start_t, goal_t, mode):
    @param graph - graph that the search algorithm is to be ran on. Defaulted to None.
    @param dim - dimension of the passed graph. Defaulted to 50.
    @param start_t - tuple representing the starting state. Defaulted to None.
    @param goal_t - tuple representing the goal state. Defaulted to None.
    @param mode - mode pertaining to the search algorithm. Defaulted to ADAPTIVE_A_STAR

    If you are passing in a graph, make sure that the parameters dim, start_t and goal_t are all also passed in as parameters.

    If a graph is not passed in, it generates a graph of size dim (with a guaranteed path), and then runs a search algorithm on that graph with the start state being (0, 0) and end state being (dim-1, dim-1). The path is then visualized using a pygame window.
    Also prints the time taken and the number of nodes expanded into the terminal.

    If there are no parameters passed in, it will simply generate a 50x50 graph and run adaptive A* on it, starting at (0, 0) and ending at (49, 49).

    The greater the dim, the longer it will take to execute since it makes sure that the graph generated has a valid path. The graph generation is given 10 iterations before it exits and raises an exception. It is recommended to keep the dim <= 50 as that has consistently worked for us in at most 30 seconds. If the pygame window pops up with no path, please execute the code again as there appears to be some inconsistency with pygame.