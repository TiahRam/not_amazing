from typing import Tuple, Optional, List
from mazegen.maze import Maze
from mazegen.maze import NORTH, EAST, SOUTH, WEST


def get_path_cells(entry: Tuple[int, int], path_string: str) -> set:
    """
    Convert path string to set of (y, x) coordinates.
    Args:
        entry: Starting position (y, x)
        path_string: String of directions (N, E, S, W)
    Returns:
        Set of (y, x) tuples representing all cells in the path
    Example:
        {(0, 0), (0, 1), (1, 1), (2, 1)}
    """
    path_cells = set()
    current_y, current_x = entry
    path_cells.add((current_y, current_x))

    # check for every possible direction
    for direction in path_string:
        if direction == 'N':
            current_y = current_y - 1
        elif direction == 'E':
            current_x = current_x + 1
        elif direction == 'S':
            current_y = current_y + 1
        elif direction == 'W':
            current_x = current_x - 1

        path_cells.add((current_y, current_x))
    return path_cells


def is_valid_position(top_y: int, top_x: int, pattern: List[List[int]],
                      path_cells: set, entry: Tuple[int, int],
                      exit_: Tuple[int, int],
                      maze: Maze) -> bool:
    """
    Check if pattern can be placed at the given position.
    Args:
        top_y: Top-left Y coordinate for pattern placement
        top_x: Top-left X coordinate for pattern placement
        pattern: 2D list where 1 = filled cell, 0 = empty
        path_cells: Set of cells that are part of the solution path
        entry: Entry position (y, x)
        exit_: Exit position (y, x)
        maze: The maze object
    Returns:
        True if pattern can be safely placed, False otherwise
    """
    pattern_height = len(pattern)
    pattern_width = len(pattern[0])

    for y in range(pattern_height):
        for x in range(pattern_width):

            if pattern[y][x] == 1:
                maze_y = top_y + y
                maze_x = top_x + x

                # Check bounds
                if maze_y >= maze.height or maze_x >= maze.width:
                    return False
                # Check if on solution path
                if (maze_y, maze_x) in path_cells:
                    return False
                # Check if on entry/exit
                if (maze_y, maze_x) == entry or (maze_y, maze_x) == exit_:
                    return False

    return True


def find_safe_location(maze: Maze, pattern: List[List[int]], path_cells: set,
                       entry: Tuple[int, int],
                       exit_: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """
    Find a safe location to place the pattern.
    Args:
        maze: The maze object
        pattern: 2D list representing the pattern to place
        path_cells: Set of cells on the solution path
        entry: Entry position (y, x)
        exit_: Exit position (y, x)
    Returns:
        (y, x) tuple for top-left corner of valid placement
        None if no valid position
    """
    pattern_height = len(pattern)
    pattern_width = len(pattern[0])

    for y in range(maze.height - pattern_height + 1):
        for x in range(maze.width - pattern_width + 1):
            if is_valid_position(y, x, pattern, path_cells,
                                 entry, exit_, maze):
                return (y, x)

    return None


def place_pattern(maze: Maze, pattern: List[List[int]],
                  top_y: int, top_x: int) -> None:
    """
    Place the pattern on the maze by closing all walls in pattern cells.

    Args:
        maze: The maze object to modify
        pattern: 2D list where 1 = place obstacle, 0 = skip
        top_y: Top-left Y coordinate for placement
        top_x: Top-left X coordinate for placement
    Returns:
        None, modified cell internally
    """
    pattern_height = len(pattern)
    pattern_width = len(pattern[0])

    for y in range(pattern_height):
        for x in range(pattern_width):
            if pattern[y][x] == 1:
                maze_y = top_y + y
                maze_x = top_x + x
                maze.grid[maze_y][maze_x] = 0xF
                # Update neighbors to close their walls facing this cell
                # NORTH neighbor
                if maze_y > 0:
                    maze.grid[maze_y - 1][maze_x] |= SOUTH

                # SOUTH neighbor
                if maze_y < maze.height - 1:
                    maze.grid[maze_y + 1][maze_x] |= NORTH

                # WEST neighbor
                if maze_x > 0:
                    maze.grid[maze_y][maze_x - 1] |= EAST

                # EAST neighbor
                if maze_x < maze.width - 1:
                    maze.grid[maze_y][maze_x + 1] |= WEST


def place_42_pattern(maze: Maze, path_string: str, entry: Tuple[int, int],
                     exit_: Tuple[int, int]) -> bool:
    """
    Place a '42' pattern on the maze without blocking the solution path.
    The pattern is placed at the first valid location found, which avoids:
    - Overlapping with the solution path
    - Blocking entry or exit points
    - Extending beyond maze boundaries
    Args:
        maze: The maze object to modify
        path_string: Solution path as a string of directions (N, E, S, W)
        entry: Entry position (y, x)
        exit_: Exit position (y, x)
    Returns:
        True if pattern was successfully placed, False otherwise
    """

    pattern = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]
    path_cells = get_path_cells(entry, path_string)
    position = find_safe_location(maze, pattern, path_cells, entry, exit_)

    if position is None:
        return False

    top_y, top_x = position
    place_pattern(maze, pattern, top_y, top_x)
    return True
