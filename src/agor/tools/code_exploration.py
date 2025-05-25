import os
import re
from typing import List, Optional, Tuple


def bfs_find(base: str, pattern: str) -> List[str]:
    """Breadth-first search for filenames matching a pattern

    Args:
        base: Base directory to search from
        pattern: Regex pattern to match filenames against

    Returns:
        List of full paths to matching files
    """
    if not os.path.exists(base):
        return []

    queue = [base]
    matched_files = []

    while queue:
        current_path = queue.pop(0)
        try:
            if os.path.isdir(current_path):
                for entry in os.listdir(current_path):
                    full_path = os.path.join(current_path, entry)
                    if os.path.isdir(full_path):
                        queue.append(full_path)
                    elif re.search(pattern, entry):
                        matched_files.append(full_path)
        except (PermissionError, OSError):
            # Skip directories we can't read
            continue

    return matched_files


def grep(
    file_path: str, pattern: str, recursive: bool = False
) -> List[Tuple[str, int, str]]:
    """Search for a pattern in a file or a directory (recursively)

    Args:
        file_path: Path to file or directory to search
        pattern: Regex pattern to search for
        recursive: If True and file_path is a directory, search recursively

    Returns:
        List of tuples: (file_path, line_number, matching_line)
    """
    matches = []

    if not os.path.exists(file_path):
        return matches

    if os.path.isdir(file_path) and recursive:
        for root, _, files in os.walk(file_path):
            for file in files:
                matches.extend(grep(os.path.join(root, file), pattern))
    elif os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_no, line in enumerate(f, start=1):
                    if re.search(pattern, line):
                        matches.append((file_path, line_no, line.strip()))
        except (PermissionError, OSError):
            # Skip files we can't read
            pass

    return matches


def tree(directory: str, prefix: str = "", depth_remaining: int = 3) -> str:
    """Generate a directory tree structure

    Args:
        directory: Directory path to generate tree for
        prefix: Current prefix for tree formatting (used internally)
        depth_remaining: Maximum depth to traverse

    Returns:
        String representation of directory tree
    """
    if (
        depth_remaining < 0
        or not os.path.exists(directory)
        or not os.path.isdir(directory)
    ):
        return ""

    try:
        contents = os.listdir(directory)
    except (PermissionError, OSError):
        return f"{prefix}[Permission Denied]"

    entries = []
    for i, entry in enumerate(sorted(contents)):
        is_last = i == len(contents) - 1
        new_prefix = prefix + ("└── " if is_last else "├── ")
        child_path = os.path.join(directory, entry)

        if os.path.isdir(child_path):
            entries.append(new_prefix + entry + "/")
            subtree = tree(
                child_path,
                prefix + ("    " if is_last else "│   "),
                depth_remaining - 1,
            )
            if subtree:  # Only extend if subtree is not empty
                entries.extend(subtree.split("\n"))
        else:
            entries.append(new_prefix + entry)

    return "\n".join(filter(None, entries))  # Filter out empty strings


def find_function_signatures(file_path: str, language: str) -> List[Tuple[int, str]]:
    """
    Find function signatures in a file.

    Args:
        file_path: Path to the source file
        language: Programming language (python, javascript, c, cpp, ruby, go, rust)

    Returns:
        List of tuples: (line_number, matching_signature)
    """
    if not file_path or not os.path.exists(file_path):
        return []

    patterns = {
        "javascript": [
            r"function\s+[a-zA-Z_$][\w$]*\s*\(",  # Named function
            r"\bfunction\s*\(",  # Anonymous function
            r"[a-zA-Z_$][\w$]*\s*=\s*function\s*\(",  # Function assigned to a variable
            r"[a-zA-Z_$][\w$]*\s*=\s*\([^)]*\)\s*=>",  # Arrow function assigned to a variable
            r"[a-zA-Z_$][\w$]*\s*:\s*function\s*\(",  # Method in an object literal (named function)
            r"[a-zA-Z_$][\w$]*\s*:\s*\([^)]*\)\s*=>",  # Method in an object literal (arrow function)
            r"export\s+function\s+[a-zA-Z_$][\w$]*\(",  # Named exported function
            r"export\s+default\s+function\s*[a-zA-Z_$][\w$]*\s*\(",  # Default exported function (named)
            r"export\s+default\s+function\s*\(",  # Default exported function (anonymous)
            r"class\s+[a-zA-Z_$][\w$]*",  # Class definitions
            r"[a-zA-Z_$][\w$]*\s*\([^)]*\)\s*{",  # Method definitions
        ],
        "typescript": [
            r"function\s+[a-zA-Z_$][\w$]*\s*\(",
            r"[a-zA-Z_$][\w$]*\s*=\s*\([^)]*\)\s*=>",
            r"class\s+[a-zA-Z_$][\w$]*",
            r"interface\s+[a-zA-Z_$][\w$]*",
            r"type\s+[a-zA-Z_$][\w$]*\s*=",
        ],
        "python": [
            r"def\s+[a-zA-Z_][\w]*\s*\(",  # Function definitions
            r"class\s+[a-zA-Z_][\w]*",  # Class definitions
            r"async\s+def\s+[a-zA-Z_][\w]*\s*\(",  # Async function definitions
        ],
        "c": [r"\w+\s+[a-zA-Z_][\w]*\s*\([^)]*\)\s*{"],  # Function definitions
        "cpp": [
            r"\w+\s+[a-zA-Z_][\w]*\s*\([^)]*\)\s*{",  # Function definitions
            r"class\s+[a-zA-Z_][\w]*",  # Class definitions
            r"struct\s+[a-zA-Z_][\w]*",  # Struct definitions
        ],
        "java": [
            r"\w+\s+[a-zA-Z_][\w]*\s*\([^)]*\)\s*{",  # Method definitions
            r"class\s+[a-zA-Z_][\w]*",  # Class definitions
            r"interface\s+[a-zA-Z_][\w]*",  # Interface definitions
        ],
        "ruby": [
            r"def\s+[a-zA-Z_][\w]*",  # Method definitions
            r"class\s+[a-zA-Z_][\w]*",  # Class definitions
            r"module\s+[a-zA-Z_][\w]*",  # Module definitions
        ],
        "go": [
            r"func\s+[a-zA-Z_][\w]*\s*\(",  # Function definitions
            r"type\s+[a-zA-Z_][\w]*\s+struct",  # Struct definitions
            r"type\s+[a-zA-Z_][\w]*\s+interface",  # Interface definitions
        ],
        "rust": [
            r"fn\s+[a-zA-Z_][\w]*\s*\(",  # Function definitions
            r"struct\s+[a-zA-Z_][\w]*",  # Struct definitions
            r"enum\s+[a-zA-Z_][\w]*",  # Enum definitions
            r"trait\s+[a-zA-Z_][\w]*",  # Trait definitions
        ],
    }

    matches = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                for pattern in patterns.get(language.lower(), []):
                    match = re.search(pattern, line.strip())
                    if match:
                        matches.append((line_no, line.strip()))
                        break  # Only match one pattern per line
    except (PermissionError, OSError):
        pass

    return matches


def extract_function_content(
    language: str, signature: str, content: List[str]
) -> Optional[List[str]]:
    """
    Extracts the content of a function given its signature and the content of the file.

    Args:
        language: The programming language
        signature: The function signature to find
        content: The content of the file as list of lines

    Returns:
        List of lines that make up the function, or None if not found
    """
    if not content or not signature:
        return None

    language = language.lower()
    if language == "python":
        return extract_python_function(signature, content)
    elif language in ["ruby"]:
        return extract_ruby_function(signature, content)
    else:  # Default to handling curly brace languages like JavaScript, C, C++, Java, etc.
        return extract_curly_brace_function(signature, content)


def extract_python_function(signature: str, content: List[str]) -> Optional[List[str]]:
    start_line = None
    end_line = None
    for idx, line in enumerate(content):
        if signature in line:
            start_line = idx
            break

    if start_line is None:
        return None

    signature_end_line = start_line
    # If the signature ends on the same line, use the start_line as the signature_end_line
    if "):" in content[start_line]:
        signature_end_line = start_line
    else:
        for idx, line in enumerate(content[start_line + 1 :]):
            if "):" in line:
                signature_end_line = start_line + idx + 1
                break

    initial_indent = len(content[signature_end_line + 1]) - len(
        content[signature_end_line + 1].lstrip()
    )
    indent_stack = [initial_indent]
    for idx, line in enumerate(content[signature_end_line + 1 :]):
        current_indent = len(line) - len(line.lstrip())
        if current_indent > indent_stack[-1] and line.strip():
            indent_stack.append(current_indent)
        elif current_indent <= indent_stack[-1] and line.strip():
            while indent_stack and current_indent < indent_stack[-1]:
                indent_stack.pop()
            if not indent_stack:
                end_line = signature_end_line + idx + 1
                break

    return content[start_line : (end_line or signature_end_line + 1) + 1]


def extract_curly_brace_function(
    signature: str, content: List[str]
) -> Optional[List[str]]:
    start_line = None
    brace_count = 0
    for idx, line in enumerate(content):
        if signature in line:
            start_line = idx
            break

    if start_line is None:
        return None

    end_line = start_line

    for idx, line in enumerate(content[start_line:]):
        brace_count += line.count("{") - line.count("}")
        if brace_count == 0:
            end_line = start_line + idx
            break

    return content[start_line : end_line + 1]


def extract_ruby_function(signature: str, content: List[str]) -> Optional[List[str]]:
    """Extract Ruby function/method content based on def...end blocks"""
    start_line = None
    for idx, line in enumerate(content):
        if signature in line and "def " in line:
            start_line = idx
            break

    if start_line is None:
        return None

    # Find matching 'end'
    indent_level = len(content[start_line]) - len(content[start_line].lstrip())
    for idx in range(start_line + 1, len(content)):
        line = content[idx]
        if line.strip() == "end" and (len(line) - len(line.lstrip())) == indent_level:
            return content[start_line : idx + 1]

    return content[start_line:]  # Return to end of file if no matching 'end' found


def get_file_language(file_path: str) -> str:
    """Determine programming language from file extension

    Args:
        file_path: Path to the file

    Returns:
        Language name (lowercase) or 'unknown'
    """
    if not file_path:
        return "unknown"

    ext = os.path.splitext(file_path)[1].lower()

    language_map = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".hpp": "cpp",
        ".java": "java",
        ".rb": "ruby",
        ".go": "go",
        ".rs": "rust",
        ".php": "php",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
        ".pl": "perl",
        ".r": "r",
        ".R": "r",
        ".swift": "swift",
        ".kt": "kotlin",
        ".scala": "scala",
    }

    return language_map.get(ext, "unknown")


def analyze_file_structure(file_path: str) -> dict:
    """Analyze a source file and return structural information

    Args:
        file_path: Path to the source file

    Returns:
        Dictionary with file analysis information
    """
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return {"error": "File not found or not a file"}

    language = get_file_language(file_path)

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except (PermissionError, OSError) as e:
        return {"error": f"Cannot read file: {e}"}

    # Basic metrics
    total_lines = len(lines)
    non_empty_lines = len([line for line in lines if line.strip()])

    # Find functions/classes
    signatures = find_function_signatures(file_path, language)

    # Count imports/includes
    import_patterns = {
        "python": [r"^\s*(import|from)\s+"],
        "javascript": [r"^\s*(import|require)\s*"],
        "typescript": [r"^\s*(import|require)\s*"],
        "c": [r"^\s*#include\s*"],
        "cpp": [r"^\s*#include\s*"],
        "java": [r"^\s*import\s+"],
        "go": [r"^\s*import\s*"],
        "rust": [r"^\s*use\s+"],
    }

    imports = []
    for line_no, line in enumerate(lines, 1):
        for pattern in import_patterns.get(language, []):
            if re.search(pattern, line):
                imports.append((line_no, line.strip()))
                break

    return {
        "file_path": file_path,
        "language": language,
        "total_lines": total_lines,
        "non_empty_lines": non_empty_lines,
        "functions_classes": len(signatures),
        "imports": len(imports),
        "signatures": signatures[:10],  # First 10 signatures
        "import_lines": imports[:5],  # First 5 imports
    }
