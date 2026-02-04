import random
from typing import Optional, Any
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST


def add_random_loops(maze: Maze, num_loops: int = 5,
                     blocked_cells: Optional[Any] = None) -> None:
    """
    Add random loops by removing walls.
    Args:
        maze: Maze object
        num_loops: Number of loops to add
        blocked_cells: Set of (y, x) cells to avoid (e.g., 42 pattern)
    """
    if blocked_cells is None:
        blocked_cells = set()

    added = 0
    attempts = 0
    max_attempts = num_loops * 20

    while added < num_loops and attempts < max_attempts:
        attempts += 1

        # Pick random cell
        y = random.randint(0, maze.height - 1)
        x = random.randint(0, maze.width - 1)

        # Skip blocked cells
        if (y, x) in blocked_cells:
            continue

        # Get all possible neighbors
        possible_walls = []

        if y > 0 and maze.has_wall(y, x, NORTH):
            ny, nx = y - 1, x
            if (ny, nx) not in blocked_cells:
                possible_walls.append(('N', ny, nx, NORTH))

        if x < maze.width - 1 and maze.has_wall(y, x, EAST):
            ny, nx = y, x + 1
            if (ny, nx) not in blocked_cells:
                possible_walls.append(('E', ny, nx, EAST))

        if y < maze.height - 1 and maze.has_wall(y, x, SOUTH):
            ny, nx = y + 1, x
            if (ny, nx) not in blocked_cells:
                possible_walls.append(('S', ny, nx, SOUTH))

        if x > 0 and maze.has_wall(y, x, WEST):
            ny, nx = y, x - 1
            if (ny, nx) not in blocked_cells:
                possible_walls.append(('W', ny, nx, WEST))

        # If this cell has walls to remove, pick one
        if possible_walls:
            direction, ny, nx, wall = random.choice(possible_walls)
            maze.remove_wall_between(y, x, ny, nx)
            added += 1
