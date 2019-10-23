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
    """

    def __init__(self, gridsize, screen, *args, **kwargs):
        self.gridsize = gridsize
        self.grid_y, self.grid_x = self.gridsize
        self.screen = screen
        self.border()
        curses.curs_set(0)
        self.screen.nodelay(True)
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, -1, i);

    def addstr(self, *args, **kwargs):
        self.screen.addstr(*args, **kwargs)

    def refresh(self, *args, **kwargs):
        self.screen.refresh(*args, **kwargs)

    def border(self):
        """
        Print the border at initialization
        """
        top = "+----------+"
        bottom = "+----------+"
        side = "|          |"
        self.addstr(0, 0, top)
        border_height = self.grid_y - screen_params['buff']
        for y in range(border_height):
            Y = y+1
            self.addstr(Y, 0, side)
        self.addstr(border_height+1, 0, bottom)
        self.screen.refresh()
    
    def print(self, *message):
        """
        print a message in the appropriate place
        """
        y_print = 4
        x_print = 12 + screen_params['x_off']
        self.screen.addstr(y_print, x_print, " ".join(message))
        self.screen.refresh()

    def overlay(self, grid):
        """
        Draw a sparse matrix over the current grid
        """
        pass
