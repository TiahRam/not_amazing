#!/usr/bin/env python3

import curses
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST # noqa


def get_path_coordinates(entry, path_str):
    coords = set()
    curr_y, curr_x = entry
    coords.add((curr_y, curr_x)) # Add start
    
    for move in path_str:
        if move == 'N': curr_y -= 1
        elif move == 'S': curr_y += 1
        elif move == 'E': curr_x += 1
        elif move == 'W': curr_x -= 1
        coords.add((curr_y, curr_x))
    return coords

def draw_maze(stdscr, maze_obj, entry, exit, path_coords):
    curses.curs_set(0) # Hides our terminal cursor
    
    max_y, max_x = stdscr.getmaxyx()
    needed_y = maze_obj.height * 2 + 2
    needed_x = maze_obj.width * 4 + 2

    if max_y < needed_y or max_x < needed_x:
        stdscr.addstr(0, 0, f"Error: Terminal too small! Need {needed_x}x{needed_y}")
        return

    # Our sacred loop
    for y in range(maze_obj.height):
        for x in range(maze_obj.width):
            cell_value = maze_obj.get_cell_value(y, x)
            
            # Coordinate offsetting
            sy = y * 2
            sx = x * 4

            # If cell is in 42 pattern
            is_pattern_block = (cell_value == 0xF)
            
            # If cell is in path_coords
            is_path = (y, x) in path_coords
            
            # We check if this (y, x) is in our path set
            if is_pattern_block:
                 stdscr.addstr(sy + 1, sx + 1, "   ", curses.color_pair(3))
            else:
                if (y, x) in path_coords:
                    stdscr.addstr(sy + 1, sx + 1, "   ", curses.color_pair(2))
            
                if (y, x) == entry:
                    stdscr.addstr(sy + 1, sx, "▀▄▀▄", curses.color_pair(5))
                if (y, x) == exit:
                    stdscr.addstr(sy + 2, sx, "▀▄▀▄", curses.color_pair(4))

            # Anchors (top left corner)
            stdscr.addstr(sy, sx, "+", curses.color_pair(1))

            # Drawing walls based on bitwise checks
            if cell_value & NORTH:
                stdscr.addstr(sy, sx + 1, "---", curses.color_pair(1))
            else:
                # GAP LOGIC: If I am on path AND North neighbor is on path -> Color the gap
                if is_path and (y - 1, x) in path_coords:
                    stdscr.addstr(sy, sx + 1, "   ", curses.color_pair(2))
                else:
                    stdscr.addstr(sy, sx + 1, "   ")

            if cell_value & WEST:
                stdscr.addstr(sy + 1, sx, "|", curses.color_pair(1))
            else:
                # GAP LOGIC: If I am on path AND West neighbor is on path -> Color the gap
                if is_path and (y, x - 1) in path_coords:
                    stdscr.addstr(sy + 1, sx, " ", curses.color_pair(2))
                else:
                    stdscr.addstr(sy + 1, sx, " ")

            if x == maze_obj.width - 1:
                stdscr.addstr(sy, sx + 4, "+", curses.color_pair(1)) # top right corner
                if cell_value & EAST:
                    stdscr.addstr(sy + 1, sx + 4, "|", curses.color_pair(1))
            
            if y == maze_obj.height - 1:
                stdscr.addstr(sy + 2, sx, "+", curses.color_pair(1)) # bottom left corner
                if cell_value & SOUTH:
                    stdscr.addstr(sy + 2, sx + 1, "---", curses.color_pair(1))

            # Draw the other corners to seal each cell
            stdscr.addstr(sy, sx + 4, "+", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx, "+", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx + 4, "+", curses.color_pair(1))

def run_visualizer(maze_obj, entry, exit, path_str=""):
    curses.wrapper(lambda stdscr: _visualizer_logic(stdscr, maze_obj, entry, exit, path_str))

def _visualizer_logic(stdscr, maze_obj, entry, exit, path_str):
    curses.start_color()
    # Color Pair 1 = Green Text on Magenta Background
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
    # Color Pair 2 = Cyan Text on Black Background
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
    # Color Pair 3 = 42 Pattern Colors
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    # Color Pair 4 = Exit
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Color Pair 5 = Entry
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Calculate path coordinates
    path_coords = get_path_coordinates(entry, path_str)

    stdscr.clear()
    draw_maze(stdscr, maze_obj, entry, exit, path_coords)
    
    # UI Message at the bottom
    msg_y = (maze_obj.height * 2) + 1
    stdscr.addstr(msg_y, 0, "Press any key to exit...")
    
    stdscr.refresh()
    stdscr.getch()