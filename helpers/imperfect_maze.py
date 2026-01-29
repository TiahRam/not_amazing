import random
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST


def add_random_loops(maze: Maze, num_loops: int = 5) -> None:
    """
    Add random passages to create loops (imperfect maze).

    This breaks down random walls to create multiple paths between
    any two points, making the maze imperfect.

    Args:
        maze: The Maze object to modify
        num_loops: Number of extra passages to add (default: 5)
    """
    added = 0
    attempts = 0
    max_attempts = num_loops * 20

    while added < num_loops and attempts < max_attempts:
        attempts += 1

        # Pick random cell
        y = random.randint(0, maze.height - 1)
        x = random.randint(0, maze.width - 1)

        # Get all possible neighbors
        possible_walls = []

        if y > 0 and maze.has_wall(y, x, NORTH):
            possible_walls.append(('N', y - 1, x, NORTH))
        if x < maze.width - 1 and maze.has_wall(y, x, EAST):
            possible_walls.append(('E', y, x + 1, EAST))
        if y < maze.height - 1 and maze.has_wall(y, x, SOUTH):
            possible_walls.append(('S', y + 1, x, SOUTH))
        if x > 0 and maze.has_wall(y, x, WEST):
            possible_walls.append(('W', y, x - 1, WEST))

        # If this cell has walls to remove, pick one
        if possible_walls:
            direction, ny, nx, wall = random.choice(possible_walls)
            maze.remove_wall_between(y, x, ny, nx)
            added += 1
