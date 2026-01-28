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
        """Maze Constructor

        Args:
            width: grid width
            height: grid height
        """
        self.height = height
        self.width = width

        # Fill all the grid with all closed wall
        self.grid: List[List[int]] = []
        for _ in range(height):
            row: List[int] = []
            for _ in range(width):
                row.append(0xF)
            self.grid.append(row)

        # All the cells are not visited by default
        self.visited: List[List[bool]] = []
        for _ in range(height):
            row: List[bool] = []
            for _ in range(width):
                row.append(False)
            self.visited.append(row)

    def remove_wall_between(self, y1: int, x1: int, y2: int, x2: int) -> None:
        """
        Remove wall between 2 cells:
        Removes the wall on cell 1 facing cell 2
        Removes the wall on cell 2 facing cell 1 (keep them in sync!)
        """
        # Check if they are neighbors
        y_distance = y2 - y1
        x_distance = x2 - x1

        if y_distance == 1:
            # cell2 on the SOUTH side of cell 1
            self.grid[y1][x1] &= ~SOUTH
            self.grid[y2][x2] &= ~NORTH
        elif y_distance == -1:
            # Cell 2 on the NORTH side of cell 1
            self.grid[y1][x1] &= ~NORTH
            self.grid[y2][x2] &= ~SOUTH
        elif x_distance == 1:
            # Cell 2 on the SOUTH side of cell 1
            self.grid[y1][x1] &= ~EAST
            self.grid[y2][x2] &= ~WEST
        elif x_distance == -1:
            # cell2 on the NORTH side of cell 1
            self.grid[y1][x1] &= ~WEST
            # self.grid[x2][y2] = 0b1101
            self.grid[y2][x2] &= ~EAST

    def get_neighbors(self, y: int, x: int) -> List[Tuple[int, int]]:
        """Get all valid neighbors within bounds."""
        valid_neighbors: List[Tuple[int, int]] = []

        if y > 0:
            # NORTH NEIGHBOR
            valid_neighbors.append((y - 1, x))
        if x < self.width - 1:
            # EAST NEIGHBOR
            valid_neighbors.append((y, x + 1))
        if y < self.height - 1:
            # SOUTH NEIGHBOR
            valid_neighbors.append((y + 1, x))
        if x > 0:
            # WEST NEIGHBOR
            valid_neighbors.append((y, x - 1))

        return valid_neighbors

    def get_unvisited_neighbors(self, y: int, x: int) -> List[Tuple[int, int]]:
        """Get neighbors that haven't been visited yet"""
        unvisited_neighbors: List[Tuple[int, int]] = []
        all_neighbors = self.get_neighbors(y, x)
        for neigh_y, neigh_x in all_neighbors:
            if not self.visited[neigh_y][neigh_x]:
                unvisited_neighbors.append((neigh_y, neigh_x))

        return unvisited_neighbors

    def mark_visited(self, y: int, x: int) -> None:
        """Mark cell as visited."""
        self.visited[y][x] = True

    def is_visited(self, y: int, x: int) -> bool:
        """
        Check if cell was visited.
        Returns: boolen
        """
        return self.visited[y][x]

    def all_visited(self) -> bool:
        """Check if all cells have been visited"""
        return all(all(row) for row in self.visited)

    def to_hex_string(self) -> str:
        """Convert maze to hex format for output file."""
        string_list: List[str] = []
        for row in self.grid:
            line = ''.join(format(cell, 'X') for cell in row)
            string_list.append(line)
        string_to_return = '\n'.join(string_list)

        return string_to_return

    def has_wall(self, y: int, x: int, direction: int) -> bool:
        """Check if cell has a wall in given direction."""
        return bool(self.grid[y][x] & direction)

    def get_cell_value(self, y: int, x: int) -> int:
        """Get cell's wall value."""
        return self.grid[y][x]

    def set_cell_value(self, y: int, x: int, value: int) -> None:
        """Set cell's wall value directly."""
        self.grid[y][x] = value
