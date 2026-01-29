#!/usr/bin/env python3
# test_maze.py
import curses
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST # noqa

def draw_maze(stdscr, maze_obj):
    curses.curs_set(0) # Hides our terminal cursor
    
    # Safety check for terminal size because I learned it the hard way
    max_y, max_x = stdscr.getmaxyx()

    # We need HEIGHT * 2 lines and WIDTH * 4 columns
    needed_y = maze_obj.height * 2 + 2
    needed_x = maze_obj.width * 4 + 2

    if max_y < needed_y or max_x < needed_x:
        stdscr.addstr(0, 0, f"Error: Terminal too small! Need {needed_x}x{needed_y}")
        return

    # Our sacred loop
    for y in range(maze_obj.height):
        for x in range(maze_obj.width):
            cell_value = maze_obj.get_cell_value(y, x)
            
            # Coordinate offsetting (each cell is 4 chars wide and 2 chars tall)
            sy = y * 2
            sx = x * 4
            
            # Anchors (top left corner)
            stdscr.addstr(sy, sx, "+", curses.color_pair(1))

            # Drawing walls based on bitwise checks
            if cell_value & NORTH:
                stdscr.addstr(sy, sx + 1, "---", curses.color_pair(1))
            else:
                stdscr.addstr(sy, sx + 1, "   ")

            if cell_value & WEST:
                stdscr.addstr(sy + 1, sx, "|", curses.color_pair(1))
            else:
                stdscr.addstr(sy + 1, sx, " ")

            if x == maze_obj.width - 1:
                # We need to close the box on the right
                stdscr.addstr(sy, sx + 4, "+", curses.color_pair(1)) # top right corner
                if cell_value & EAST:
                    stdscr.addstr(sy + 1, sx + 4, "|", curses.color_pair(1))
            
            if y == maze_obj.height - 1:
                # We need to close the box at the bottom
                stdscr.addstr(sy + 2, sx, "+", curses.color_pair(1)) # bottom left corner
                if cell_value & SOUTH:
                    stdscr.addstr(sy + 2, sx + 1, "---", curses.color_pair(1))

            # Draw the other corners to seal each cell
            stdscr.addstr(sy, sx + 4, "+", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx, "+", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx + 4, "+", curses.color_pair(1))

def run_visualizer(maze_obj):
    curses.wrapper(lambda stdscr: _visualizer_logic(stdscr, maze_obj))

def _visualizer_logic(stdscr, maze_obj):
    curses.start_color()
    # Color Pair 1 = Green Text on Black Background
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
    
    stdscr.clear()
    draw_maze(stdscr, maze_obj)
    
    # UI Message at the bottom
    msg_y = (maze_obj.height * 2) + 1
    stdscr.addstr(msg_y, 0, "Press any key to exit...")
    
    stdscr.refresh()
    stdscr.getch()