"""Pathfinding algorithms for maze solving."""

from typing import Tuple, Dict, Set, List
from collections import deque
from .maze import Maze, NORTH, EAST, SOUTH, WEST


def bfs(maze: Maze, entry: Tuple[int, int],
        exit_: Tuple[int, int]) -> str:
    """Find the shortest path between entry and exit using BFS.
    Args:
        maze: The Maze object
        entry: tuple for START coordinates (y, x)
        exit_: tuple for EXIT coordinates (y, x)
    Returns:
        String of directions: "N" (North), "E" (East), "S" (South), "W" (West)
        Example: "NNEESW" means: go North, North, East, East, South, West
    """
    entry_y, entry_x = entry
    exit_y, exit_x = exit_

    queue: deque[Tuple[int, int, str]] = deque()
    visited: Set[Tuple[int, int]] = set()

    queue.append((entry_y, entry_x, ""))
    visited.add((entry_y, entry_x))

    while len(queue) != 0:
        current_y, current_x, path = queue.popleft()

        if (current_y, current_x) == (exit_y, exit_x):
            return path

        # NORTH
        if not maze.has_wall(current_y, current_x, NORTH):
            neighbor_y = current_y - 1
            neighbor_x = current_x
            if (0 <= neighbor_y < maze.height and 0 <= neighbor_x < maze.width
                    and (neighbor_y, neighbor_x) not in visited):
                visited.add((neighbor_y, neighbor_x))
                queue.append((neighbor_y, neighbor_x, path + "N"))
        # EAST
        if not maze.has_wall(current_y, current_x, EAST):
            neighbor_y = current_y
            neighbor_x = current_x + 1
            if (0 <= neighbor_y < maze.height and 0 <= neighbor_x < maze.width
                    and (neighbor_y, neighbor_x) not in visited):
                visited.add((neighbor_y, neighbor_x))
                queue.append((neighbor_y, neighbor_x, path + "E"))
        # SOUTH
        if not maze.has_wall(current_y, current_x, SOUTH):
            neighbor_y = current_y + 1
            neighbor_x = current_x
            if (0 <= neighbor_y < maze.height and 0 <= neighbor_x < maze.width
                    and (neighbor_y, neighbor_x) not in visited):
                visited.add((neighbor_y, neighbor_x))
                queue.append((neighbor_y, neighbor_x, path + "S"))
        # WEST
        if not maze.has_wall(current_y, current_x, WEST):
            neighbor_y = current_y
            neighbor_x = current_x - 1
            if (0 <= neighbor_y < maze.height and 0 <= neighbor_x < maze.width
                    and (neighbor_y, neighbor_x) not in visited):
                visited.add((neighbor_y, neighbor_x))
                queue.append((neighbor_y, neighbor_x, path + "W"))

    return ""


def dfs(maze: Maze, entry: Tuple[int, int],
        exit_: Tuple[int, int]) -> str:
    """Find a path from entry to exit using Depth-First Search.
    Note: DFS does NOT guarantee shortest path.
    Args:
        maze: The Maze object
        entry: (y, x) coordinates of entry
        exit_: (y, x) coordinates of exit
    Returns:
        Path string (e.g., "NNEESW") or empty string if no path
    """
    stack: List[Tuple[int, int, str]] = [(entry[0], entry[1], "")]
    visited: Set[Tuple[int, int]] = {entry}

    directions: Dict[int, Tuple[int, int, str]] = {
        NORTH: (-1, 0, 'N'),
        EAST:  (0, 1, 'E'),
        SOUTH: (1, 0, 'S'),
        WEST:  (0, -1, 'W')
    }

    while stack:
        current_y, current_x, path = stack.pop()

        if (current_y, current_x) == exit_:
            return path

        for wall, (dy, dx, char) in directions.items():
            if maze.has_wall(current_y, current_x, wall):
                continue

            next_y = current_y + dy
            next_x = current_x + dx

            if (0 <= next_y < maze.height and
                    0 <= next_x < maze.width and
                    (next_y, next_x) not in visited):
                visited.add((next_y, next_x))
                stack.append((next_y, next_x, path + char))

    return ""
