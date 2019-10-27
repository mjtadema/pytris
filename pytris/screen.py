import sys
import curses

class Screen():
    """
    Screen acts as an abstraction to curses
    It displays output but also records input

    Methods:
        command(): Get a command from

    screen.addstr(y, x, "hello world!")

       0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
    0  + - - - - - - - - - -  +
    1  | 0 0 0 0 0 0 0 0 0 0  |  S  C  O  R  E  :  int
    2  | 0 0 0 0 0 0 0 0 0 0  |  L  E  V  E  L  :  int
    3  | 0 0 0 0 0 0 0 0 0 0  |
    4  | 0 0 0 0 0 0 0 0 0 0  |  H  I  G  H  S  C  O  R  E  :
    5  | 0 0 0 0 0 0 0 0 0 0  |  str
    6  | 0 0 0 0 0 0 0 0 0 0  |  int
    7  | 0 0 0 0 0 0 0 0 0 0  |
    8  | 0 0 0 0 0 0 0 0 0 0  |
    9  | 0 0 0 0 0 0 0 0 0 0  |
    10 | 0 0 0 0 0 0 0 0 0 0  |
    11 | 0 0 0 0 0 0 0 0 0 0  |  N  E  X  T  :
    12 | 0 0 0 0 0 0 0 0 0 0  |
    13 | 0 0 0 0 0 0 0 0 0 0  |  +  -  -  -  -  +
    14 | 0 0 0 0 0 0 0 0 0 0  |  |  0  0  0  0  |
    15 | 0 0 0 0 0 0 0 0 0 0  |  |  0  0  0  0  |
    16 | 0 0 0 0 0 0 0 0 0 0  |  |  0  0  0  0  |
    17 | 0 0 0 0 0 0 0 0 0 0  |  |  0  0  0  0  |
    18 | 0 0 0 0 0 0 0 0 0 0  |  +  -  -  -  -  +
    19 | 0 0 0 0 0 0 0 0 0 0  |
    20 | 0 0 0 0 0 0 0 0 0 0  |
    21 + - - - - - - - - - -  +

    Your application can determine the size of the screen by using the
    curses.LINES and curses.COLS variables to obtain the y and x sizes.
    Legal coordinates will then extend from (0,0) to (curses.LINES - 1, curses.COLS - 1)

    """

    def __init__(self, game, screen = None):
        # Initialize some attributes
        self.game = game
        self.screen = screen
        # Draw static information to the screen
        try:
            self.static()
        except curses.error:
            raise Exception("Screen is too small!")
        self.print_count = 0
        # Only do this stuff if there is a screen
        if self.screen:
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                # Initialize all the color pairs
                curses.init_pair(i, -1, i)
            curses.curs_set(0)
            self.screen.nodelay(True)

    """
    Some wrappers to the screen
    They are skipped when there is no screen (for testing)
    """
    def addstr(self, y, x, s, color = 0):
        if not self.screen:
            return
        try:
            self.screen.addstr(y, x, str(s), curses.color_pair(color))
        except curses.error:
            pass
    def getkey(self, *args, **kwargs):
        if not self.screen:
            return
        return self.screen.getkey(*args, **kwargs)
    def refresh(self, *args, **kwargs):
        if not self.screen:
            return
        self.screen.refresh(*args, **kwargs)

    def pixel(self, x, y, color, y0 = 1, x0 = 1):
        """
        Method that draws a pixel to the grid
        Accepts coordinates as (x, y), abstracts away lame curses convention of using (y,x)
        """
        #if y < 0 or color == 0:
        #    return False

        self.addstr(
            y + y0,
            x + x0,
            " ",
            color
        )

    def resize(self):
        """
        Force a screen redraw when resizing
        """
        self.static()
        self.data()
        self.grid()
        self.block()
        self.next()

    def keytest(self):
        """
        prints a key string to the screen
        for testing
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
        TODO pause
        TODO exit
        :return: a function to execute
        """
        if not self.screen:
            return
        commands = {
            " ": self.game.block.down,
            "KEY_LEFT": self.game.block.left,
            "KEY_RIGHT": self.game.block.right,
            "KEY_UP": self.game.block.clockwise,
            "KEY_DOWN": self.game.block.countercw,
            "x": exit,
            "p": self.game.pause,
            "KEY_RESIZE": self.resize
        }
        try:
            return commands[self.getkey()]()
        except (curses.error, KeyError):
            pass
        return None

    def block(self):
        """
        Draw a mobile block to the screen
        Only draw if block is beyond the buffer zone..
        :return:
        """
        # First blank the previous position
        for x, y in self.game.block.last():
            y -= self.game.grid.top_buffer
            if y >= 0:
                self.pixel(x, y, 0)
        # Then draw the new position
        for x, y in self.game.block.position():
            y -= self.game.grid.top_buffer
            #self.print("y new: " + str(y))
            if y >= 0:
                self.pixel(x, y, self.game.block.color)
        # Finally refresh the screen
        self.refresh()

    def ghost(self):
        """
        TODO draw a ghost block on the bottom of the grid
        basically simulate falling and draw the final position
        """

    def next(self):
        """
        Draw next block pixels

        next(): Prints the next block in the corresponding field

           12 13 14 15 16 17
        13 +  -  -  -  -  +
        14 |  0  0  0  0  |
        15 |  0  0  0  0  |
        16 |  0  0  0  0  |
        17 |  0  0  0  0  |
        18 +  -  -  -  -  +

        :return: None
        """
        # Blank the next box
        for y in range(14, 18):
            self.addstr(y, 13, " " * 4)
        # Get the next block in the queue
        next = self.game.queue.next()
        for x, y in next.position(anchor = (2,1)):
            self.pixel(x, y, next.color, y0 = 14, x0 = 13)
        # Finally refresh the screen
        self.refresh()

    def data(self):
        """
        Draw data to appropriate places

        data(): print data like score, level, highscore etc

           0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
        0
        1                                              int
        2                                              int
        3
        4
        5                            str
        6                            int

        :return: None
        """
        self.addstr(1, 18, str(self.game.score))
        self.addstr(2, 18, str(self.game.level))
        self.addstr(5, 12, str(self.game.username))
        self.addstr(6, 12, str(self.game.highscore))
        # finally refresh
        self.refresh()

    def static(self):
        """
        Print all the static elements of the ui

           0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
        0  + - - - - - - - - - -  +
        1  |                      |  S  C  O  R  E  :
        2  |                      |  L  E  V  E  L  :
        3  |                      |
        4  |                      |  H  I  G  H  S  C  O  R  E  :
        5  |                      |
        6  |                      |
        7  |                      |
        8  |                      |
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

        # Finally refresh the screen
        self.refresh()

    def print(self, *message):
        """
        print a message in the appropriate place
        """
        self.addstr(8, 12, " " * 20)
        self.addstr(8, 12, str(self.print_count)+" "+" ".join(message))
        self.print_count += 1
        self.refresh()

    def grid(self):
        """
        Draw a matrix over the current grid
        Pixel by pixel (because different colors..)
        Then draw the mobile block

           0 1 2 3 4 5 6 7 8 9 10 11
        0  + - - - - - - - - - -  +
        1  | 0 0 0 0 0 0 0 0 0 0  |
        2  | 0 0 0 0 0 0 0 0 0 0  |
        3  | 0 0 0 0 0 0 0 0 0 0  |
        4  | 0 0 0 0 0 0 0 0 0 0  |
        5  | 0 0 0 0 0 0 0 0 0 0  |
        6  | 0 0 0 0 0 0 0 0 0 0  |
        7  | 0 0 0 0 0 0 0 0 0 0  |
        8  | 0 0 0 0 0 0 0 0 0 0  |
        9  | 0 0 0 0 0 0 0 0 0 0  |
        10 | 0 0 0 0 0 0 0 0 0 0  |
        11 | 0 0 0 0 0 0 0 0 0 0  |
        12 | 0 0 0 0 0 0 0 0 0 0  |
        13 | 0 0 0 0 0 0 0 0 0 0  |
        14 | 0 0 0 0 0 0 0 0 0 0  |
        15 | 0 0 0 0 0 0 0 0 0 0  |
        16 | 0 0 0 0 0 0 0 0 0 0  |
        17 | 0 0 0 0 0 0 0 0 0 0  |
        18 | 0 0 0 0 0 0 0 0 0 0  |
        19 | 0 0 0 0 0 0 0 0 0 0  |
        20 | 0 0 0 0 0 0 0 0 0 0  |
        21 + - - - - - - - - - -  +

        """
        # Blank the grid
        for y in range(1, 21):
            self.addstr(y, 1, " " * 10)
        # Draw the new grid
        for x, column in enumerate(self.game.grid):
            for y, color in enumerate(column):
                y -= self.game.grid.top_buffer
                if y >= 0:
                    self.pixel(x, y, color)

        # Finally refresh the screen
        self.refresh()

    def endgame(self):
        """
        Deal with the endgame condition
        """
        # TODO Write something for an endgame screen
        pass
