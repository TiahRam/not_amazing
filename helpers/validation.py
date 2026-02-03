#!/usr/bin/env python3

from typing import Optional
from mazegen.maze import Maze


def validate_perfect_maze(maze: Maze,
                          blocked_cells: Optional[set] = None) -> bool:
    """
    Validate that maze is perfect (exactly one path between any two points).
    A perfect maze has exactly (width × height - 1) passages.
    Args:
        maze: The Maze object to validate
    Returns:
        True if maze is perfect, False otherwise
    """
    if blocked_cells is None:
        blocked_cells = set()

    total_cells = maze.width * maze.height
    navigable_cells = total_cells - len(blocked_cells)
    expected_passages = navigable_cells - 1

    # Count actual passages
    actual_passages = count_passages(maze)

    return actual_passages == expected_passages


def count_passages(maze: Maze) -> int:
    """
    Count total number of passages (removed walls) in the maze.
    Each passage is counted once (not twice from both sides).
    Args:
        maze: The Maze object
    Returns:
        Number of passages
    """
    passage_count = 0

    for y in range(maze.height):
        for x in range(maze.width):
            cell_value = maze.get_cell_value(y, x)

            # Count open walls (bit = 0 means wall is open)
            # We only count EAST and SOUTH to avoid double-counting
            # (Each passage connects 2 cells, we count from one side only)

            # Check if EAST wall is open (bit 1)
            if x < maze.width - 1:
                if not (cell_value & 0b0010):
                    passage_count += 1

            # Check if SOUTH wall is open (bit 2)
            if y < maze.height - 1:
                if not (cell_value & 0b0100):
                    passage_count += 1

    return passage_count


def get_validation_message(maze: Maze) -> str:
    """
    Get detailed validation message for debugging.
    Args:
        maze: The Maze object
    Returns:
        Formatted message string
    """
    total_cells = maze.width * maze.height
    expected_passages = total_cells - 1
    actual_passages = count_passages(maze)

    msg = "Maze Validation:\n"
    msg += f"- Total cells: {total_cells}\n"
    msg += f"- Expected passages (for perfect): {expected_passages}\n"
    msg += f"- Actual passages: {actual_passages}\n"

    if actual_passages == expected_passages:
        msg += "PERFECT MAZE!"
    elif actual_passages > expected_passages:
        extra = actual_passages - expected_passages
        msg += f"IMPERFECT MAZE (+{extra} extra passages = loops)"
    else:
        missing = expected_passages - actual_passages
        msg += f"INVALID MAZE (-{missing} passages = disconnected)"

    return msg
