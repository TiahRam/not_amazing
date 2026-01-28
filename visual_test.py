#!/usr/bin/env python3
# test_maze.py
import curses
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST # noqa

maze = Maze(5, 5) 

# 1. Create the Entrance & Top-Left Pocket
maze.remove_wall_between(0, 0, 1, 0)  # Down from Start
maze.remove_wall_between(1, 0, 1, 1)  # Right
maze.remove_wall_between(1, 1, 0, 1)  # Up (Dead End at 0,1)

# 2. The Upper Corridor (Top Right)
maze.remove_wall_between(0, 2, 0, 3)  # Right
maze.remove_wall_between(0, 3, 0, 4)  # Right (Top Right Corner)
maze.remove_wall_between(0, 4, 1, 4)  # Down
maze.remove_wall_between(1, 4, 1, 3)  # Left (Dead End at 1,3)

# 3. The Central Spine (Connecting the middle)
maze.remove_wall_between(1, 1, 1, 2)  # Right (Connecting Left Pocket to Center)
maze.remove_wall_between(1, 2, 0, 2)  # Up (Connecting to Top Corridor)
maze.remove_wall_between(1, 2, 2, 2)  # Down (Center of Maze)

# 4. The Bottom Left Section
maze.remove_wall_between(2, 2, 2, 1)  # Left
maze.remove_wall_between(2, 1, 2, 0)  # Left (Dead End at 2,0)
maze.remove_wall_between(2, 1, 3, 1)  # Down
maze.remove_wall_between(3, 1, 3, 0)  # Left (Dead End at 3,0)

# 5. The Path to Exit (Bottom Right)
maze.remove_wall_between(2, 2, 2, 3)  # Right from Center
maze.remove_wall_between(2, 3, 3, 3)  # Down
maze.remove_wall_between(3, 3, 3, 2)  # Left (Dead End at 3,2)
maze.remove_wall_between(3, 3, 3, 4)  # Right
maze.remove_wall_between(3, 4, 4, 4)  # Down (Exit at 4,4)

# 6. Final Twist (Bottom Middle)
maze.remove_wall_between(4, 4, 4, 3)  # Left
maze.remove_wall_between(4, 3, 4, 2)  # Left (Dead End at 4,2)



# =====================================================================================

import curses
from mazegen.maze import Maze, NORTH, SOUTH, EAST, WEST

def draw_maze(stdscr, maze_obj):
    curses.curs_set(0)

    for y in range(maze_obj.height):
        for x in range(maze_obj.width):
            cell_value = maze_obj.get_cell_value(y, x)
            
            sy = y * 2
            sx = x * 3
            

            stdscr.addstr(sy, sx, " ", curses.color_pair(1))

            if cell_value & NORTH:
                stdscr.addstr(sy, sx + 1, "  ", curses.color_pair(1))
            else:
                stdscr.addstr(sy, sx + 1, "  ")

            if cell_value & WEST:
                stdscr.addstr(sy + 1, sx, " ", curses.color_pair(1))
            else:
                stdscr.addstr(sy + 1, sx, " ")

            if cell_value & EAST:
                stdscr.addstr(sy + 1, sx + 3, " ", curses.color_pair(1))
                
            if cell_value & SOUTH:
                 stdscr.addstr(sy + 2, sx + 1, "  ", curses.color_pair(1))

            stdscr.addstr(sy, sx + 3, " ", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx, " ", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx + 3, " ", curses.color_pair(1))

def run_visualizer(maze_obj):
    curses.wrapper(lambda stdscr: _visualizer_logic(stdscr, maze_obj))

def _visualizer_logic(stdscr, maze_obj):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    
    stdscr.clear()
    draw_maze(stdscr, maze_obj)
    stdscr.addstr(22, 0, "press kboard to end or some shit...")
    stdscr.refresh()
    stdscr.getch()

run_visualizer(maze)

# smol edit to make sure we can pull