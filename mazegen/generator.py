import random
from typing import Optional, Tuple, List, Set
from .maze import Maze


class MazeGenerator:
    """
    Generates mazes using Hunt and Kill or Recursive Backtracker algorithm.
    """

    def __init__(self, width: int, height: int,
                 seed: Optional[int] = None) -> None:
        """
        Initialize generator.
        Args:
            width: Maze width in cells
            height: Maze height in cells
            seed: Random seed for reproducibility (optional)
        """
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.maze: Optional[Maze] = None
        self._pattern_42_cells: Set[Tuple[int, int]] = set()

    def generate(self, algorithm: str = "hunt_and_kill") -> Maze:
        """
        Generate the maze using specified algorithm.
        Args:
            algorithm: "hunt_and_kill" or "recursive_backtracker"
        Returns:
            Generated Maze object
        """
        # Set random seed if given
        if self.seed is not None:
            random.seed(self.seed)

        # Create a new Maze object
        self.maze = Maze(self.height, self.width)

        # PLACE "42" PATTERN BEFORE GENERATION
        placed_pattern = self.place_42_pattern()

        if not placed_pattern:
            print("Cannot place '42' pattern: Maze too small")

        # Generate using selected algorithm
        if algorithm.lower() == "recursive_backtracker":
            self._generate_recursive_backtracker()
        else:
            self._generate_hunt_and_kill()

        return self.maze

    def _get_valid_start(self) -> Tuple[int, int]:
        """Get a starting cell that's not on the 42 pattern.
        Return:
            Coodrinate (y, x) of the valid start
        """
        curr_y = random.randint(0, self.height - 1)
        curr_x = random.randint(0, self.width - 1)

        while (curr_y, curr_x) in self._pattern_42_cells:
            curr_y = random.randint(0, self.height - 1)
            curr_x = random.randint(0, self.width - 1)

        return (curr_y, curr_x)

    def _generate_hunt_and_kill(self) -> None:
        """Generate maze using Hunt and Kill algorithm."""
        assert self.maze is not None

        # Pick a starting cell (not on "42" pattern)
        curr_y, curr_x = self._get_valid_start()

        # Mark the starting cell as visited
        self.maze.mark_visited(curr_y, curr_x)

        while not self.maze.all_visited():
            # The kill phase
            unv_cell_neighbors = self.maze.get_unvisited_neighbors(
                curr_y, curr_x)

            # Filter out "42" cells from neighbors
            valid_neighbors = [
                (ny, nx) for (ny, nx) in unv_cell_neighbors
                if (ny, nx) not in self._pattern_42_cells
            ]

            # If there's valid unvisited neighbors:
            if valid_neighbors:
                next_cell = random.choice(valid_neighbors)
                next_y, next_x = next_cell
                # remove wall between current and next coordinates
                self.maze.remove_wall_between(curr_y, curr_x, next_y, next_x)
                # mark next as visited
                self.maze.mark_visited(next_y, next_x)
                # update the current
                curr_y, curr_x = next_y, next_x
            else:
                # Hunt phase
                hunt_result = self._hunt()
                if hunt_result:
                    curr_y, curr_x = hunt_result
                else:
                    break

    def _generate_recursive_backtracker(self) -> None:
        """Generate maze using Recursive Backtracker (DFS-based) algorithm."""
        assert self.maze is not None

        # Pick starting cell (not on 42 pattern)
        start_y, start_x = self._get_valid_start()

        stack: List[Tuple[int, int]] = [(start_y, start_x)]
        self.maze.mark_visited(start_y, start_x)

        while stack:
            y, x = stack[-1]

            # Get unvisited neighbors (not 42 cells)
            neighbors = [
                (ny, nx) for ny, nx in self.maze.get_neighbors(y, x)
                if not self.maze.is_visited(ny, nx)
                and (ny, nx) not in self._pattern_42_cells
            ]

            if neighbors:
                # Pick random neighbor, carve passage
                ny, nx = random.choice(neighbors)
                self.maze.remove_wall_between(y, x, ny, nx)
                self.maze.mark_visited(ny, nx)
                stack.append((ny, nx))
            else:
                # Dead end - backtrack
                stack.pop()

    def place_42_pattern(self) -> bool:
        """
        Place '42' pattern before generation (as immutable obstacle).
        Return:
            True if '42' pattern is placed successfully, else False
        """
        # Maze must be initialized
        assert self.maze is not None

        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        # Require adequate margins around pattern for connectivity
        # At least 2 cells on each side to ensure paths can connect
        min_margin = 2
        min_width = pattern_width + (min_margin * 2)
        min_height = pattern_height + (min_margin * 2)

        if self.width < min_width or self.height < min_height:
            print(f"Maze too small for '42' pattern (need "
                  f"{min_width}x{min_height}, "
                  f"got {self.width}x{self.height}) - pattern omitted")
            return False

        # Calculate center position
        center_y = (self.height - pattern_height) // 2
        center_x = (self.width - pattern_width) // 2

        # Place pattern
        for y in range(pattern_height):
            for x in range(pattern_width):
                if pattern[y][x] == 1:
                    maze_y = center_y + y
                    maze_x = center_x + x

                    # Set cell to 0xF (all walls closed)
                    self.maze.grid[maze_y][maze_x] = 0xF

                    # Mark as visited so Hunt & Kill skips it
                    self.maze.mark_visited(maze_y, maze_x)
                    self._pattern_42_cells.add((maze_y, maze_x))

        # print(f"Pre-placed '42' pattern at ({center_y}, {center_x})")
        return True

    def _hunt(self) -> Optional[Tuple[int, int]]:
        """
        Hunt phase: Find next unvisited cell adjacent to visited cell.
        Returns:
            (y, x) coordinates of found cell, or None if all visited
        """
        maze = self.maze
        assert maze is not None
        for y in range(maze.height):
            for x in range(maze.width):
                # Skip "42" cells (all walls = 0xF)
                if (y, x) in self._pattern_42_cells:
                    continue

                # Skip visited cells
                if maze.is_visited(y, x):
                    continue

                # Get visited neighbors (excluding "42" cells)
                visited_n: List[Tuple[int, int]] = []
                neighbors = maze.get_neighbors(y, x)

                for ny, nx in neighbors:
                    # Only take neighbors that are visited AND not "42" cells
                    if (maze.is_visited(ny, nx) and
                            (ny, nx) not in self._pattern_42_cells):
                        visited_n.append((ny, nx))

                # Connect to random visited neighbor
                if visited_n:
                    choosen_visited_n = random.choice(visited_n)
                    new_y, new_x = choosen_visited_n
                    maze.remove_wall_between(y, x, new_y, new_x)
                    maze.mark_visited(y, x)
                    return (y, x)

        return None

    def get_pattern_42_cells(self) -> Set[Tuple[int, int]]:
        """Retrun the set of cells occupied by the 42 pattern."""
        return self._pattern_42_cells.copy()
