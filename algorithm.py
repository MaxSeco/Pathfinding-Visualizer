import pygame
from queue import PriorityQueue
from collections import deque

WIDTH = 800
ROWS = 50
COLS = 50
infinity = float("inf")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (114, 188, 220)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
LIGHT_BLUE = (173, 216, 230)

path_color = YELLOW
start_color = ORANGE
barrier_color = BLACK
end_color = PURPLE
open_color = BLUE
closed_color = TURQUOISE

# each box in the grid is a node
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self._color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self._color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self._color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].color == barrier_color:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].color == barrier_color:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].color == barrier_color:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].color == barrier_color:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        # DIAGONALS
        # if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].color == barrier_color:
        #     self.neighbors.append(grid[self.row - 1][self.col - 1])  # TOP LEFT
        #
        # if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():
        #     self.neighbors.append(grid[self.row + 1][self.col - 1])  # TOP RIGHT
        #
        # if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():
        #     self.neighbors.append(grid[self.row - 1][self.col + 1])  # BOTTOM LEFT
        #
        # if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier():
        #     self.neighbors.append(grid[self.row + 1][self.col + 1])  # BOTTOM RIGHT

    def __lt__(self, other):
        return False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color


# h_score
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# makes the path from start to end after algorithm finishes
def reconstruct_path(parents, start, current, draw):
    while current in parents:
        current = parents[current]
        if current == start:
            break
        current.color = path_color
        draw()


def a_star_algorithm(draw, grid, start, end, delay=True):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    parents = {}
    g_score = {node: infinity for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: infinity for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(parents, start, end, draw)
            start.color = start_color
            end.color = end_color
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                parents[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = open_color

        if delay:
            draw()

        if current != start:
            current.color = closed_color

    return False


def breadth_first_search(draw, start, end):
    queue = deque()
    visited = set()  # prevents checking nodes already checked
    parents = {}  # used to reconstruct path
    queue.append(start)

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False

        current = queue.popleft()
        if current not in visited:
            for neighbor in current.neighbors:
                # if any neighbor node is the end node, end algorithm and construct path
                if neighbor == end:
                    parents[neighbor] = current
                    reconstruct_path(parents, start, end, draw)
                    start.color = start_color
                    end.color = end_color
                    return True

                # adds neighbor to queue to be evaluated
                queue.append(neighbor)
                if neighbor not in parents:
                    parents[neighbor] = current
                if neighbor not in visited:
                    neighbor.color = open_color

            current.color = closed_color
            visited.add(current)
            draw()
        else:
            current.color = closed_color

        start.color = start_color

    return False


# creates the grid object
def make_grid(rows, cols, width):
    gap = width // rows
    grid = [[Node(i, j, gap, rows) for j in range(cols)] for i in range(rows)]

    return grid


# draws the grid lines but doesn't update display
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# resets grid, leaving only the start, end, and barriers
def clear_grid(grid):
    for row in grid:
        for node in row:
            if node.color == open_color or node.color == closed_color or node.color == path_color:
                node.reset()


# updates the display
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

