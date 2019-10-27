def main(screen = None, keytest = False):
    from pytris.game import Game
    try:
        game = Game(screen = screen)
        if keytest:
            game.screen.keytest()
        else:
            game.start()
    except KeyboardInterrupt:
        exit()

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio', '-a', action='store_true', default=False)
    parser.add_argument('--debug', '-d', action='store_true', default=True)
    parser.add_argument('--keytest', '-t', action='store_true', default=False)
    return parser.parse_args()

def wrap():
    import curses
    args = parse_args()
    kwargs = {}
    if args.keytest:
        kwargs['keytest'] = True
    curses.wrapper(main, **kwargs)

if __name__ == "__main__":
    wrap()