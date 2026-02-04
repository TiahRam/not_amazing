*This project has been created as part of the 42 curriculum by mramidam and mnassir.*

# A-Maze-Ing

A maze generator and solver using the Hunt and Kill algorithm with BFS/DFS pathfinding.

## Description

A-Maze-Ing is a command-line maze generator that creates perfect or imperfect mazes with a "42" pattern embedded in the center. The project includes:
- **Maze generation** using the Hunt and Kill algorithm
- **Pathfinding** with BFS (shortest path) and DFS algorithms
- **Configurable parameters** via a config file
- **Reusable Python package** (`mazegen`) for integration in other projects

## Instructions

### Running the CLI

```bash
./a_maze_ing.py config.txt
```

### Installing the Package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or build from source:
```bash
pip install build
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

## Config File Format

```text
# required
WIDTH=30              # Maze width in cells (required)
HEIGHT=30             # Maze height in cells (required)
ENTRY=0,0             # Entry point x,y (required, must be on border)
EXIT=0,29             # Exit point x,y (required, must be on border)
OUTPUT_FILE=maze.txt  # Output file path (required)
PERFECT=yes           # yes/no - Perfect maze or add loops (required)

# optional
SEED=42               # Random seed for reproducibility (optional)
ALGORITHM=BFS         # BFS or DFS for pathfinding (optional, default: BFS)
```

## Algorithm Choice: Hunt and Kill

We chose the **Hunt and Kill algorithm** for the following reasons:

1. **Easy to implement** - The algorithm is straightforward with two simple phases (kill and hunt)
2. **Always produces perfect mazes** - By design, it creates exactly one path between any two cells
3. **Easy to add imperfections** - Since we start with a perfect maze, adding loops for `PERFECT=no` is trivial (just remove random walls)
4. **Good visual results** - Produces mazes with long, winding passages

We also choose **BFS and DFS** for the following reasons:

1. **Easy to implement and easy to understand**
2. Another reason
3. More other reasons

## Reusable Code: mazegen Package

The `mazegen/` directory is a standalone Python package that can be imported independently:

```python
from mazegen import MazeGenerator, bfs, dfs

# Create and generate maze
gen = MazeGenerator(width=20, height=20, seed=42)
maze = gen.generate()

# Find path
path = bfs(maze, entry=(0, 0), exit_=(19, 19))
print(path)  # "EESSSWW..."
```

### Package Contents

| Module | Description |
|--------|-------------|
| `MazeGenerator` | Generates mazes using Hunt & Kill |
| `Maze` | Maze data structure with wall operations |
| `bfs()` | Shortest path using Breadth-First Search |
| `dfs()` | Any path using Depth-First Search |

## Resources

### References
- [Hunt and Kill Algorithm - Jamis Buck](https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm) - Algorithm explanation and visualization
- [Maze Algorithms - Jamis Buck](https://www.jamisbuck.org/mazes/) - Interactive maze algorithm demos

### AI Usage
AI assistance (Claude/Gemini) was used for:
- **Debugging** - Identifying issues with maze connectivity and validation
- **Code organization** - Structuring the package for pip distribution
- **Documentation** - Generating docstrings and README content

All algorithm implementation and core logic was written by the team.

## Team & Project Management

### Team Roles

| Member | Responsibilities |
|--------|------------------|
| mramidam | Maze generation, pathfinding (BFS/DFS), package structure |
| mnassiri | Visualization |
| Both | Initial parsing implementation |

### Planning Evolution
1. **Phase 1**: Config parsing (collaborative)
2. **Phase 2**: Split work - maze generation vs visualization
3. **Phase 3**: Integration and testing (collaborative)

### What Worked Well
- Clear separation of concerns between modules
- Using a config file for flexibility
- Creating a reusable package

### What Could Be Improved
- Earlier integration testing between components
- More comprehensive error messages

### Tools Used
- Python 3.10+
- Git for version control
- VSCode/vim as IDE
