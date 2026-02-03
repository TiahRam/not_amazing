from typing import Tuple, Dict, Set, List
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST


def dfs(maze: Maze, entry: Tuple[int, int],
        exit_: Tuple[int, int]) -> str:
    """
    Find a path from entry to exit using Depth-First Search.
    Note: DFS does NOT guarantee shortest path.
    Args:
        maze: The Maze object
        entry: (y, x) coordinates of entry
        exit_: (y, x) coordinates of exit
    Returns:
        Path string (e.g., "NNEESW") or empty string if no path
    """
    # Stack: (y, x, path_string)
    stack: List[Tuple] = [(entry[0], entry[1], "")]

    # Track visited cells
    visited: Set[Tuple[int, int]] = {entry}

    # Direction mappings: direction -> (dy, dx, char)
    directions: Dict[str, Tuple[int, int, str]] = {
        NORTH: (-1, 0, 'N'),
        EAST:  (0, 1, 'E'),
        SOUTH: (1, 0, 'S'),
        WEST:  (0, -1, 'W')
    }

    while stack:
        # Pop from stack (DFS uses LIFO)
        current_y, current_x, path = stack.pop()

        # Check if we reached exit
        if (current_y, current_x) == exit_:
            return path

        # Explore neighbors
        for wall, (dy, dx, char) in directions.items():
            # Check if wall exists in given direction
            if maze.has_wall(current_y, current_x, wall):
                continue

            # Calculate neighbor
            next_y = current_y + dy
            next_x = current_x + dx

            # Check bounds and visited
            if (0 <= next_y < maze.height and
                0 <= next_x < maze.width and
                (next_y, next_x) not in visited):
                # Mark visited and push to stack
                visited.add((next_y, next_x))
                stack.append((next_y, next_x, path + char))

    # No path found
    return ""
