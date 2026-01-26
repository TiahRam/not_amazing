import curses

def main(stdscr):
    curses.curs_set(0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_MAGENTA )
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.box()
    stdscr.addstr(0,48, "A-MAZE-ING", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(1,3, "welcome to a-maze-ing or some shit", curses.color_pair(2) | curses.A_BLINK)
    curses.flash()

    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)