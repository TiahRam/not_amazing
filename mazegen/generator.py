import random
from typing import Optional, Tuple
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
        self.width = width
        self.height = height 
        self.seed = seed
        self.maze = Optional[Maze] = None

    def generate(self) -> Maze:
        """
        Generate the actual maze.
        
        Returns:
            Generated Maze object
        """
        # set random seed if given
        given_seed = None
        if self.seed:
            given_seed = random.seed(self.seed)
        
        # Create a new Maze object and pick a starting cell
        maze = Maze(self.height, self.width)
        start_cell = maze[0][0]

        # mark the starting cell as visited
        maze.mark_visited(0, 0)

        while not maze.all_visited():
            # the kill phase
            ...


    
    def _hunt(self) -> Optional[Tuple[int, int]]:
        """
        Hunt phase: Find next unvisited cell adjacent to visited cell.
        
        Returns:
            (y, x) coordinates of found cell, or None if all visited
        """
        # TODO: Implement hunt logic
        pass
