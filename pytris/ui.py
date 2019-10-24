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
    """

    def __init__(self, game, screen, *args, **kwargs):
        self.game = game
        self.grid_y, self.grid_x = self.game.gridsize
        self.screen = screen
        self.border()
        curses.curs_set(0)
        self.screen.nodelay(True)


    def addstr(self, *args, **kwargs):
        self.screen.addstr(*args, **kwargs)

    def refresh(self, *args, **kwargs):
        self.screen.refresh(*args, **kwargs)

    def block(self):
        """
        Draw a mobile block to the screen
        Only draw if block is beyond the buffer zone..
        :return:
        """
        pass

    def next(self):
        """
        Draw next block to screen in appropriate area
        :return: None
        """
        pass

    def data(self):
        """
        Draw data to appropriate places
        :return: None
        """
        pass

    def border(self):
        """
        Print the border at initialization
        """
        horizontal = "+----------+"
        vertical   = "|          |"
        self.addstr(0, 0, horizontal)
        border_height = self.grid_y - screen_params['buff']
        for y in range(border_height):
            Y = y+1
            self.addstr(Y, 0, vertical)
        self.addstr(border_height+1, 0, horizontal)
        self.screen.refresh()
    
    def print(self, *message):
        """
        print a message in the appropriate place
        """
        y_print = 4
        x_print = 12 + screen_params['x_off']
        self.screen.addstr(y_print, x_print, " ".join(message))
        self.screen.refresh()

    def grid(self, grid):
        """
        Draw a matrix over the current grid
        Then draw the mobile block again because that's the easiest
        """
        pass
