#!/usr/bin/env python3

import curses
import pyfiglet
from typing import Tuple, List, Any
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST  # noqa
from helpers.entry_and_exit import add_entry_exit
from mazegen.pathfinding import bfs
from mazegen.generator import MazeGenerator
from helpers.imperfect_maze import add_random_loops


def get_path_coordinates(entry: Tuple[int, int],
                         path_str: Any) -> List[Tuple[int, int]]:
    coords = []
    curr_y, curr_x = entry
    coords.append((curr_y, curr_x))  # Add start
    for move in path_str:
        if move == "N":
            curr_y -= 1
        elif move == "S":
            curr_y += 1
        elif move == "E":
            curr_x += 1
        elif move == "W":
            curr_x -= 1
        coords.append((curr_y, curr_x))
    return coords


def animate_solution(stdscr: Any, maze_obj: Maze,
                     entry: Tuple[int, int], exit: Tuple[int, int],
                     path_coords_list: List[Tuple[int, int]]) -> None:
    # First, ensure the maze is drawn CLEAN
    stdscr.clear()
    draw_maze(stdscr, maze_obj, entry, exit, set())
    stdscr.refresh()

    path_pair = curses.color_pair(2)
    if not path_coords_list:
        return

    # Start with the first cell
    prev_y, prev_x = path_coords_list[0]
    # Draw Start cell center
    sy = prev_y * 2
    sx = prev_x * 4
    stdscr.addstr(sy + 1, sx + 1, "   ", path_pair)
    stdscr.refresh()
    curses.napms(30)

    # Loop starting from the second step
    for i in range(1, len(path_coords_list)):
        curr_y, curr_x = path_coords_list[i]
        sy = curr_y * 2
        sx = curr_x * 4

        # 1. Draw Center of the new cell
        stdscr.addstr(sy + 1, sx + 1, "   ", path_pair)

        # 2. Draw Connection (The Pierced Wall) to create a full line
        # Check relation to previous cell to know which wall to paint over

        # Moving South (Previous was above) -> Fill North Gap of Current
        if curr_y > prev_y:
            stdscr.addstr(sy, sx + 1, "   ", path_pair)

        # Moving North (Previous was below) -> Fill North Gap of Previous
        elif curr_y < prev_y:
            prev_sy = prev_y * 2
            prev_sx = prev_x * 4
            stdscr.addstr(prev_sy, prev_sx + 1, "   ", path_pair)

        # Moving East (Previous was left) -> Fill West Gap of Current
        elif curr_x > prev_x:
            stdscr.addstr(sy + 1, sx, " ", path_pair)

        # Moving West (Previous was right) -> Fill West Gap of Previous
        elif curr_x < prev_x:
            prev_sy = prev_y * 2
            prev_sx = prev_x * 4
            stdscr.addstr(prev_sy + 1, prev_sx, " ", path_pair)

        stdscr.refresh()
        curses.napms(20)  # Delay for effect

        prev_y, prev_x = curr_y, curr_x


def draw_maze(stdscr: Any, maze_obj: Maze, entry: Tuple[int, int],
              exit: Tuple[int, int], path_coords: Any) -> None:
    curses.curs_set(0)  # Hides our terminal cursor

    max_y, max_x = stdscr.getmaxyx()
    needed_y = maze_obj.height * 2 + 2
    needed_x = maze_obj.width * 4 + 2

    if max_y < needed_y or max_x < needed_x:
        stdscr.addstr(
            0, 0, f"Error: Terminal too small! Need " f"{needed_x}x{needed_y}"
        )
        return

    # Our sacred loop
    for y in range(maze_obj.height):
        for x in range(maze_obj.width):
            cell_value = maze_obj.get_cell_value(y, x)

            # Coordinate offsetting
            sy = y * 2
            sx = x * 4

            # If cell is in 42 pattern
            is_pattern_block = cell_value == 0xF

            # If cell is in path_coords
            is_path = (y, x) in path_coords

            # We check if this (y, x) is in our path set
            if is_pattern_block:
                stdscr.addstr(sy + 1, sx + 1, "   ", curses.color_pair(3))
            else:
                if (y, x) in path_coords:
                    stdscr.addstr(sy + 1, sx + 1, "   ", curses.color_pair(2))

                if (y, x) == entry:
                    stdscr.addstr(sy + 1, sx + 1, "▄▀▄", curses.color_pair(5))
                if (y, x) == exit:
                    stdscr.addstr(sy + 1, sx + 1, "▄▀▄", curses.color_pair(4))

            # Anchors (top left corner)
            stdscr.addstr(sy, sx, " ", curses.color_pair(1))

            # Drawing walls based on bitwise checks
            if cell_value & NORTH:
                stdscr.addstr(sy, sx + 1, "   ", curses.color_pair(1))
            else:
                # GAP: color If I am on path AND North neighbor is on path
                if is_path and (y - 1, x) in path_coords:
                    stdscr.addstr(sy, sx + 1, "   ", curses.color_pair(2))
                else:
                    stdscr.addstr(sy, sx + 1, "   ")

            if cell_value & WEST:
                stdscr.addstr(sy + 1, sx, " ", curses.color_pair(1))
            else:
                # GAP: color If I am on path AND West neighbor is on path
                if is_path and (y, x - 1) in path_coords:
                    stdscr.addstr(sy + 1, sx, " ", curses.color_pair(2))
                else:
                    stdscr.addstr(sy + 1, sx, " ")

            if x == maze_obj.width - 1:
                stdscr.addstr(
                    sy, sx + 4, " ", curses.color_pair(1)
                )  # top right corner
                if cell_value & EAST:
                    stdscr.addstr(sy + 1, sx + 4, " ", curses.color_pair(1))

            if y == maze_obj.height - 1:
                stdscr.addstr(
                    sy + 2, sx, " ", curses.color_pair(1)
                )  # bottom left corner
                if cell_value & SOUTH:
                    stdscr.addstr(sy + 2, sx + 1, "   ", curses.color_pair(1))

            # Draw the other corners to seal each cell
            stdscr.addstr(sy, sx + 4, " ", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx, " ", curses.color_pair(1))
            stdscr.addstr(sy + 2, sx + 4, " ", curses.color_pair(1))


def run_visualizer(perfect: bool, generator: MazeGenerator, maze_obj: Maze,
                   entry: Tuple[int, int], exit: Tuple[int, int],
                   path_str: Any = "") -> None:
    curses.wrapper(
        lambda stdscr: _visualizer_logic(
            perfect, generator, stdscr, maze_obj, entry, exit, path_str
        )
    )


def _visualizer_logic(perfect: bool, generator: MazeGenerator, stdscr: Any,
                      maze_obj: Maze, entry: Tuple[int, int],
                      exit: Tuple[int, int],
                      path_str: Any) -> None:
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
    # Color Pair 6 = Green Text on Magenta Background
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # State variables for menu options
    show_solution = True
    wall_color_index = 0
    pattern_color_index = 0
    path_color_index = 0

    # Color options for walls (foreground, background)
    wall_colors = [
        (curses.COLOR_BLUE, curses.COLOR_BLUE),
        (curses.COLOR_WHITE, curses.COLOR_WHITE),
        (curses.COLOR_CYAN, curses.COLOR_CYAN),
        (curses.COLOR_YELLOW, curses.COLOR_YELLOW),
        (curses.COLOR_MAGENTA, curses.COLOR_MAGENTA),
    ]

    # Color options for 42 pattern (foreground, background)
    pattern_colors = [
        (curses.COLOR_RED, curses.COLOR_WHITE),
        (curses.COLOR_WHITE, curses.COLOR_RED),
        (curses.COLOR_BLACK, curses.COLOR_YELLOW),
        (curses.COLOR_BLUE, curses.COLOR_WHITE),
        (curses.COLOR_GREEN, curses.COLOR_BLACK),
    ]

    # Color options for solution path
    path_colors = [
        (curses.COLOR_MAGENTA, curses.COLOR_MAGENTA),
        (curses.COLOR_WHITE, curses.COLOR_WHITE),
        (curses.COLOR_CYAN, curses.COLOR_CYAN),
        (curses.COLOR_YELLOW, curses.COLOR_YELLOW),
        (curses.COLOR_BLUE, curses.COLOR_BLUE),
    ]

    # Calculate path coordinates
    path_coords_list = get_path_coordinates(entry, path_str)
    path_coords_set = set(path_coords_list)
    # Check terminal size
    max_y, max_x = stdscr.getmaxyx()
    needed_y = maze_obj.height * 2 + 10  # maze + menu space
    needed_x = maze_obj.width * 4 + 2

    if max_y < needed_y or max_x < needed_x:
        stdscr.addstr(
            0, 0, f"Error: Terminal too small! Need {needed_x}x{needed_y}"
        )
        stdscr.addstr(1, 0, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()
        return

    # title screen on startup
    result = pyfiglet.figlet_format("a-maze-ing", font="slant")
    stdscr.addstr(result, curses.color_pair(6) | curses.A_BOLD)
    stdscr.addstr("\nProject by: ")
    stdscr.addstr(
        "mramidam & mnassiri",
        curses.A_BLINK | curses.A_BOLD | curses.color_pair(6),
    )
    stdscr.addstr("\n\nPRESS ANY KEY TO START...")
    stdscr.getch()
    stdscr.refresh()
    stdscr.clear()

    # solution animation on startup
    if show_solution:
        animate_solution(stdscr, maze_obj, entry, exit, path_coords_list)

    # Main loop
    while True:
        # Update color pairs based on current selections
        fg, bg = wall_colors[wall_color_index]
        curses.init_pair(1, fg, bg)
        fg, bg = pattern_colors[pattern_color_index]
        curses.init_pair(3, fg, bg)
        fg, bg = path_colors[path_color_index]
        curses.init_pair(2, fg, bg)

        stdscr.clear()

        # Draw maze with or without solution based on show_solution
        if show_solution:
            draw_maze(stdscr, maze_obj, entry, exit, path_coords_set)
        else:
            draw_maze(stdscr, maze_obj, entry, exit, set())

        # Menu at the bottom
        msg_y = (maze_obj.height * 2) + 1
        stdscr.addstr(msg_y + 1, 0, "1. Re-generate a mew maze", curses.A_BOLD)
        stdscr.addstr(msg_y + 2, 0, "2. Show/Hide the solution", curses.A_BOLD)
        stdscr.addstr(
            msg_y + 3, 0, "3. Change maze wall colors", curses.A_BOLD
        )
        stdscr.addstr(
            msg_y + 4, 0, '4. Change "42" Pattern colors', curses.A_BOLD
        )
        stdscr.addstr(
            msg_y + 5, 0, "5. Change solution path colors", curses.A_BOLD
        )
        stdscr.addstr(msg_y + 6, 0, "6. Play StarWars lmao", curses.A_BOLD)
        stdscr.addstr(msg_y + 8, 0, "Press any other key to exit...")
        if not generator.place_42_pattern():
            stdscr.addstr(
                msg_y,
                0,
                "Cannot place '42' pattern: Maze too small!",
                curses.A_BOLD | curses.A_BLINK | curses.color_pair(5),
            )

        stdscr.refresh()
        key = stdscr.getch()

        if key == ord("1"):
            # Re-generate a new maze
            generator._pattern_42_cells = set()
            maze_obj = generator.generate()
            add_entry_exit(maze_obj, entry, exit)
            if not perfect:
                pattern_cells = generator.get_pattern_42_cells()
                loop_number = (maze_obj.width * maze_obj.height) // 10
                add_random_loops(maze_obj, loop_number, pattern_cells)
            path_str = bfs(maze_obj, entry, exit)

            # Recalculate coordinates
            path_coords_list = get_path_coordinates(entry, path_str)
            path_coords_set = set(path_coords_list)

            # --- ANIMATE SOLUTION ONLY ---
            if show_solution:
                animate_solution(
                    stdscr, maze_obj, entry, exit, path_coords_list
                )

        elif key == ord("2"):
            # Toggle solution visibility
            show_solution = not show_solution
        elif key == ord("3"):
            # Cycle wall colors
            wall_color_index = (wall_color_index + 1) % len(wall_colors)
        elif key == ord("4"):
            # Cycle 42 pattern colors
            pattern_color_index = (pattern_color_index + 1) % len(
                pattern_colors
            )
        elif key == ord("5"):
            # Cycle solution path colors
            path_color_index = (path_color_index + 1) % len(path_colors)
        else:
            # Any other key exits
            break
