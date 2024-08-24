import argparse
import os
from typing import List, Optional, Tuple

"""
Simple CLI that generates an overview of a filesystem by exploring the directory structure
and looking for README.md files.
"""

def read_readme_content(file_path: str, max_chars: int = 1000) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read(max_chars)
    except IOError:
        return "Error: Unable to read README.md file"

def explore_directory(
    directory: str,
    max_depth: int,
    show_all_dirs: bool,
    current_depth: int = 0
) -> List[Tuple[str, Optional[str]]]:
    if current_depth > max_depth:
        return []

    result = []
    readme_path = os.path.join(directory, "README.md")
    
    if os.path.isfile(readme_path):
        readme_content = read_readme_content(readme_path)
        result.append((directory, readme_content))
    elif show_all_dirs:
        result.append((directory, None))
    else:
        return []  # Skip directories without README if show_all_dirs is False

    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                result.extend(explore_directory(item_path, max_depth, show_all_dirs, current_depth + 1))
    except PermissionError:
        print(f"Warning: Permission denied to access {directory}")

    return result

def generate_report(root_directory: str, structure: List[Tuple[str, Optional[str]]]) -> str:
    report = ""
    for directory, readme_content in structure:
        dir_name = directory.removeprefix(root_directory)
        if dir_name == "":
            dir_name = "/"
        report += f"\n{dir_name}\n"
        if readme_content:
            indented_content = "\n".join("    " + line for line in readme_content[:1000].split("\n"))
            report += f"{indented_content}\n\n"
    return report

def main(root_directory: str, max_depth: int, show_all_dirs: bool) -> None:
    if not os.path.isdir(root_directory):
        print(f"Error: {root_directory} is not a valid directory")
        return

    structure = explore_directory(root_directory, max_depth, show_all_dirs)
    report = generate_report(root_directory, structure)
    print(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a report of directory structure and README contents")
    parser.add_argument("directory", help="Root directory to start the exploration")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum depth for directory traversal (default: 3)")
    parser.add_argument("--show-all-dirs", action="store_true", help="Show directories without README files (default: False)")
    args = parser.parse_args()

    main(args.directory, args.max_depth, args.show_all_dirs)