#!/usr/bin/env python3


from typing import Tuple
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST


def add_entry_exit(maze: Maze, entry: Tuple[int, int],
                   exit_: Tuple[int, int]) -> None:
    """
    Open walls at entry and exit points.

    Args:
        maze: The Maze object
        entry: (y, x) coordinates of entry
        exit: (y, x) coordinates of exit
    """
    entry_y, entry_x = entry
    exit_y, exit_x = exit_

    # ENTRY: Check which border it is and open wall
    # if Top border
    if entry_y == 0:
        maze.grid[entry_y][entry_x] &= ~NORTH
    # if bottom border
    elif entry_y == maze.height - 1:
        maze.grid[entry_y][entry_x] &= ~SOUTH
    # if left border
    elif entry_x == 0:
        maze.grid[entry_y][entry_x] &= ~WEST
    # if right border
    elif entry_x == maze.width - 1:
        maze.grid[entry_y][entry_x] &= ~EAST

    # EXIT: Check which border it is and open wall
    # if Top border
    if exit_y == 0:
        maze.grid[exit_y][exit_x] &= ~NORTH
    # if bottom border
    elif exit_y == maze.height - 1:
        maze.grid[exit_y][exit_x] &= ~SOUTH
    # if left border
    elif exit_x == 0:
        maze.grid[exit_y][exit_x] &= ~WEST
    # if right border
    elif exit_x == maze.width - 1:
        maze.grid[exit_y][exit_x] &= ~EAST


# def write_output(maze: Maze, entry: Tuple[int, int], exit_: Tuple[int, int],
#                  output_file: str, path: str = "") -> None:
#     """
#     Write maze to output file.

#     Args:
#         maze: The Maze object
#         entry: (y, x) coordinates of entry
#         exit: (y, x) coordinates of exit
#         output_file: Path to output file
#         path: Solution path string (e.g., "NNEESW") - empty for now
#     """
#     with open(output_file, 'w') as f:
#         # Hexadecimal maze data
#         f.write(maze.to_hex_string())
#         f.write("\n\n")

#         # Add metadata to the file (entry, exit, path)
#         # write the entry coordinate (x,y) format as in the subject
#         entry_y, entry_x = entry
#         f.write(f"{entry_x}, {entry_y}\n")

#         # write the entry coordinate (x,y) format as in the subject
#         exit_y, exit_x = exit_
#         f.write(f"{exit_x}, {exit_y}\n")

#         # write path
#         f.write(f"{path}\n")
