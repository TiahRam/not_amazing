
import random
from typing import Optional, Tuple, List
from .maze import Maze


class MazeGenerator:
    """Generates mazes using Hunt and Kill algorithm."""
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

    def generate(self) -> Maze:
        """
        Generate the actual maze.
        Returns:
            Generated Maze object
        """
        # set random seed if given
        if self.seed is not None:
            random.seed(self.seed)

        # Create a new Maze object and pick a starting cell
        self.maze = Maze(self.height, self.width)
        curr_y = random.randint(0, self.height - 1)
        curr_x = random.randint(0, self.width - 1)

        # mark the starting cell as visited
        self.maze.mark_visited(curr_y, curr_x)

        while not self.maze.all_visited():
            # the kill phase
            # Get all unvisited neighbors of the current cell
            unv_cell_neighbors = self.maze.get_unvisited_neighbors(
                curr_y, curr_x)

            # if there's unvisited neighbors:
            if unv_cell_neighbors:
                next_cell = random.choice(unv_cell_neighbors)
                next_y, next_x = next_cell
                self.maze.remove_wall_between(curr_y, curr_x, next_y, next_x)
                self.maze.mark_visited(next_y, next_x)
                curr_y, curr_x = next_y, next_x
            # if stuck, meaning we all neighbors are visited
            else:
                hunt_result = self._hunt()
                if hunt_result:
                    curr_y, curr_x = hunt_result
                else:
                    break
        return self.maze

    def _hunt(self) -> Optional[Tuple[int, int]]:
        """
        Hunt phase: Find next unvisited cell adjacent to visited cell.
        Returns:
            (y, x) coordinates of found cell, or None if all visited
        """
        # loop through every single cell, row and col until we find unv one
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                # if we find an unvisited cell,
                # we check if it has visited neighbors
                if not self.maze.is_visited(y, x):
                    visited_n: List[Tuple[int, int]] = []

                    # we get all nighbors of that unvisited cell
                    # and add to the visited listed of that unv cell
                    neighbors = self.maze.get_neighbors(y, x)
                    for ny, nx in neighbors:
                        if self.maze.is_visited(ny, nx):
                            visited_n.append((ny, nx))
                    # Now, if it has visited neighbors, we choose one random
                    # Crave path between the two, mark as visited
                    # And return the coordinates of the unv cell
                    if visited_n:
                        choosen_visited_n = random.choice(visited_n)
                        new_y, new_x = choosen_visited_n
                        self.maze.remove_wall_between(y, x, new_y, new_x)
                        self.maze.mark_visited(y, x)
                        return (y, x)
        # if not we return None
        return None
