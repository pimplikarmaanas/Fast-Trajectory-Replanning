import os
from graph_util import *
from search import *
import sys, time, pygame, random

sys.setrecursionlimit(12000)
SCREEN_HEIGHT, SCREEN_WIDTH = 800, 800

# modes for demo and visualization
REPEATED_FORWARD_A_STAR = 0
REPEATED_BACKWARD_A_STAR = 1
ADAPTIVE_A_STAR = 2

def run(screen, path, block_size):
    i = 0
    prev = False
    while True:
        if path and i < len(path):
            time.sleep(0.05)
            if prev:
                pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(prev[0], prev[1], block_size-1, block_size-1))
            x = path[i].position[1]*block_size + 1
            y = path[i].position[0]*block_size + 1
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, block_size-1, block_size-1))
            prev = (x, y)
            i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()


def draw_grid(g, block_size, screen):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    for i in range(g.get_dim()):
        for j in range(g.get_dim()):
            if g[(i, j)].is_blocked():
                left = block_size * j
                top = block_size * i
                width = block_size
                height = block_size
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(left, top, width, height))

    for i in range(g.get_dim()+1):
        pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(block_size * i, 0),
                         end_pos=(block_size * i, SCREEN_HEIGHT), width=1)
        pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(0, (SCREEN_HEIGHT/(g.get_dim())) * i),
                         end_pos=(SCREEN_WIDTH, (SCREEN_HEIGHT/(g.get_dim())) * i), width=1)

def generate_valid_graph(label:int, dim=TEST_GRAPH_DIM):
    total_time, s, m = 0, Search(), Maze()

    g, time = m.generate_graph(label, dim)
    total_time += time

    count = 1
    path, _ = s.adaptive_A_star(g, (0, 0), (dim-1, dim-1))

    while not path and count < 10:
        g, time = m.generate_graph(label, dim)
        total_time += time
        path, _ = s.adaptive_A_star(g, (0, 0), (dim-1, dim-1))

    if count == 10:
        return None
    
    return g

def repeated_vs_adaptive_statistics(graph_count=50):
    count = graph_count
    test_start = time.perf_counter()

    # ran on 50 graphs of dimensions 101x101
    s, m = Search(), Maze()
    test_graphs = m.get_testing_graphs(count=graph_count)
    print("Generated graphs!")

    r_time, r_expanded = 0, 0
    a_time, a_expanded = 0, 0

    for graph in test_graphs:
        print(f"{graph.get_label()/graph_count: .2%} completed.", end="\r")
        c_start, c_end = (0, 0), (100, 100)
        # REPEATED A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.repeated_A_star(graph, c_start, c_end)

        if not cur_path: # if no path exists, don't use for statistics
            graph_count -= 1
            continue

        end_time = time.perf_counter()
        r_time += (end_time - start_time)
        r_expanded += num_expanded

        # ADAPTIVE A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.adaptive_A_star(graph, c_start, c_end)
        end_time = time.perf_counter()
        a_time += (end_time - start_time)
        a_expanded += num_expanded

    r_time, r_expanded = r_time/count, r_expanded/count
    a_time, a_expanded = a_time/count, a_expanded/count

    if r_time == 0:
        raise Exception("None of the graphs generated had a viable path.")

    print(f"Average time taken for repeated A star: {r_time} seconds, with average number of nodes expanded: {r_expanded: .2f}")
    print(f"Average time taken for adaptive A star: {a_time} seconds, with average number of nodes expanded: {a_expanded: .2f}")

    diff_time, diff_expanded = (r_time - a_time)/r_time, (r_expanded - a_expanded)/r_expanded
    print(f"On average, adaptive A star took {diff_time: .2%} less time, with {diff_expanded: .2%} less nodes expanded.")
    test_end = time.perf_counter()
    print(f"Testing took {test_end - test_start : .4f} seconds.")

def forward_vs_backward_statistics(graph_count=50):
    count = graph_count
    test_start = time.perf_counter()

    # ran on 50 graphs of dimensions 101x101
    s, m = Search(), Maze()
    test_graphs = m.get_testing_graphs(count=graph_count)
    print("Generated graphs!")

    f_time, f_expanded = 0, 0
    b_time, b_expanded = 0, 0

    for graph in test_graphs:
        print(f"{graph.get_label()/count: .2%} completed.", end="\r")
        c_start, c_end = (0, 0), (100, 100)
        # REPEATED A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.repeated_A_star(graph, c_start, c_end)

        if not cur_path: # if no path exists, don't use for statistics
            graph_count -= 1
            continue

        end_time = time.perf_counter()
        c_f_time = end_time - start_time

        # BACKWARD A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.repeated_backwards_A_star(graph, c_start, c_end)
        if not cur_path: # if no path exists, don't use for statistics
            graph_count -= 1
            continue
        end_time = time.perf_counter()

        b_time += (end_time - start_time)
        b_expanded += num_expanded

        f_time += c_f_time
        f_expanded += num_expanded

    f_time, f_expanded = f_time/count, f_expanded/count
    b_time, b_expanded = b_time/count, b_expanded/count

    if f_time == 0:
        raise Exception("None of the graphs generated had a viable path.")

    print(f"Average time taken for repeated forward A star: {f_time} seconds, with average number of nodes expanded: {f_expanded: .2f}")
    print(f"Average time taken for repeated backwards A star: {b_time} seconds, with average number of nodes expanded: {b_expanded: .2f}")

    diff_time, diff_expanded = (f_time - b_time)/f_time, (f_expanded - b_expanded)/f_expanded
    print(f"On average, repeated backwards A star took {diff_time: .2%} less time, with {diff_expanded: .2%} less nodes expanded.")
    test_end = time.perf_counter()
    print(f"Testing took {test_end - test_start : .4f} seconds.")    

def run_demo(mode=ADAPTIVE_A_STAR):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH+1, SCREEN_HEIGHT+1))

    m = Maze()
    s = Search()

    # TESTING GRAPH THATS SHOWN IN THE ASSIGNMENT PDF
    g = Graph(1, 5)
    g.set_cell_status((1, 2), True)
    g.set_cell_status((2, 2), True)
    g.set_cell_status((3, 2), True)
    g.set_cell_status((2, 3), True)
    g.set_cell_status((3, 3), True)
    g.set_cell_status((4, 3), True)

    BLOCK_SIZE = SCREEN_WIDTH/g.get_dim()
    head = pygame.image.load(os.path.join('./models/', 'head.png'))
    head = pygame.transform.scale(head, (BLOCK_SIZE, BLOCK_SIZE))
    
    if mode == ADAPTIVE_A_STAR:
        path, _ = s.adaptive_A_star(g, (4, 2), (4, 4))
    elif mode == REPEATED_FORWARD_A_STAR:
        path, _ = s.repeated_A_star(g, (4, 2), (4, 4))
    elif mode == REPEATED_BACKWARD_A_STAR:
        path, _ = s.repeated_backwards_A_star(g, (4, 4), (4, 2))
    else:
        raise Exception("Invalid mode.")
    

    draw_grid(g, BLOCK_SIZE, screen)
    run(screen, path, BLOCK_SIZE)

def run_search(graph=None, dim=50, start_t=None, goal_t=None, mode=ADAPTIVE_A_STAR):
    m = Maze()
    s = Search()

    if not graph:
        graph = generate_valid_graph(1, dim)
    
    if not graph:
        raise Exception("Graph creation took too long. Please try again or reduce the dimensions.")
        return

    if not start_t:
        start_t = (0, 0)
    
    if not goal_t:
        goal_t = (dim-1, dim-1)

    total_time = 0
    if mode == ADAPTIVE_A_STAR:
        start = time.perf_counter()
        path, num_nodes = s.adaptive_A_star(graph, start_t, goal_t)
        total_time = time.perf_counter() - start

    elif mode == REPEATED_FORWARD_A_STAR:
        start = time.perf_counter()
        path, num_nodes = s.repeated_A_star(graph, start_t, goal_t)
        total_time = time.perf_counter() - start

    elif mode == REPEATED_BACKWARD_A_STAR:
        start = time.perf_counter()
        path, num_nodes = s.repeated_backwards_A_star(graph, start_t, goal_t)
        total_time = time.perf_counter() - start

    else:
        raise Exception("Invalid mode.")

    print(f"Path found in {total_time: .3f} seconds, with {num_nodes} nodes expanded")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH+1, SCREEN_HEIGHT+1))

    BLOCK_SIZE = SCREEN_WIDTH/graph.get_dim()
    draw_grid(graph, BLOCK_SIZE, screen)
    run(screen, path, BLOCK_SIZE)