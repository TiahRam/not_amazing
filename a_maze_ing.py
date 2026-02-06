#!/usr/bin/env python3
import sys
from mazegen.generator import MazeGenerator
from mazegen.pathfinding import bfs, dfs
from helpers.parser import first_args_validation, semantic_validation
from helpers.output_writing import write_output
from helpers.imperfect_maze import add_random_loops
from helpers.validation import validate_perfect_maze
from helpers.visualizer import run_visualizer


def main() -> None:
    """Main Program orchestrator"""
    # 1. Parse config
    configs = first_args_validation()
    typed_configs = semantic_validation(configs)

    entry = typed_configs["ENTRY"]
    exit_ = typed_configs["EXIT"]
    output_file = typed_configs["OUTPUT_FILE"]
    perfect = typed_configs["PERFECT"]
    algo = typed_configs.get("ALGORITHM", "BFS")
    gen_algo = typed_configs.get("GEN_ALGORITHM", "hunt_and_kill")

    # 2. Generate maze
    generator = MazeGenerator(
        width=typed_configs["WIDTH"],
        height=typed_configs["HEIGHT"],
        seed=typed_configs.get("SEED")
    )
    maze = generator.generate(algorithm=gen_algo)
    print(f"Maze generated using '{gen_algo}'! "
          f"All cells visited: {maze.all_visited()}")

    # 3. Check for perfect config if true or flase
    if not perfect:
        pattern_cells = generator.get_pattern_42_cells()
        loop_number = (maze.width * maze.height) // 10
        add_random_loops(maze, loop_number, pattern_cells)
        print(f"Imperfect maze created 'PERFECT={perfect}'")
    else:
        print(f"Perfect maze created 'PERFECT={perfect}'")

    # 4. Validate perfect maze BEFORE adding entry/exit
    if perfect:
        pattern_cells = generator.get_pattern_42_cells()
        if not validate_perfect_maze(maze, pattern_cells):
            print(f"ERROR: 'PERFECT={perfect}' but the maze is not perfect")
            sys.exit(1)

    # 5. Find the shortest path
    path = ""
    if algo.upper() == "DFS":
        path = dfs(maze, entry, exit_)
        print("Using DFS algorithm")
    else:
        path = bfs(maze, entry, exit_)
        print("Using BFS algorithm (default)")

    print(f"Path found! Length: {len(path)} steps")
    if len(path) > 0:
        print(f"Path: {path[:50]}{'...' if len(path) > 50 else ''}")

    # 6. Write output (without path for now)
    write_output(maze, entry, exit_, output_file, path)

    print("Maze generated successfully!")
    print(f"Written to: {typed_configs['OUTPUT_FILE']}")
    try:
        run_visualizer(perfect, generator, maze, entry, exit_,
                       algo, path, gen_algo)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
