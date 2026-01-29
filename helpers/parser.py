#!/usr/bin/env python

from typing import Dict, List, Any
import sys
import os


def first_args_validation() -> Dict[str, str]:
    """
    Validate file operations (exist and proper permission),
    Validate proper syntax

    Returns:
        Config dict with everything as strings
        Exit the program if errors
    """
    config_variables: List[str] = []
    valid_configs: List[tuple] = []
    errors: List[str] = []

    if len(sys.argv) < 2:
        print("ERROR: No configuration provided."
              "\nUsage: python3 a_maze_ing.py <config.txt>")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("WARNING: Too many arguments provided."
              "Only the first one will be used\n")

    # File-level errors handling:
    # File not found, Cannot open file, No read permission
    config_file: Any = sys.argv[1]
    try:
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                config_variables.append(line)
    except FileNotFoundError:
        print(f"[Error]: Cannot open file '{config_file}'\n"
              "Error detail: File not found")
        sys.exit(1)
    except PermissionError:
        print(f"[Error]: Cannot open file '{config_file}'\n"
              "Error detail: Permission error")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    # Second-level errors handling:
    # Syntax error (formatting):
    for config in config_variables:
        # check for Wrong format (= instead of :)
        if '=' not in config and ':' in config:
            errors.append("Wrong configuration format: ':' "
                          f"is used instead of '=' in {config}")
            continue

        # check for extra "=" symbol
        if config.count('=') != 1:
            errors.append("Bad configuration syntax: "
                          f"use of multiple '=' in {config}")
            continue

        key, value = config.split('=')

        # check for missing key or missing value
        if not key:
            errors.append("Bad configuration syntax: "
                          f"missing key in: {config}")
            continue
        if not value:
            errors.append("Bad configuration syntax: "
                          f"missing value in: {config}")
            continue

        # take if valid
        valid_configs.append((key, value))

    # Check if there's any error, print them and exit the program
    if errors:
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    # return if all configs are valid
    return dict(valid_configs)


def semantic_validation(config_values: Dict[str, str]) -> Dict[str, Any]:
    """
    Validate and convert config values to proper types.

    Args:
        config_values: Raw config dict (all strings)

    Returns:
        Typed config dict with proper types
    """
    updated_config_values: Dict[str, Any] = config_values
    typed_configs: Dict = {}
    errors: List[str] = []

    # ============================================================
    # Check for all the mandatory keys
    required_keys: List[str] = ["WIDTH", "HEIGHT", "ENTRY",
                                "EXIT", "OUTPUT_FILE", "PERFECT"]
    missing_keys: List = [k for k in required_keys if k not in config_values]

    if missing_keys:
        print("Semantic error found:")
        for err in missing_keys:
            print(f" - {err}")
        sys.exit(1)

    # ============================================================
    # validate WIDTH & HEIGHT convert to int and must be > 0
    for key in ("WIDTH", "HEIGHT"):
        try:
            num = int(config_values[key])
            if num <= 0:
                errors.append(f"{key} must be > 0")
            typed_configs[key] = num
            del updated_config_values[key]
        except ValueError:
            errors.append(f"{key} must be integer, "
                          f"got '{config_values[key]}' instead")

    if errors:
        print("Semantic error found:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    width, height = typed_configs["WIDTH"], typed_configs["HEIGHT"]

    # ============================================================
    # Validate and Parse ENTRY AND EXIT
    splitted_entry = config_values["ENTRY"].split(',')
    splitted_exit = config_values["EXIT"].split(',')

    # Check if we have exactly 2 coordinates x and y for both ENTRY AND EXIT
    if len(splitted_entry) != 2:
        errors.append(f"ENTRY must have exactly 2 values (x,y), "
                      f"got {len(splitted_entry)}")
    if len(splitted_exit) != 2:
        errors.append(f"EXIT must have exactly 2 values (x,y), "
                      f"got {len(splitted_exit)}")

    # helper to check if the ENTRY and EXIT are at the border of the maze
    # ONLY IF THE PARSING SUCCEED
    def is_at_border(x: int, y: int, width: int, height: int) -> bool:
        """Check if coordinate is at external border of maze."""
        return x == 0 or x == width - 1 or y == 0 or y == height - 1

    # ENTRY and EXIT cannot be at the same coordinates
    if splitted_entry == splitted_exit:
        errors.append("ENTRY and EXIT coordinates cannot be the same")
    else:
        successful_entry_parsing = False
        # Checking for the ENTRY coordinates
        try:
            y = int(splitted_entry[0])
            x = int(splitted_entry[1])
            if x < 0 or y < 0:
                errors.append("ENTRY coordinates cannot be negative")
            elif y >= width or x >= height:
                if y >= width:
                    errors.append(f"In 'ENTRY' coordinates line: "
                                  f"{y} value is out of WIDTH bounds")
                else:
                    errors.append(f"In 'ENTRY' coordinates line: "
                                  f"{x} value is out of HEIGHT bounds")
            else:
                typed_configs["ENTRY"] = (y, x)
                del updated_config_values["ENTRY"]
                successful_entry_parsing = True
        except ValueError:
            errors.append(f"Invalid ENTRY value: {splitted_entry}")

        # After parsing coordinates, check if it's at the border:
        if successful_entry_parsing:
            if not is_at_border(typed_configs["ENTRY"][1],
                                typed_configs["ENTRY"][0],
                                typed_configs["WIDTH"],
                                typed_configs["HEIGHT"]):
                errors.append("ENTRY must be at external border of the maze")

        # Checking for the EXIT coordinates
        successful_exit_parsing = False
        try:
            y = int(splitted_exit[0])
            x = int(splitted_exit[1])
            if x < 0 or y < 0:
                errors.append("EXIT coordinates cannot be negative")
            elif y >= width or x >= height:
                if y >= width:
                    errors.append(f"In 'EXIT' coordinates line: "
                                  f"{y} value is out of WIDTH bounds")
                else:
                    errors.append(f"In 'EXIT' coordinates line: "
                                  f"{x} value is out of HEIGHT bounds")
            else:
                typed_configs["EXIT"] = (y, x)
                del updated_config_values["EXIT"]
                successful_exit_parsing = True
        except ValueError:
            errors.append(f"Invalid EXIT value: {splitted_exit}")

        # After parsing coordinates, check if it's at the border:
        if successful_exit_parsing:
            if not is_at_border(typed_configs["EXIT"][1],
                                typed_configs["EXIT"][0],
                                typed_configs["WIDTH"],
                                typed_configs["HEIGHT"]):
                errors.append("EXIT must be at external border of the maze")

    # check if there's any errors and exit
    if errors:
        print("Semantic error found:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    # ============================================================
    #  Check for valid parsable bool value for PERFECT config varibale
    valid_bool = ["TRUE", "FALSE", "0", "1", "YES", "NO"]
    if config_values["PERFECT"].upper() in valid_bool:
        if config_values["PERFECT"].upper() in ["TRUE", "1", "YES"]:
            typed_configs["PERFECT"] = True
        else:
            typed_configs["PERFECT"] = False
        del updated_config_values["PERFECT"]
    else:
        errors.append("In 'PERFECT' configuration line: "
                      f"'{config_values['PERFECT']}' is not a valid "
                      "parsable boolean value. Please use 'True/False', "
                      "'1/0' or 'Yes/No'")

    if errors:
        print("Semantic error found:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    # ============================================================
    #  Check for valid path and file name for the OUTPUT_FILE config variable

    # Check for valid OUTPUT_FILE
    output_file = config_values["OUTPUT_FILE"]

    # 1. Check it's not empty
    if not output_file.strip():
        errors.append("OUTPUT_FILE cannot be empty")
    else:
        # 2. Check if it contains invalid characters for the OS
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in output_file for char in invalid_chars):
            errors.append(f"OUTPUT_FILE contains invalid characters: "
                          f"{output_file}")

        # 3. Check if directory exists (if path is specified)
        # If there's a directory part (e.g., "output/maze.txt")
        directory = os.path.dirname(output_file)
        if directory:
            if not os.path.exists(directory):
                errors.append(f"Directory does not exist: {directory}")
            elif not os.path.isdir(directory):
                errors.append(f"Path is not a directory: {directory}")
            elif not os.access(directory, os.W_OK):
                errors.append(f"No write permission for directory: "
                              f"{directory}")
        # Just a filename like "maze.txt" - writes to current dir
        else:
            if not os.access('.', os.W_OK):
                errors.append("No write permission in current directory")

        # If all checks pass, store it to the dictionnary that we return
        typed_configs["OUTPUT_FILE"] = output_file
        del updated_config_values["OUTPUT_FILE"]

    if errors:
        print("Semantic error found:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    # ============================================================
    # OPTIONAL CONFIGS
    # SEED (optional, int)
    if "SEED" in config_values:
        try:
            seed = int(config_values["SEED"])
            typed_configs["SEED"] = seed
            del updated_config_values["SEED"]
        except ValueError:
            errors.append(f"Invalid SEED: must be an integer, "
                          f"got '{config_values['SEED']}' instead")

    # VISUAL (optional, string)
    if "VISUAL" in config_values:
        typed_configs["VISUAL"] = config_values["VISUAL"]
        del updated_config_values["VISUAL"]

    # ALGORITHM (optional, string)
    if "ALGORITHM" in config_values:
        typed_configs["ALGORITHM"] = config_values["ALGORITHM"]
        del updated_config_values["ALGORITHM"]

    # DISPLAY MODE (optional, string)
    if "DISPLAY MODE" in config_values:
        typed_configs["DISPLAY MODE"] = config_values["DISPLAY MODE"]
        del updated_config_values["DISPLAY MODE"]

    if errors:
        print("Semantic error found:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    # getting the rest of the valid configs in case we will need them
    typed_configs.update(updated_config_values)

    # return final_dict
    return typed_configs
