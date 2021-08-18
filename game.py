import pygame
from menu import *
from algorithm import *


class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 800
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption("PathFinding Algorithm")
        self.font_name = '8-BIT WONDER.TTF'
        # self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.algorithm_type = "A Star"
        self.quit = False

    def game_loop(self):
        grid = make_grid(ROWS, COLS, self.DISPLAY_W)
        start = end = None

        while self.playing:
            self.check_events()
            if self.START_KEY or self.BACK_KEY:
                self.playing = False

            draw(self.window, grid, ROWS, self.DISPLAY_W)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.quit = True
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.playing = False
                        break

                if pygame.mouse.get_pressed()[0]:  # LEFT MOUSE BUTTON
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, self.DISPLAY_W)
                    node = grid[row][col]

                    if not start and node != end:
                        start = node
                        start.color = start_color
                    elif not end and node != start:
                        end = node
                        end.color = end_color
                    elif node != end and node != start:
                        node.color = barrier_color

                    clear_grid(grid)

                elif pygame.mouse.get_pressed()[2]:  # RIGHT MOUSE BUTTON
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, self.DISPLAY_W)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)

                        clear_grid(grid)
                        draw(self.window, grid, ROWS, self.DISPLAY_W)

                        # there are two types of algorithm this program can run: a* and breadth first search
                        if self.algorithm_type == "A Star":
                            a_star_algorithm(lambda: draw(self.window, grid, ROWS, self.DISPLAY_W), grid, start, end)
                        elif self.algorithm_type == "Breadth First":
                            breadth_first_search(lambda: draw(self.window, grid, ROWS, self.DISPLAY_W), start, end)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = make_grid(ROWS, COLS, self.DISPLAY_W)

            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
