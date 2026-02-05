"""
mazegen - A maze generator using Hunt and Kill algorithm.

INSTALLATION
------------
    pip install mazegen-1.0.0-py3-none-any.whl

BASIC USAGE
-----------
    from mazegen import MazeGenerator, bfs

    # 1. Instantiate the generator with custom parameters
    gen = MazeGenerator(width=20, height=20, seed=42)

    # 2. Generate the maze (returns a Maze object)
    maze = gen.generate()

    # 3. Find a path from entry to exit
    path = bfs(maze, entry=(0, 0), exit_=(19, 19))
    print(f"Path: {path}")  # e.g., "EESSSWW..."

PARAMETERS
----------
    width : int
        Maze width in cells
    height : int
        Maze height in cells
    seed : int, optional
        Random seed for reproducibility
    algorithm : str, optional
        Generation algorithm: "hunt_and_kill" (default)
                              or "recursive_backtracker"

ACCESSING THE MAZE STRUCTURE
----------------------------
    # Get maze dimensions
    maze.width, maze.height

    # Get cell value (wall flags as integer)
    cell_value = maze.get_cell_value(y, x)

    # Check if wall exists in a direction
    from mazegen import NORTH, EAST, SOUTH, WEST
    has_wall = maze.has_wall(y, x, NORTH)

GETTING A SOLUTION
------------------
    from mazegen import bfs, dfs

    # BFS finds the SHORTEST path
    path = bfs(maze, entry=(0, 0), exit_=(19, 19))

    # DFS finds ANY path (not necessarily shortest)
    path = dfs(maze, entry=(0, 0), exit_=(19, 19))

    # Path is a string of directions: "N", "E", "S", "W"
"""

from .generator import MazeGenerator
from .maze import Maze, NORTH, EAST, SOUTH, WEST
from .pathfinding import bfs, dfs

__version__ = "1.0.0"
__all__ = [
    "MazeGenerator",
    "Maze",
    "bfs",
    "dfs",
    "NORTH",
    "EAST",
    "SOUTH",
    "WEST",
]
