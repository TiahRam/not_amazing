#!/usr/bin/env python3
import sys
from visualizer import run_visualizer
from validation import validate_perfect_maze
from mazegen.generator import MazeGenerator
from helpers.parser import first_args_validation, semantic_validation
from helpers.entry_and_exit import add_entry_exit
from helpers.output_writing import write_output
from helpers.imperfect_maze import add_random_loops
from pathfinding import find_shortest_path


def main():
    # 1. Parse config
    configs = first_args_validation()
    typed_configs = semantic_validation(configs)

    entry = typed_configs["ENTRY"]
    exit_ = typed_configs["EXIT"]
    output_file = typed_configs["OUTPUT_FILE"]
    perfect = typed_configs["PERFECT"]

    # 2. Generate maze
    generator = MazeGenerator(
        width=typed_configs["WIDTH"],
        height=typed_configs["HEIGHT"],
        seed=typed_configs.get("SEED")
    )
    maze = generator.generate()

    # 3. Check for perfect config if true or flase
    if not perfect:
        loop_number = (maze.width * maze.height) // 10
        add_random_loops(maze, loop_number)
        print(f"Imperfect maze created 'PERFECT={perfect}'")
    else:
        print(f"Perfect maze created 'PERFECT={perfect}'")

    # 5. Find the shortest path
    path = find_shortest_path(maze, entry, exit_)
    print(f"Path found! Length: {len(path)} steps")
    print(f"Path: {path[:50]}{'...' if len(path) > 50 else ''}")

    # 6. Write output (without path for now)
    write_output(maze, entry, exit_, output_file, path)

    print("Maze generated successfully!")
    print(f"Written to: {typed_configs['OUTPUT_FILE']}")

    add_entry_exit(maze, entry, exit_)

    run_visualizer(maze, entry, exit_, path)


if __name__ == "__main__":
    main()