#!/usr/bin/env python3


from typing import List, Dict, Any, Tuple, Optional # noqa


# Maze Wall using bit flags
# 1 is closed and 0 is open
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


class Maze:
    """Represents a maze grid with wall operations."""
    def __init__(self, height: int, width: int) -> None:
        """Maze Constructor"""
        self.height = height
        self.width = width

        # Fill all the grid with all closed wall
        self.grid: List[List[int]] = []
        for _ in range(height):
            row: List[int] = []
            for _ in range(width):
                row.append(0xF)
            self.grid.append(0xF)
        # self.grid: List[List[int]] = [[0xF for _ in range(width)]
        #                               for _ in range(height)]
        self.visited: List[List[bool]] = [[False for _ in range(width)]
                                          for _ in range(height)]

    # def has_wall(self, y: int, x: int, direction: int) -> bool:
    #     """Check if cell has a wall in given direction."""
    #     return bool(self.grid[y][x] & direction)

    # def remove_wall_between(self, y1: int, x1: int, y2: int, x2: int) -> None:
    #     """Remove wall between two adjacent cells."""
    #     dy = y2 - y1
    #     dx = x2 - x1

    #     if dy == -1:  # Neighbor is north
    #         self.grid[y1][x1] &= ~NORTH
    #         self.grid[y2][x2] &= ~SOUTH
    #     elif dy == 1:  # Neighbor is south
    #         self.grid[y1][x1] &= ~SOUTH
    #         self.grid[y2][x2] &= ~NORTH
    #     elif dx == 1:  # Neighbor is east
    #         self.grid[y1][x1] &= ~EAST
    #         self.grid[y2][x2] &= ~WEST
    #     elif dx == -1:  # Neighbor is west
    #         self.grid[y1][x1] &= ~WEST
    #         self.grid[y2][x2] &= ~EAST

    # def get_neighbors(self, y: int, x: int) -> List[Tuple[int, int]]:
    #     """Get all valid neighbors within bounds."""
    #     neighbors = []
    #     if y > 0:
    #         neighbors.append((y - 1, x))  # North
    #     if x < self.width - 1:
    #         neighbors.append((y, x + 1))  # East
    #     if y < self.height - 1:
    #         neighbors.append((y + 1, x))  # South
    #     if x > 0:
    #         neighbors.append((y, x - 1))  # West
    #     return neighbors

    # def get_unvisited_neighbors(self, y: int, x: int) -> List[Tuple[int, int]]:
    #     """Get unvisited neighbors."""
    #     return [(ny, nx) for ny, nx in self.get_neighbors(y, x)
    #             if not self.visited[ny][nx]]

    # def mark_visited(self, y: int, x: int) -> None:
    #     """Mark cell as visited."""
    #     self.visited[y][x] = True

    # def is_visited(self, y: int, x: int) -> bool:
    #     """Check if cell was visited."""
    #     return self.visited[y][x]

    # def all_visited(self) -> bool:
    #     """Check if all cells have been visited."""
    #     return all(all(row) for row in self.visited)

    # def to_hex_string(self) -> str:
    #     """Convert maze to hex format (for output file)."""
    #     lines = []
    #     for row in self.grid:
    #         line = ''.join(format(cell, 'X') for cell in row)
    #         lines.append(line)
    #     return '\n'.join(lines)


my_two_d_arr = [[0, 0], [1, 1]]