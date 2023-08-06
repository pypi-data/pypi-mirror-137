




import curses
from curses import textpad

class NCursesScreen:
    def __init__(self, screen: curses._CursesWindow) -> None:
        self.__screen = screen
        self.height, self.width = self.__screen.getmaxyx()

         # red
        red_fore = curses.COLOR_RED
        red_back = 0
        curses.init_pair(1, red_fore, curses.COLOR_BLACK)
        self.red_foreground = curses.color_pair(1)

        # blue
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.blue_foreground = curses.color_pair(2)

        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.yellow_foreground = curses.color_pair(3)

        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.white_foreground = curses.color_pair(4)

        #  curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, 240, 233)
        self.gray_foreground = curses.color_pair(5)


        curses.init_pair(6, 240, 233)
        self.gray_background = curses.color_pair(6) | curses.A_BOLD

        #  curses.init_pair(6, 197, 52)
        curses.init_pair(7, red_fore, red_back)
        self.red_background = curses.color_pair(7) | curses.A_BOLD

        curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.green_foreground = curses.color_pair(8)


    def draw_rectangle(self, y1: int, x1: int, y2: int, x2: int) -> None:
        """
            this is a rectangle with specified coordinates:

            (y1, x1)            (y1, x1)
            |------------------|
            |                  |
            |                  |
            |                  |
            |------------------|
            (y2, x1)            (y2, x2)
        """
        textpad.rectangle(self.__screen, y1, x1, y2, x2)


    def print_text(self, y: int, x: int, item, color=None) -> None:
        """
            just prints text on ncurses screen at (y, x)
        """

        if type(item) != str:
            item = str(item)
        if color:
            self.__screen.addstr(y, x, item, color)
        else:
            self.__screen.addstr(y, x, item)


    def print_lines(self,
        y: int,
        x: int,
        lines: list,
        from_index: int
    ) -> None:
        for yy, line in enumerate(lines[from_index:], start=y):
            self.__screen.addstr(
                yy,
                x,
                line.replace("\n", "↵").replace("\t", "--->")
            )


    def await_input(self):
        self.__screen.getch()


    def refresh(self):
        self.__screen.refresh()


    def move_cursor(self, y: int, x: int):
        self.__screen.move(y, x)



    def get_char(self):
        return self.__screen.getch()


    def get_max_x_y(self):
        return self.__screen.getmaxyx()


    def clear(self):
        self.__screen.clear()


    def resize(self):
       self.height, self.width = self.get_max_x_y()
       self.clear()


