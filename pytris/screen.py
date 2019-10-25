import curses

"""
Define some parameters for the screen to use later
"""
screen_params = {
    "buff": 4, # Horizontal grid lines to not draw
    "y_off": 1, # y offset relative to grid
    "x_off": 1, # x offset relative to grid
}

class Screen():
    """
    Screen acts as an abstraction to curses
    It displays output but also records input

    Methods:
        command(): Get a command from

    screen.addstr(y, x, "hello world!")

       0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
    0  + - - - - - - - - - -  +
    1  |                      |  S  C  O  R  E  :  int
    2  |                      |  L  E  V  E  L  :  int
    3  |                      |
    4  |                      |  H  I  G  H  S  C  O  R  E  :
    5  |                      |  str
    6  |                      |  int
    7  |                      |
    8  |                      |  print statement
    9  |                      |
    10 |                      |
    11 |                      |  N  E  X  T  :
    12 |                      |
    13 |                      |  +  -  -  -  -  +
    14 |                      |  |              |
    15 |                      |  |              |
    16 |                      |  |              |
    17 |                      |  |              |
    18 |                      |  +  -  -  -  -  +
    19 |                      |
    20 |                      |
    21 + - - - - - - - - - -  +

    Your application can determine the size of the screen by using the
    curses.LINES and curses.COLS variables to obtain the y and x sizes.
    Legal coordinates will then extend from (0,0) to (curses.LINES - 1, curses.COLS - 1)

    """

    def __init__(self, game, screen = None):
        self.game = game
        self.screen = screen
        self.static()
        self.print_count = 0

        # Initialize empty frame buffer
        self.frame_buffer = self.blank_frame()

        if self.screen:
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                curses.init_pair(i, -1, i)
            curses.curs_set(0)
            self.screen.nodelay(True)

    @staticmethod
    def blank_frame():
        frame = [[] for _ in range(22)]
        for col in frame:
            col = [" " for _ in range(22)]
        return

    def build_frame(self):
        """
        Writes all the screen elements to the frame buffer layer by layer
        """
        self.static()
        self.data()
        self.next()
        self.grid()

    def flush(self):
        """
        Write the frame buffer row by row to curses and refresh the screen
        """
        for y in range(22):
            row = [self.frame_buffer[x][y] for x in range(22)]
            row = "".join(row)
            self.


        self.frame_buffer = self.blank_frame()

    # TODO this code should be moved to addstr
    def curses(curses_func):
        """
        Decorator for functions dealing with a curses screen
        If in debugging mode, curses is not initialized so these functions would fail
        This decorator simply passes those functions if in debug mode
        :return: None
        """
        def wrapper(self, *args, **kwargs):

            func_return = curses_func(*args, **kwargs)
            self.screen.refresh()
            return func_return
        return wrapper

    """
    Some wrappers to the screen attribute
    """
    def addstr(self, *args, **kwargs):
        if not self.screen:
            return
        self.screen.addstr(*args, **kwargs)
    def getkey(self, *args, **kwargs):
        if not self.screen:
            return
        return self.screen.getkey(*args, **kwargs)
    def block_color(self, color):
        if not self.screen:
            return
        return curses.color_pair(color)
    def refresh(self, *args, **kwargs):
        if not self.screen:
            return
        self.screen.refresh(*args, **kwargs)


    def pixel(self, x, y, color):
        """
        Method that draws a pixel to the grid
        0 is ignored as well as pixels above the buffer
        """
        border_width = 1
        y_offset = 1
        x_offset = 1
        y -= self.game.grid.buffer
        if y < 0 or color == 0:
            return False

        self.addstr(
            y + y_offset + border_width,
            x + x_offset + border_width,
            color,
            color
        )

    def keytest(self):
        """
        prints a key string to the screen
        """
        import time
        self.print("Testing keys")
        while True:
            try:
                self.print(self.getkey())
            except curses.error:
                pass # ignore when no key is pressed

            time.sleep(0.01)

    def command(self):
        """
        Attempt to get a command and execute it
        Available commands:
        down
        left
        right
        clockwise
        counter clockwise
        pause
        exit
        :return: Bool for success status
        """
        commands = {
            " ": self.game.block.down(),
            "KEY_LEFT": self.game.block.left(),
            "KEY_RIGHT": self.game.block.right(),
            "KEY_UP": self.game.block.clockwise(),
            "KEY_DOWN": self.game.block.countercw()
        }
        try:
            commands[self.getkey()]
        except curses.error:
            pass

    def block(self):
        """
        Draw a mobile block to the screen
        Only draw if block is beyond the buffer zone..
        :return:
        """
        for x, y in self.game.block.position():
            self.pixel(y, x, self.game.block.color)

    def next(self):
        """
        Draw next block pixels
        :return: None
        """
        y_off, x_off = (14, 13)
        next = self.game.queue.next()
        for x, y in next.position():
            self.addstr(
                y + y_off,
                x + x_off,
                " ",
                next.color
            )

    def data(self):
        """
        Draw data to appropriate places
        :return: None
        """
        self.addstr(1, 18, str(self.game.score))
        self.addstr(2, 18, str(self.game.level))
        self.addstr(5, 12, str(self.game.username))
        self.addstr(6, 12, str(self.game.highscore))

    def static(self):
        """
        Print all the static elements of the ui
        TODO: maybe not hardcode the width and height? though it would never change..
        """
        horizontal = "-"
        vertical = "|"
        corner = "+"

        # Draws the game border
        top = corner + horizontal * 10 + corner
        bottom = top
        side = vertical + " " * 10 + vertical
        self.addstr(0, 0, top)
        for i in range(1, 21):
            self.addstr(i, 0, side)
        self.addstr(21, 0, bottom)

        # Draws the "next" border
        top = corner + horizontal * 4 + corner
        bottom = top
        side = vertical + " " * 4 + vertical
        self.addstr(13, 12, top)
        for i in range(14, 14 + 4):
            self.addstr(i, 12, side)
        self.addstr(14 + 4, 12, bottom)

        # Draws text to the screen
        self.addstr(1, 12, "SCORE:")
        self.addstr(2, 12, "LEVEL:")
        self.addstr(4, 12, "HIGHSCORE:")
        self.addstr(11, 12, "NEXT:")

        self.refresh()

    def print(self, *message):
        """
        print a message in the appropriate place
        """
        self.screen.addstr(8, 12, " " * 12)
        self.screen.addstr(8, 12, str(self.print_count)+" "+" ".join(message))
        self.print_count += 1
        self.screen.refresh()

    def grid(self):
        """
        Draw a matrix over the current grid
        Then draw the mobile block again because that's the easiest
        """
        self.print("Drawing grid..")
        self.blank_grid()
        for x, col in enumerate(self.game.grid):
            for y, color in enumerate(col):
                self.pixel(x, y, color)
        self.print("Drawing block")
        self.block()

    def blank_grid(self):
        """
        Blank the grid to prepare for a freshly drawn screen
        """
        for y in range(2, 2 + 1 + 20):
            self.addstr(y, 2, " " * 20)

    def endgame(self):
        """
        Deal with the endgame condition
        """
        pass
