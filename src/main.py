import os
from graph_util import *
from search import *
import sys, time, pygame, random

# main file
sys.setrecursionlimit(12000)
SCREEN_HEIGHT, SCREEN_WIDTH = 800, 800

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
        f_time += (end_time - start_time)
        f_expanded += num_expanded

        # ADAPTIVE A STAR
        start_time = time.perf_counter()
        cur_path, num_expanded = s.adaptive_A_star(graph, c_start, c_end)
        end_time = time.perf_counter()
        b_time += (end_time - start_time)
        b_expanded += num_expanded

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

if __name__ == "__main__":
    # repeated_vs_adaptive_statistics(2)
    forward_vs_backward_statistics()

    """
    OFFSET = 1
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH+OFFSET, SCREEN_HEIGHT+OFFSET))

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
    print(g)

    g, _ = m.generate_graph(1, dim=10)

    BLOCK_SIZE = SCREEN_WIDTH/g.get_dim()
    head = pygame.image.load(os.path.join('./models/', 'head.png'))
    head = pygame.transform.scale(head, (BLOCK_SIZE, BLOCK_SIZE))

    r_path, _ = s.repeated_A_star(g, (0, 0), (9, 9))
    print(r_path)
    a_path, _ = s.adaptive_A_star(g, (0, 0), (9, 9))
    print(a_path)

    draw_grid(g, BLOCK_SIZE, screen)
    run(screen, a_path, BLOCK_SIZE)
    """
