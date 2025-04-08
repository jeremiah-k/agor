from setuptools import setup, find_packages

setup(
    name="agentgrunt",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "httpx",
        "plumbum",
        "pydantic",
        "pyperclip",
        "pytest",
        "tqdm",
        "typer",
        "platformdirs>=4.3.7,<5.0.0",
    ],
    entry_points={
        "console_scripts": [
            "agentgrunt=agentgrunt.main:app",
        ],
    },
)
