from typing import Tuple, Dict, Set
from collections import deque
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST


def bfs(maze: Maze, entry: Tuple[int, int],
        exit_: Tuple[int, int]) -> str:
    """Find the shortes path between entry and exit using BFS
    Args:
        - Maze: The maze object
        - Entry: tuple for START coodinates (y, x)
        - Exit: tuple for EXIT coodinates (y, x)
    Returns:
        String of directions: "N" (North), "E" (East), "S" (South), "W" (West)
        Example: "NNEESW" means: go North, North, East, East, South, West
    """
    entry_y, entry_x = entry
    exit_y, exit_x = exit_

    # 1 - Creating the data structures:
    #   - deque (double ended queue) for fast storing path
    #   - set for storing visited cell
    queue = deque()
    visited = set()

    # 2 - initialize
    queue.append((entry_y, entry_x, ""))
    visited.add((entry_y, entry_x))

    # main loop:
    while len(queue) != 0:
        # Get next position to explore
        current_y, current_x, path = queue.popleft()

        # if we reach the goal
        if (current_y, current_x) == (exit_y, exit_x):
            return path

        # check every direction
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

    # if no path found, return empty string
    return ""
