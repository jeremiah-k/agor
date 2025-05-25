# Code Exploration Tools Documentation

This document provides detailed information about the code exploration tools available to AGOR AI assistants.

## Available Functions

### File Search Functions

#### `bfs_find(base: str, pattern: str) -> List[str]`

Performs breadth-first search for filenames matching a pattern.

**Parameters:**

- `base`: Starting directory path
- `pattern`: Regular expression pattern to match filenames

**Returns:** List of file paths matching the pattern

**Example:**

```python
# Find all Python files
python_files = bfs_find("/path/to/repo", r"\.py$")

# Find all test files
test_files = bfs_find("/path/to/repo", r"test.*\.py$")
```

#### `grep(file_path: str, pattern: str, recursive: bool = False) -> List[Tuple[str, int, str]]`

Search for text patterns in files or directories. Use this as a last resort, preferring the provided git binary's `git grep` feature.

**Parameters:**

- `file_path`: File or directory path to search
- `pattern`: Regular expression pattern to search for
- `recursive`: If True, search recursively through directories

**Returns:** List of tuples containing (file_path, line_number, matching_line)

**Example:**

```python
# Search for function definitions in a file
matches = grep("main.py", r"def \w+")

# Recursively search for TODO comments
todos = grep("/path/to/repo", r"TODO|FIXME", recursive=True)
```

### Directory Structure Functions

#### `tree(directory: str, prefix: str = "", depth_remaining: int = 3) -> str`

Generate a visual directory tree representation.

**Parameters:**

- `directory`: Directory path to visualize
- `prefix`: Internal parameter for formatting (leave default)
- `depth_remaining`: Maximum depth to traverse

**Returns:** String representation of directory tree

**Example:**

```python
# Show project structure
structure = tree("/path/to/repo")
print(structure)
```

### Function Analysis Functions

#### `find_function_signatures(file_path: str, language: str) -> List[Tuple[int, str]]`

Find function signatures in a file based on programming language.

**Parameters:**

- `file_path`: Path to the source file
- `language`: Programming language ("python", "javascript", "c", "cpp", "ruby", "go", "rust")

**Returns:** List of tuples containing (line_number, function_signature)

**Supported Languages:**

- **Python**: `def function_name(`
- **JavaScript**: Various function patterns including arrow functions
- **C/C++**: Function definitions with braces
- **Ruby**: `def function_name`
- **Go**: `func function_name(`
- **Rust**: `fn function_name(`

#### `extract_function_content(language: str, signature: str, content: List[str]) -> Optional[List[str]]`

Extract the complete content of a function given its signature.

**Parameters:**

- `language`: Programming language
- `signature`: Function signature to find
- `content`: List of file lines

**Returns:** List of lines containing the complete function, or None if not found

#### `extract_python_function(signature: str, content: List[str]) -> Optional[List[str]]`

Python-specific function extraction using indentation analysis.

#### `extract_curly_brace_function(signature: str, content: List[str]) -> Optional[List[str]]`

Extract functions from languages that use curly braces (JavaScript, C, C++, etc.).

## Usage Patterns

### Comprehensive Code Analysis

```python
# 1. Get file listing
files = bfs_find(".", r"\.(py|js|cpp|h)$")

# 2. Find all functions
all_functions = []
for file_path in files:
    if file_path.endswith('.py'):
        functions = find_function_signatures(file_path, 'python')
    elif file_path.endswith('.js'):
        functions = find_function_signatures(file_path, 'javascript')
    # ... handle other languages
    all_functions.extend([(file_path, f) for f in functions])

# 3. Search for specific patterns
api_calls = grep(".", r"requests\.|fetch\(", recursive=True)
error_handling = grep(".", r"try:|except:|catch\(", recursive=True)
```

### Function Dependency Analysis

```python
# Find function calls to analyze dependencies
function_calls = grep(".", r"(\w+)\s*\(", recursive=True)

# Find imports and includes
imports = grep(".", r"^(import|from|#include|require)", recursive=True)
```

## Best Practices

1. **Start with broad searches** using `bfs_find` to understand project structure
2. **Use recursive grep** to find patterns across the entire codebase
3. **Combine tools** for comprehensive analysis (structure + content + functions)
4. **Language-specific analysis** using appropriate function signature detection
5. **Extract complete functions** when you need to understand implementation details

## Integration with AGOR

These tools are automatically available in the AGOR environment. Use them to:

- **Analyze codebases** before making changes
- **Find related code** when implementing features
- **Understand project structure** and dependencies
- **Locate specific patterns** or anti-patterns
- **Extract functions** for detailed analysis or modification

The tools work seamlessly with git operations and can help you make informed decisions about code changes.
