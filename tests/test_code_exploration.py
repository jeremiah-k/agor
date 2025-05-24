from agor.tools.code_exploration import (
    extract_curly_brace_function,
    extract_function_content,
    extract_python_function,
)


def test_extract_python_function():
    content_single_line = [
        "def example_function(param1, param2):",
        "    return param1 + param2",
    ]
    assert (
        extract_python_function("def example_function(", content_single_line)
        == content_single_line
    )

    content_multi_line = [
        "def process_response(",
        "        self, response, level=0):",
        "    return response",
    ]
    assert (
        extract_python_function("def process_response(", content_multi_line)
        == content_multi_line
    )

    assert (
        extract_python_function("def nonexistent_function(", content_single_line)
        is None
    )


def test_extract_curly_brace_function():
    content_js = [
        "function exampleFunction(param1, param2) {",
        "    return param1 + param2;",
        "}",
    ]
    assert (
        extract_curly_brace_function("function exampleFunction(", content_js)
        == content_js
    )

    assert (
        extract_curly_brace_function("function nonexistentFunction(", content_js)
        is None
    )


def test_extract_function_content():
    content_python_single_line = [
        "def example_function(param1, param2):",
        "    return param1 + param2",
    ]
    assert (
        extract_function_content(
            "python", "def example_function(", content_python_single_line
        )
        == content_python_single_line
    )

    content_js = [
        "function exampleFunction(param1, param2) {",
        "    return param1 + param2;",
        "}",
    ]
    assert (
        extract_function_content("javascript", "function exampleFunction(", content_js)
        == content_js
    )
