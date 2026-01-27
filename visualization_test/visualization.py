import curses

def main(stdscr):
    curses.curs_set(0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    stdscr.box()
    stdscr.addstr(0, 48, "A-MAZE-ING", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(1, 2, "welcome to a-maze-ing or some shit", curses.color_pair(2))
    stdscr.addstr(2, 2, "here's yo maze babe:", curses.color_pair(1))
    
    curses.flash()

    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
