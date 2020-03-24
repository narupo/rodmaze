import curses
from curses import wrapper
import random


class Color:
    FLOOR = 1
    WALL = 2


class Maze:
    FLOOR = 0
    WALL = 1

    def __init__(self, height, width):
        self.__mat = []
        
        self.__height = height
        if self.__height % 2 == 0:
            self.__height -= 1

        self.__width = width
        if self.__width % 2 == 0:
            self.__width -= 1

        self.init_matrix()
        self.build_outer_wall()
        self.build_maze()

    def init_matrix(self):
        self.__mat = []

        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                row.append(Maze.FLOOR)
            self.__mat.append(row)

    def build_outer_wall(self):
        h, w = self.__height, self.__width

        for y in range(h):
            for x in range(w):
                if (y == 0 or y == h-1) or (x == 0 or x == w-1):
                    self.__mat[y][x] = Maze.WALL
    
    def build_maze(self):
        for y in range(2, self.__height-1, 2):
            for x in range(2, self.__width-1, 2):
                self.__mat[y][x] = Maze.WALL

                dr = random.randint(0, 3)
                if dr == 0:
                    self.__mat[y-1][x] = Maze.WALL
                elif dr == 1:
                    self.__mat[y+1][x] = Maze.WALL
                elif dr == 2:
                    self.__mat[y][x-1] = Maze.WALL
                elif dr == 3:
                    self.__mat[y][x+1] = Maze.WALL

    def render(self, window):
        for my in range(self.__height):
            for mx in range(self.__width):
                c = self.__mat[my][mx]
                ch = None
                color = None
                if c == 0:
                    ch = ' '
                    color = Color.FLOOR
                elif c == 1:
                    ch = ' '
                    color = Color.WALL
                
                try:
                    window.addstr(my, mx, ch, curses.color_pair(color))
                except curses.error:
                    pass


def main(window):
    # カーソルを非表示に
    curses.curs_set(False)

    # 色の初期化
    curses.init_pair(Color.FLOOR, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(Color.WALL, curses.COLOR_BLACK, curses.COLOR_BLACK)

    h, w = window.getmaxyx()
    maze = Maze(h, w)

    window.clear()
    maze.render(window)
    window.refresh()
    window.getch()


wrapper(main)
