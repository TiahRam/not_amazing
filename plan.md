# Resume of the all the project

---

- we have file: amazing.py, config.py
  amazing.py will be the main script
  config will have the configuration for the script (as a key: value -> dict)
  Now, amazing will take the configutation from the config files, run every
  implementation using the config we have (which basically generate a maze)
  After all of that, it will write the output of the generated maze to an output file

the output file is a hexadecimal wall representation of that generated maze

# Steps

---

- First of all we need to take all the args and parse them
  meaning: we initialize an empty dict, open the file:

```python
config_variables = {}
with open("config.txt", "r") as file:
	for line in file:
		key, value in line.strip().slpit("=")
		config_variables["key"] = "value"
```

Now that we have all the config variables, we can go to the next steps

✅ Phase 1 — Argument & Config Handling

1. Parse CLI arguments

Decide what input arguments your script should accept. Typical ones would be:

The config file path (positional)

Optional flags (if you decide to support them later), e.g.:

--output path for maze file

--visual to show visual rendering

--seed to control RNG for reproducibility

2. Read the config file

The config file will likely provide maze parameters such as:

Maze width

Maze height

Perfect maze flag (true/false)

Output file name

Visual mode preference

3. Validate config values

Check that:

Width & height are positive integers

Perfect flag is boolean or parsable

File paths are correct / writable

Any visualization options are valid

✅ Phase 2 — Maze Data Model

Before generating a maze, decide how to represent it internally.

4. Decide your internal data structure

For grid mazes, common structures:

2D array of cells, each with walls info

Graph-like adjacency

Or a binary matrix of walls and passages

The important point: each cell needs to store which walls exist.

5. Define the cell state & wall representation

Typical cell walls:

NORTH

SOUTH

EAST

WEST

You might represent them in multiple ways, e.g.:

Boolean flags

Bitmask integers (0–15)

Enum-style data

This directly affects your final export format.

✅ Phase 3 — Maze Generation Logic 6. Choose a generation algorithm

Perfect mazes (exactly one path between two points) use algorithms like:

Depth-first search (DFS) backtracking (classic)

Prim’s algorithm

Kruskal’s algorithm

Recursive division

Choose one that:

Supports perfect maze generation

Can be encapsulated cleanly

7. Implement the maze “carving”

Using the chosen algorithm:

Initialize all cells as “walled”

Remove walls according to traversal

Ensure no loops & no isolated sections if perfect mode is requested

If configs allow imperfect mazes, optionally add loops afterwards.

✅ Phase 4 — Hexadecimal Wall Encoding

You will eventually output a maze using a hex representation.

8. Define your hex encoding scheme

Each cell’s walls must map to a hex value. For example:

North = 1
East = 2
South = 4
West = 8

Then hex cell = sum of active walls, converted to hex.

Example:

North + West = 1 + 8 = 9 → hex 0x9

Your tasks here:

Choose bit ordering (document it)

Implement conversion from walls to hex

Organize final maze output format (rows, whitespace, etc.)

✅ Phase 5 — Output Formatting 9. Write the encoded maze to a file

Output file contains:

Grid of hex values

One row per maze row

Possibly metadata (width, height, etc.)

Define output format clearly (required for later interoperability).

✅ Phase 6 — Visualization 10. Provide a human-readable visual representation

Multiple options exist:

ASCII output (simple)

Matplotlib/grid drawing (medium complexity)

Tkinter/Pygame (interactive)

ASCII is easiest and portable, e.g.:

+---+---+
| |
+---+ +
| |
+---+---+

Key tasks:

Decide border drawing rules

Convert internal walls to visible characters

Optionally print to console or save to file

✅ Phase 7 — Code Organization & Reusability 11. Modularize your code

Suggested separation:

parser.py → CLI parsing + config loading
maze.py → Maze data structure + wall logic
generator.py → Maze generation algorithm(s)
encoder.py → Hex wall encoding
visualizer.py → ASCII or graphical output
main.py → Script orchestration

Not mandatory, but helps with:

Debugging

Reuse

Possible future enhancements

📦 Bonus Considerations (Optional but Good to Plan) 12. RNG seeding support

To allow reproducible mazes:

Accept --seed argument

Initialize random.seed(seed)

13. Error handling & messaging

Show helpful errors when:

Config file missing

Invalid values

Output directory not writable

14. Testing strategy

Plan some test cases:

Small mazes (2x2, 3x3)

Perfect vs imperfect

Seeded vs random

Visualization checks

📝 Final Summary Checklist

To succeed, you'll need to implement:

✔ Argument parsing
✔ Config file reading & validation
✔ Internal maze cell structure & walls
✔ Generation algorithm (for perfect maze)
✔ Hexadecimal encoding for output
✔ Visual display (ASCII or graphical)
✔ Clean code structure for reuse

==================================================================
Summary of Validation Categories

Here’s a clean mental model:

1. File-level errors
   File not found
   Cannot open file
   No read permission

2. Syntax errors (formatting)
   Wrong format (: instead of =)
   Missing key or missing value
   Extra symbols
   Empty lines with junk data

3. Semantic errors (meaning problems)
   Wrong types (width=abc)
   Values not convertible (perfect=maybe)

4. Logical errors (impossible conditions)
   width=0
   height < 2
   Required fields missing
   Contradictory values (perfect=false + force_perfection=true)

=================================================================
LEVEL 1 — File-Level Validation

Handles:
✔ File missing
✔ File unreadable
✔ No read permission
✔ Invalid command-line args

NO parsing of content yet

LEVEL 2 — Syntax Validation

Handles:
✔ Bad key=value lines
✔ Missing =
✔ Multiple = if not allowed
✔ Empty keys or empty values

LEVEL 3 — Semantic Validation

Handles:
✔ Wrong types (width="abc")
✔ Wrong values (perfect="maybe")
✔ Missing required keys
✔ Duplicates keys

LEVEL 4 — Logical Validation

Handles:
✔ Width <= 0
✔ Impossible maze sizes
✔ Contradictory options



<!-- Wilson 5s: Maze feel: Extremely natural, beautiful
prism maybe
dfs, might be boring asf


Recursive Backtracker (aka randomized DFS) -->
-----> Hunt and kill