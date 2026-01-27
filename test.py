#!/usr/bin/env python3
# test_maze.py
from mazegen.maze import Maze, NORTH, EAST, SOUTH, WEST

# Create small 3x3 maze
maze = Maze(3, 3)

print("Initial state (all walls closed):")
print(maze.to_hex_string())
# Should print:
# FFF
# FFF
# FFF

# Remove some walls manually
maze.remove_wall_between(0, 0, 0, 1)  # Remove wall between (0,0) and (0,1)
maze.remove_wall_between(0, 1, 1, 1)  # Remove wall between (0,1) and (1,1)

print("\nAfter removing walls:")
print(maze.to_hex_string())
# Should show opened walls

# Test neighbors
print("\nNeighbors of (1,1):")
print(maze.get_neighbors(1, 1))
# Should print: [(0, 1), (1, 2), (2, 1), (1, 0)]

# Test visited tracking
maze.mark_visited(0, 0)
print("\nIs (0,0) visited?", maze.is_visited(0, 0))  # True
print("Is (1,1) visited?", maze.is_visited(1, 1))    # False
print("All visited?", maze.all_visited())            # False
