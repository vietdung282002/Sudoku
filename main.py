import pygame
import time
from Constant import *
from Solver import Solver
from Button import Button

pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)


class Grid:
    def __init__(self, N, K, rows, cols, width, height):
        self.N = N
        self.K = K
        self.solve = Solver(N, K)
        self.board = self.solve.board
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cubes(self.board.grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.Value = None
        self.selected = None
        self.Btn_Sol = Button("Solve", 120, 50, (40, 545))

    def Solve(self):
        self.solve.solve(self.board.grid)
        self.solve.printSudoku(self.board.grid)

    def update_value(self):
        self.Value = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_value()

            print("value: " + str(val) + " row: " + str(row) + " col: " + str(col))

            if val == self.board.grid[row][col]:
                return True
            else:
                self.cubes[row][col].set(0)
                self.update_value()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, screen):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(screen, BLACK, (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(screen, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(screen)

        self.Btn_Sol.draw(screen)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].flag = 1
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cubes:
    rows = 9
    cols = 9

    def __init__(self, value, rows, cols, width, height):
        self.value = value
        self.temp = 0
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.selected = False
        self.flag = None

    def draw(self, screen):
        gap = self.width / 9
        x = self.cols * gap
        y = self.rows * gap
        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), True, (128, 128, 128))
            screen.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), True, BLACK)
            screen.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(screen, RED, (x, y, gap, gap), 3)

        if self.flag == 0:
            pygame.draw.rect(screen, RED, pygame.Rect(x, y, gap, gap))
            text = font.render(str(self.temp), True, BLACK)
            screen.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
            for i in range(self.rows + 1):
                if i % 3 == 0 and i != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(screen, BLACK, (0, i * gap), (self.width, i * gap), thick)
                pygame.draw.line(screen, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        if self.flag == 2:
            pygame.draw.rect(screen, AQUA, pygame.Rect(x, y, gap, gap))
            text = font.render(str(self.value), True, BLACK)
            screen.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
            for i in range(self.rows + 1):
                if i % 3 == 0 and i != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(screen, BLACK, (0, i * gap), (self.width, i * gap), thick)
                pygame.draw.line(screen, BLACK, (i * gap, 0), (i * gap, self.height), thick)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(screen, board, time):
    screen.fill(WHITE)
    # Draw time
    font = pygame.font.SysFont("comicsans", 35)
    text = font.render("Time: " + timeToString(time), True, BLACK)
    screen.blit(text, (540 - 180, 540))
    # Draw grid and board
    board.draw(screen)


def timeToString(secs):
    sec = secs % 60
    minute = secs // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


class GameController(object):
    def __init__(self):
        self.levels = 0
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        pygame.display.set_caption("Sudoku")
        self.board = Grid(N, self.levels, 9, 9, SCREENWIDTH, SCREENHEIGHT - 60)
        self.val = None
        self.start = time.time()
        self.play_time = time.time()
        self.easy_btn = Button("EASY", 240, 80, (150, 170))
        self.medium_btn = Button("MEDIUM", 240, 80, (150, 270))
        self.hard_btn = Button("HARD", 240, 80, (150, 370))
        self.expert_btn = Button("EXPERT", 240, 80, (150, 470))

    def StartGame(self, screen):
        while True:
            screen.fill(WHITE)
            text = font.render("Choose levels", True, BLACK)
            screen.blit(text, (150, 80))
            self.easy_btn.draw(screen)
            self.medium_btn.draw(screen)
            self.hard_btn.draw(screen)
            self.expert_btn.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.easy_btn.check_click():
                        self.levels = EASY
                        self.board = Grid(N, self.levels, 9, 9, SCREENWIDTH, SCREENHEIGHT - 60)
                        self.print()
                        self.start = time.time()
                        self.update()
                    elif self.medium_btn.check_click():
                        self.levels = MEDIUM
                        self.board = Grid(N, self.levels, 9, 9, SCREENWIDTH, SCREENHEIGHT - 60)
                        self.print()
                        self.start = time.time()
                        self.update()
                    elif self.hard_btn.check_click():
                        self.levels = HARD
                        self.board = Grid(N, self.levels, 9, 9, SCREENWIDTH, SCREENHEIGHT - 60)
                        self.print()
                        self.start = time.time()
                        self.update()
                    elif self.expert_btn.check_click():
                        self.levels = EXPERT
                        self.board = Grid(N, self.levels, 9, 9, SCREENWIDTH, SCREENHEIGHT - 60)
                        self.print()
                        self.start = time.time()
                        self.update()
            pygame.display.update()

    def Solve(self):
        for i in range(N):
            for j in range(N):
                if self.board.cubes[i][j].value == 0:
                    self.board.cubes[i][j].flag = 2
                    self.board.cubes[i][j].set(self.board.board.grid[i][j])

    def update(self):
        while True:
            self.checkEvent()

    def print(self):
        self.board.Solve()

    def checkEvent(self):
        self.screen.fill(WHITE)
        self.play_time = round(time.time() - self.start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.val = 1
                if event.key == pygame.K_2:
                    self.val = 2
                if event.key == pygame.K_3:
                    self.val = 3
                if event.key == pygame.K_4:
                    self.val = 4
                if event.key == pygame.K_5:
                    self.val = 5
                if event.key == pygame.K_6:
                    self.val = 6
                if event.key == pygame.K_7:
                    self.val = 7
                if event.key == pygame.K_8:
                    self.val = 8
                if event.key == pygame.K_9:
                    self.val = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    self.board.clear()
                    self.val = None
                if event.key == pygame.K_RETURN:
                    i, j = self.board.selected
                    if self.board.cubes[i][j].temp != 0:
                        if self.board.place(self.board.cubes[i][j].temp):
                            self.board.cubes[i][j].flag = 1
                            print("Success")
                        else:
                            self.board.cubes[i][j].flag = 0
                            print("Wrong")
                        self.val = None

                        if self.board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.board.Btn_Sol.check_click():
                    self.Solve()
                pos = pygame.mouse.get_pos()
                clicked = self.board.click(pos)
                if clicked:
                    self.board.select(clicked[0], clicked[1])
                    self.val = None

        if self.board.selected and self.val is not None:
            self.board.sketch(self.val)

        redraw_window(self.screen, self.board, self.play_time)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        game.StartGame(game.screen)
