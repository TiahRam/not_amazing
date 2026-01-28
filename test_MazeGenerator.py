#!/usr/bin/env python3
from mazegen.maze import Maze
from mazegen.generator import MazeGenerator


def test_basic_generation():
    """Test 1: Basic 5x5 maze generation"""
    print("=" * 50)
    print("TEST 1: Basic 5x5 Maze Generation")
    print("=" * 50)
    
    gen = MazeGenerator(width=5, height=5, seed=42)
    maze = gen.generate()
    
    print("\nGenerated Maze (hex):")
    print(maze.to_hex_string())
    
    print(f"\nAll cells visited? {maze.all_visited()}")
    print(f"Maze dimensions: {maze.width}x{maze.height}")
    
    # Check that it's not all Fs (walls were removed)
    hex_string = maze.to_hex_string()
    if hex_string.count('F') == maze.width * maze.height:
        print("❌ FAIL: All cells are still 0xF (no walls removed!)")
    else:
        print("✅ PASS: Walls were removed!")
    
    print()


def test_reproducibility():
    """Test 2: Same seed = same maze"""
    print("=" * 50)
    print("TEST 2: Reproducibility (Same Seed)")
    print("=" * 50)
    
    gen1 = MazeGenerator(width=5, height=5, seed=123)
    maze1 = gen1.generate()
    
    gen2 = MazeGenerator(width=5, height=5, seed=123)
    maze2 = gen2.generate()
    
    hex1 = maze1.to_hex_string()
    hex2 = maze2.to_hex_string()
    
    print("\nMaze 1:")
    print(hex1)
    print("\nMaze 2:")
    print(hex2)
    
    if hex1 == hex2:
        print("\n✅ PASS: Same seed produces identical mazes!")
    else:
        print("\n❌ FAIL: Mazes are different with same seed!")
    
    print()


def test_different_seeds():
    """Test 3: Different seeds = different mazes"""
    print("=" * 50)
    print("TEST 3: Different Seeds")
    print("=" * 50)
    
    gen1 = MazeGenerator(width=5, height=5, seed=100)
    maze1 = gen1.generate()
    
    gen2 = MazeGenerator(width=5, height=5, seed=200)
    maze2 = gen2.generate()
    
    hex1 = maze1.to_hex_string()
    hex2 = maze2.to_hex_string()
    
    print("\nMaze with seed=100:")
    print(hex1)
    print("\nMaze with seed=200:")
    print(hex2)
    
    if hex1 != hex2:
        print("\n✅ PASS: Different seeds produce different mazes!")
    else:
        print("\n⚠️  WARNING: Mazes are identical (might happen by chance)")
    
    print()


def test_larger_maze():
    """Test 4: Larger maze (10x10)"""
    print("=" * 50)
    print("TEST 4: Larger Maze (10x10)")
    print("=" * 50)
    
    gen = MazeGenerator(width=10, height=10, seed=42)
    maze = gen.generate()
    
    print("\nGenerated 10x10 Maze:")
    print(maze.to_hex_string())
    
    print(f"\nAll cells visited? {maze.all_visited()}")
    
    # Count how many cells still have all 4 walls
    fully_closed = 0
    for row in maze.grid:
        for cell in row:
            if cell == 0xF:
                fully_closed += 1
    
    print(f"Cells with all 4 walls closed: {fully_closed}")
    print(f"Total cells: {maze.width * maze.height}")
    
    if maze.all_visited():
        print("✅ PASS: All cells were visited!")
    else:
        print("❌ FAIL: Some cells were not visited!")
    
    print()


def test_tiny_maze():
    """Test 5: Smallest possible maze (2x2)"""
    print("=" * 50)
    print("TEST 5: Tiny Maze (2x2)")
    print("=" * 50)
    
    gen = MazeGenerator(width=2, height=2, seed=42)
    maze = gen.generate()
    
    print("\nGenerated 2x2 Maze:")
    print(maze.to_hex_string())
    
    print(f"\nAll cells visited? {maze.all_visited()}")
    
    # Decode each cell
    print("\nDecoded:")
    for y in range(2):
        for x in range(2):
            val = maze.get_cell_value(y, x)
            print(f"  Cell ({y},{x}): 0x{val:X} = 0b{val:04b}")
    
    print()


def test_perfect_maze():
    """Test 6: Is it a perfect maze? (No loops)"""
    print("=" * 50)
    print("TEST 6: Perfect Maze Check (No Loops)")
    print("=" * 50)
    
    gen = MazeGenerator(width=5, height=5, seed=42)
    maze = gen.generate()
    
    # Count total passages (removed walls)
    # In a perfect maze: passages = cells - 1
    total_cells = maze.width * maze.height
    
    # Count removed walls (each passage is counted twice, once from each side)
    passages = 0
    for y in range(maze.height):
        for x in range(maze.width):
            cell_val = maze.get_cell_value(y, x)
            # Count how many walls are OPEN (bit = 0)
            # 0xF = 1111 (all closed)
            # Each 0 bit = open wall
            walls_closed = bin(cell_val).count('1')
            walls_open = 4 - walls_closed
            passages += walls_open
    
    # Each passage counted twice, so divide by 2
    actual_passages = passages // 2
    expected_passages = total_cells - 1
    
    print(f"\nTotal cells: {total_cells}")
    print(f"Expected passages (for perfect maze): {expected_passages}")
    print(f"Actual passages: {actual_passages}")
    
    if actual_passages == expected_passages:
        print("✅ PASS: Perfect maze! (Exactly one path between any two cells)")
    else:
        print(f"❌ FAIL: Not a perfect maze! (Expected {expected_passages}, got {actual_passages})")
    
    print()


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("RUNNING ALL TESTS")
    print("=" * 50 + "\n")
    
    test_basic_generation()
    test_reproducibility()
    test_different_seeds()
    test_larger_maze()
    test_tiny_maze()
    test_perfect_maze()
    
    print("=" * 50)
    print("ALL TESTS COMPLETE!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()