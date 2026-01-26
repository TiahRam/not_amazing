# **A-MAZE-ING: Complete Implementation Plan**

## **PHASE 1: PROJECT SETUP & ENVIRONMENT**

### **Step 1.1: Repository & Environment Setup**
- Create Git repository
- Set up Python 3.10+ virtual environment (venv or conda recommended)
- Create `.gitignore` file (exclude `__pycache__`, `.mypy_cache`, `*.pyc`, virtual env, etc.)
- Initialize basic project structure:
  ```
  a-maze-ing/
  ├── a_maze_ing.py          # Main entry point
  ├── config.txt             # Default config file
  ├── Makefile
  ├── README.md
  ├── mazegen-*/             # Reusable package directory
  ├── requirements.txt
  └── .gitignore
  ```

### **Step 1.2: Dependencies Planning**
- Identify needed libraries (e.g., for MLX graphics if chosen, or terminal rendering)
- Consider maze generation algorithm libraries (research only - you'll implement yourself)
- Plan testing framework (pytest or unittest)

---

## **PHASE 2: CONFIGURATION FILE PARSER**

### **Step 2.1: Config Parser Design**
- Design a class/module to parse `config.txt`
- Handle `KEY=VALUE` format
- Ignore lines starting with `#` (comments)
- Strip whitespace appropriately

### **Step 2.2: Config Validation**
**2.2.1: Syntax Validation**
- Check file exists and is readable
- Validate each line format (KEY=VALUE or comment)
- Handle empty lines
- Report line numbers for syntax errors

**2.2.2: Mandatory Keys Validation**
- Verify presence of: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`
- Report missing mandatory keys with clear error messages

**2.2.3: Value Validation**
- **WIDTH/HEIGHT**: Must be positive integers
- **ENTRY/EXIT**: Must be valid coordinates (x,y format), within bounds, different from each other
- **OUTPUT_FILE**: Valid filename/path
- **PERFECT**: Boolean (True/False or similar)
- **Optional keys**: seed (integer), algorithm (string), display_mode (string)

**2.2.4: Logical Validation**
- Entry and exit must be at maze boundaries (external borders)
- Coordinates must be within WIDTH × HEIGHT bounds
- If maze too small for "42" pattern, print error (if size doesn't allow it)

### **Step 2.3: Config Storage**
- Store validated configuration in a data structure (dict, dataclass, or config object)
- Make it easily accessible throughout the program

---

## **PHASE 3: MAZE GENERATION ALGORITHM RESEARCH & DESIGN**

### **Step 3.1: Algorithm Selection**
Research and choose ONE algorithm to start with:
- **Recursive Backtracker** (DFS-based, creates long winding corridors)
- **Prim's Algorithm** (random spanning tree, creates shorter dead-ends)
- **Kruskal's Algorithm** (creates more branching)
- **Eller's Algorithm** (memory efficient, row-by-row)
- **Binary Tree** (simple but biased)

**Decision Criteria:**
- Can it create perfect mazes (single solution)?
- Can it be seeded for reproducibility?
- Does it naturally avoid large open areas?
- Complexity vs. implementation difficulty

### **Step 3.2: Data Structure Design**
Design how to represent the maze internally:
- **Option A**: 2D grid of Cell objects, each with wall states (N, E, S, W)
- **Option B**: 2D array where each cell is a number (bit flags for walls)
- **Option C**: Graph representation (nodes and edges)

Consider:
- Easy wall manipulation
- Neighbor consistency (if cell A has wall on East, cell B on West must match)
- Efficient pathfinding later
- Easy conversion to hexadecimal output

---

## **PHASE 4: CORE MAZE GENERATOR CLASS (Reusable Module)**

### **Step 4.1: MazeGenerator Class Structure**
Create a standalone, importable class with:
- **Constructor**: Accept parameters (width, height, seed, algorithm, etc.)
- **Generate method**: Creates the maze structure
- **Public properties**: Access to maze grid, dimensions, entry, exit
- **Get solution method**: Returns shortest path from entry to exit

### **Step 4.2: Maze Generation Implementation**

**4.2.1: Initialize Grid**
- Create empty grid (all walls closed initially, or all walls open - depends on algorithm)
- Set random seed for reproducibility

**4.2.2: Apply Algorithm**
- Implement chosen algorithm step-by-step
- Ensure walls are consistent between neighboring cells
- Track visited cells to ensure full connectivity

**4.2.3: Entry/Exit Placement**
- Open walls at entry and exit coordinates
- Ensure they're at external borders
- Verify they're accessible (connected to the maze)

**4.2.4: "42" Pattern Implementation**
- Identify suitable locations (not on solution path if perfect maze)
- Create fully closed cells forming visible "42" when rendered
- Check maze size allows it, otherwise print error to console

**4.2.5: Validation Checks**
- **Connectivity**: Run flood-fill or DFS to ensure all cells (except "42" pattern) are reachable
- **No large open areas**: Check for corridors wider than 2 cells
- **Border walls**: Ensure external borders have walls (except entry/exit)
- **Neighbor coherence**: Validate all neighboring walls match

### **Step 4.3: Pathfinding Implementation**
- Implement BFS or A* to find shortest path from entry to exit
- If PERFECT=True, verify exactly ONE path exists (no alternative routes)
- Store path as sequence of directions (N, E, S, W)

---

## **PHASE 5: OUTPUT FILE GENERATION**

### **Step 5.1: Hexadecimal Encoding**
- For each cell, convert wall state to hex:
  - Bit 0 (LSB): North wall (1 = closed, 0 = open)
  - Bit 1: East wall
  - Bit 2: South wall
  - Bit 3: West wall
- Example: walls on East and West = binary 1010 = hex A

### **Step 5.2: File Writing**
**5.2.1: Maze Data**
- Write cells row by row, one row per line
- Each cell = 1 hex digit
- No spaces between cells

**5.2.2: Metadata**
- Empty line after maze data
- Line 1: Entry coordinates (format: `x,y`)
- Line 2: Exit coordinates (format: `x,y`)
- Line 3: Shortest path as direction string (e.g., `NNEESWWSE`)

**5.2.3: Newlines**
- Ensure all lines end with `\n`

### **Step 5.3: Error Handling**
- Handle file write errors (permissions, disk space, invalid path)
- Provide clear error messages
- Use context managers (`with open(...)`) for automatic cleanup

---

## **PHASE 6: VISUAL REPRESENTATION**

### **Step 6.1: Choose Display Method**
- **Option A**: Terminal ASCII rendering (simpler, no external dependencies)
- **Option B**: MiniLibX (MLX) graphics (more visual, requires MLX library)

### **Step 6.2: ASCII Terminal Rendering** (if chosen)

**6.2.1: Design Character Mapping**
- Walls: `█` or `#` or `│─┌┐└┘├┤┬┴┼` (box-drawing characters)
- Open space: ` ` (space)
- Entry: `E` or colored marker
- Exit: `X` or colored marker
- Solution path: `.` or `*` or highlighted color
- "42" pattern: Distinct color or character

**6.2.2: Render Implementation**
- Convert internal maze structure to displayable characters
- Apply colors using ANSI escape codes
- Handle terminal size constraints
- Display menu/options for user interactions

### **Step 6.3: MLX Graphics** (if chosen)

**6.3.1: MLX Setup**
- Initialize MLX window
- Set up window size based on maze dimensions
- Calculate cell pixel size

**6.3.2: Drawing Functions**
- Draw walls as colored lines/rectangles
- Draw entry/exit with distinct colors
- Draw solution path overlay
- Render "42" pattern with specific color

### **Step 6.4: User Interactions**

**6.4.1: Mandatory Interactions**
- **Regenerate maze**: Parse config again, generate new maze, redisplay
- **Show/Hide path**: Toggle solution path visibility
- **Change wall colors**: Cycle through color options

**6.4.2: Optional Interactions**
- Set specific colors for "42" pattern
- Zoom in/out
- Step-by-step generation animation
- Export current view as image

**6.4.3: Input Handling**
- Keyboard controls (document keys in visual display)
- Handle events gracefully
- Provide help/menu screen

---

## **PHASE 7: MAIN PROGRAM (a_maze_ing.py)**

### **Step 7.1: Command-Line Interface**
- Accept exactly 1 argument: config file path
- Validate argument count
- Provide usage message if incorrect

### **Step 7.2: Error Handling Strategy**
- **Try-except blocks** around:
  - File operations
  - Config parsing
  - Maze generation
  - File writing
  - Visual display
- **Never crash unexpectedly**
- **Always provide clear error messages** to user

### **Step 7.3: Program Flow**
1. Parse command-line arguments
2. Load and validate configuration file
3. Instantiate MazeGenerator with config parameters
4. Generate maze
5. Validate maze meets all requirements
6. Write output file (hexadecimal format)
7. Launch visual representation
8. Handle user interactions in visual mode

---

## **PHASE 8: MAKEFILE CREATION**

### **Step 8.1: Required Targets**

**8.1.1: `install`**
- Install dependencies using `pip install -r requirements.txt`
- Consider using `uv`, `pipx`, or other package managers
- Support virtual environment activation message

**8.1.2: `run`**
- Execute main script: `python3 a_maze_ing.py config.txt`
- Use default config file

**8.1.3: `debug`**
- Run with Python debugger (pdb)
- Example: `python3 -m pdb a_maze_ing.py config.txt`

**8.1.4: `clean`**
- Remove temporary files: `__pycache__`, `.mypy_cache`, `*.pyc`
- Remove generated maze output files (optional, or specific ones)

**8.1.5: `lint`**
- Run flake8 with specified flags:
  ```
  flake8 . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
  ```
- Run mypy

**8.1.6: `lint-strict` (optional)**
- Run with `--strict` flag:
  ```
  flake8 . --strict
  mypy . --strict
  ```

### **Step 8.2: Makefile Best Practices**
- Use `.PHONY` for non-file targets
- Add helpful comments
- Consider `help` target listing all available commands

---

## **PHASE 9: REUSABLE PACKAGE CREATION**

### **Step 9.1: Package Structure**
Create a distributable package:
```
mazegen-1.0.0/
├── mazegen/
│   ├── __init__.py
│   ├── generator.py      # MazeGenerator class
│   ├── algorithms.py     # Algorithm implementations
│   └── utils.py          # Helper functions
├── setup.py or pyproject.toml
├── README.md (package-specific)
└── LICENSE (optional)
```

### **Step 9.2: Setup Configuration**
**Using `setup.py`:**
- Define package name: `mazegen-*` (replace * with your identifier)
- Version: `1.0.0`
- Author information
- Dependencies
- Python version requirement (>=3.10)

**Or using `pyproject.toml`** (modern approach):
- Same information in TOML format
- Use build system (e.g., setuptools, hatchling)

### **Step 9.3: Build Package**
- Create wheel file: `python -m build` or `python setup.py bdist_wheel`
- Creates `mazegen-1.0.0-py3-none-any.whl` in `dist/` directory
- Alternatively, create `.tar.gz` source distribution

### **Step 9.4: Package Documentation**
In the package README.md, document:
- **Installation**: `pip install mazegen-1.0.0-py3-none-any.whl`
- **Basic usage example**:
  ```python
  from mazegen import MazeGenerator
  
  gen = MazeGenerator(width=20, height=15, seed=42)
  gen.generate()
  maze = gen.get_maze()
  solution = gen.get_solution()
  ```
- **Custom parameters**: How to pass seed, algorithm choice, etc.
- **Accessing structure**: How to iterate over cells, get wall states
- **Accessing solution**: Format of returned path

### **Step 9.5: Integration**
- Ensure main program (`a_maze_ing.py`) imports and uses this package
- Keep package file separate and standalone (can be used without main program)

---

## **PHASE 10: CODE QUALITY & STANDARDS**

### **Step 10.1: Type Hints**
- Add type hints to ALL function parameters and return types
- Use `typing` module for complex types (List, Dict, Optional, etc.)
- Run `mypy` and fix all errors

### **Step 10.2: Docstrings**
Follow PEP 257 (Google or NumPy style):
- **Module-level**: Brief description of module purpose
- **Class-level**: Purpose, attributes, usage example
- **Function/Method-level**: 
  - Description
  - Args: parameter names, types, descriptions
  - Returns: type and description
  - Raises: exceptions that might be raised

Example:
```python
def generate_maze(width: int, height: int, seed: int) -> MazeGrid:
    """
    Generates a random maze using Recursive Backtracker algorithm.
    
    Args:
        width: Number of cells horizontally (must be > 0)
        height: Number of cells vertically (must be > 0)
        seed: Random seed for reproducibility
    
    Returns:
        MazeGrid object containing the generated maze structure
    
    Raises:
        ValueError: If width or height is not positive
    """
```

### **Step 10.3: Flake8 Compliance**
- Run `make lint` frequently
- Fix all warnings:
  - Unused variables
  - Unused imports
  - Missing imports
  - Untyped definitions
  - Return type issues
- Aim for zero warnings

### **Step 10.4: Exception Handling**
- Use try-except blocks for:
  - File I/O
  - Parsing operations
  - External library calls (MLX, etc.)
- Prefer context managers (`with` statements) for resources
- Provide specific error messages (not just generic exceptions)

### **Step 10.5: Resource Management**
- Use context managers for file operations
- Close any network connections (if applicable)
- Clean up MLX resources on exit
- Ensure no memory leaks in long-running visual mode

---

## **PHASE 11: TESTING (Optional but Recommended)**

### **Step 11.1: Unit Tests**
Create test files for:
- **Config parser**: Valid/invalid configs, missing keys, wrong value types
- **Maze generator**: Correct dimensions, connectivity, entry/exit placement
- **Hexadecimal encoder**: Correct bit encoding
- **Pathfinding**: Finds correct shortest path

### **Step 11.2: Integration Tests**
- Full program run with various config files
- Output file format validation
- Edge cases: minimum size maze, maximum size, perfect vs. non-perfect

### **Step 11.3: Test Framework**
- Use `pytest` or `unittest`
- Create `tests/` directory
- Run tests with `make test` target (add to Makefile)

**Note**: Tests are not graded, but very useful for debugging!

---

## **📋 PHASE 12: README.md DOCUMENTATION**

### **Step 12.1: Required Sections**

**12.1.1: Attribution Line (First Line)**
```markdown
_This project has been created as part of the 42 curriculum by [Your Name(s)]._
```
(Must be italicized)

**12.1.2: Description**
- Project goal: Maze generator in Python
- Brief overview of features
- What makes it interesting/unique

**12.1.3: Instructions**
- **Installation**:
  - Clone repository
  - Set up virtual environment
  - Run `make install`
- **Usage**:
  - Basic command: `python3 a_maze_ing.py config.txt`
  - Or `make run`
- **Configuration**:
  - Explain all config keys (mandatory and optional)
  - Provide example config file
  - Format rules (KEY=VALUE, comments with #)
- **Visual Mode Controls**:
  - List all keyboard shortcuts
  - Explain each interaction feature

**12.1.4: Resources**
- **Documentation**: Links to Python docs, algorithm explanations
- **Articles/Tutorials**: Any maze generation resources you used
- **AI Usage Disclosure**:
  - Which tasks used AI (e.g., "Used ChatGPT for algorithm research")
  - Which parts of the project
  - Be specific and honest

**12.1.5: Algorithm Choice**
- Name of algorithm used (e.g., "Recursive Backtracker")
- Why you chose it:
  - Creates perfect mazes naturally
  - Seeded random for reproducibility
  - Avoids large open areas
  - Relatively simple to implement
- Brief explanation of how it works
- References to algorithm sources

**12.1.6: Code Reusability**
- Explain the `mazegen-*` package
- How to install: `pip install mazegen-*.whl`
- Usage examples
- What structure is exposed (maze grid format)
- How to access solution path

**12.1.7: Project Management**
- **Team Roles** (if team project):
  - Who worked on what components
  - Division of labor
- **Planning**:
  - Initial approach
  - How it evolved during development
  - Timeline
- **What Worked Well**:
  - Successful strategies
  - Good decisions made
- **What Could Be Improved**:
  - Challenges faced
  - What you'd do differently
- **Tools Used**:
  - Git for version control
  - VS Code / PyCharm / etc.
  - Debugging tools
  - Testing frameworks

### **Step 12.2: Optional Sections**
- **Features**: List of implemented features
- **Advanced Features**: If you implemented bonuses (multiple algorithms, animations)
- **Examples**: Screenshots or example output
- **Troubleshooting**: Common issues and solutions
- **Contributing**: How others can contribute (if open source)
- **License**: MIT, GPL, etc.

---

## **📋 PHASE 13: ADVANCED FEATURES / BONUSES (Optional)**

### **Step 13.1: Multiple Algorithms**
- Implement 2-3 different maze generation algorithms
- Add `algorithm` key to config file
- Modify MazeGenerator to accept algorithm choice
- Update README with algorithm comparisons

### **Step 13.2: Generation Animation**
- If using MLX, show maze being generated step-by-step
- Highlight current cell being processed
- Add speed control (fast/slow/pause)
- Terminal version: Use ANSI cursor movements for live updates

---

## **📋 PHASE 14: FINAL VALIDATION & SUBMISSION**

### **Step 14.1: Complete Checklist**
- [ ] Python 3.10+ used
- [ ] Flake8 compliant (run `make lint` with no errors)
- [ ] Mypy passes with no errors
- [ ] All functions have type hints
- [ ] All functions/classes have docstrings
- [ ] Makefile with all required targets works
- [ ] `config.txt` default file in repository
- [ ] Program handles all errors gracefully (never crashes)
- [ ] Output file format matches specification exactly
- [ ] Maze meets all validation rules
- [ ] "42" pattern visible (or error printed if too small)
- [ ] If PERFECT=True, exactly one solution path exists
- [ ] Visual representation shows walls, entry, exit, solution
- [ ] All user interactions work
- [ ] Reusable package `mazegen-*.whl` or `.tar.gz` created
- [ ] Package is importable and functional
- [ ] README.md complete with all required sections
- [ ] .gitignore excludes artifacts
- [ ] Repository clean (no `__pycache__`, temporary files)

### **Step 14.2: Peer Review**
- Have someone else run your program
- Test with various config files
- Ensure error messages are clear
- Check README is understandable

### **Step 14.3: Edge Case Testing**
Test with:
- Minimum maze size (e.g., 3×3)
- Very large maze (e.g., 100×100)
- Entry and exit at different boundaries
- Perfect vs. non-perfect mazes
- Invalid configs (missing keys, wrong types, etc.)
- File write errors (read-only directory, invalid path)

---

## **🎯 RECOMMENDED IMPLEMENTATION ORDER**

For optimal learning and debugging:

1. **Start small**: Config parser + validation
2. **Core logic**: MazeGenerator class with simple algorithm
3. **Output**: Hexadecimal file writing
4. **Visual**: Basic ASCII rendering (no interactions yet)
5. **Path**: Implement pathfinding
6. **Perfect maze**: Add validation for single path
7. **"42" pattern**: Add fully closed cells
8. **Interactions**: Add user controls
9. **Package**: Create reusable module
10. **Polish**: Makefile, README, error handling
11. **Advanced**: Bonuses if time permits

---

## **💡 TIPS FOR SUCCESS**

1. **Incremental Development**: Build one feature at a time, test thoroughly before moving on
2. **Git Commits**: Commit frequently with clear messages
3. **Debug Early**: Don't wait until the end to test
4. **Read Requirements**: Re-read the PDF frequently to ensure nothing is missed
5. **Ask Questions**: Clarify ambiguities early
6. **Time Management**: Budget time for each phase, leave buffer for debugging
7. **Documentation First**: Write docstrings as you code, not at the end
8. **Type Hints**: Add them as you write functions, easier than retrofitting

---

**Good luck with your learning journey! 🚀**
