import os
from graph_util import *
from search import *
import sys, time, pygame

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

def get_statistics():
    # ran on 50 graphs of dimensions 101x101
    s, m = Search(), Maze()
    test_graphs = m.get_testing_graphs(count=5)
    print("Generated graphs!")

    r_time, r_expanded = 0, 0
    for graph in test_graphs:
        print("Checking repeated")
        start_time = time.perf_counter()
        cur_path, num_expanded = s.repeated_A_star(graph, (0, 0), (19, 19))

        if not cur_path: # if no path exists, don't use for statistics
            continue

        end_time = time.perf_counter()
        r_time += (end_time - start_time)
        r_expanded += num_expanded
    r_time, r_expanded = r_time/50, r_expanded/50

    if r_time == 0:
        raise Exception("None of the graphs generated had a viable path.")

    a_time, a_expanded = 0, 0
    for graph in test_graphs:
        print("Checking adaptive")

        start_time = time.perf_counter()
        cur_path, num_expanded = s.adaptive_A_star(graph, (0, 0), (19, 19))

        if not cur_path: # if no path exists, don't use for statistics
            continue

        end_time = time.perf_counter()
        a_time += (end_time - start_time)
        a_expanded += num_expanded
    a_time, a_expanded = a_time/50, a_expanded/50

    print(f"Average time taken for repeated A star: {r_time: .2f}, with average number of nodes expanded: {r_expanded: .2f}")
    print(f"Average time taken for adaptive A star: {a_time: .2f}, with average number of nodes expanded: {a_expanded: .2f}")

    diff_time, diff_expanded = (r_time - a_time)/r_time, (r_expanded - a_expanded)/r_expanded
    print(f"On average, adaptive A star took {diff_time: .2%} less time, with {diff_expanded: .2%} less nodes expanded.")

if __name__ == "__main__":
    get_statistics()
    '''
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

    BLOCK_SIZE = SCREEN_WIDTH/g.get_dim()
    head = pygame.image.load(os.path.join('./models/', 'head.png'))
    head = pygame.transform.scale(head, (BLOCK_SIZE, BLOCK_SIZE))

    path, _ = s.adaptive_A_star(g, (4, 2), (4, 4))
    draw_grid(g, BLOCK_SIZE, screen)
    run(screen, path, BLOCK_SIZE)
    '''

