"""Coding Challenge Code Checker

Use this tool to collect coding challenge projects, run and evaluate them.
Configure using YAML notation and produce output in many formats.

Rode map before release 0.1.0:
1. Read YAML file codechecker.yml in the root of a repository
2. Execute code inside a project
3. Produce output in txt format
"""

from .codechecker import main

if __name__ == "__main__":
  main()
