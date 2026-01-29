from typing import Tuple
from mazegen.maze import Maze


def write_output(maze: Maze, entry: Tuple[int, int], exit_: Tuple[int, int],
                 output_file: str, path: str = "") -> None:
    """
    Write maze to output file.

    Args:
        maze: The Maze object
        entry: (y, x) coordinates of entry
        exit: (y, x) coordinates of exit
        output_file: Path to output file
        path: Solution path string (e.g., "NNEESW") - empty for now
    """
    with open(output_file, 'w') as f:
        # Hexadecimal maze data
        f.write(maze.to_hex_string())
        f.write("\n\n")

        # Add metadata to the file (entry, exit, path)
        # write the entry coordinate (x,y) format as in the subject
        entry_y, entry_x = entry
        f.write(f"{entry_x}, {entry_y}\n")

        # write the entry coordinate (x,y) format as in the subject
        exit_y, exit_x = exit_
        f.write(f"{exit_x}, {exit_y}\n")

        # write path
        f.write(f"{path}\n")
