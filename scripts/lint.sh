#!/usr/bin/env bash

set -e
set -x

cd "$(dirname "$0")/.." || exit

# Run type checking with mypy
echo "Running mypy for type checking..."
mypy app

# Run linting with ruff
echo "Running ruff for linting..."
ruff check app

# Run ruff for formatting check
echo "Checking formatting with ruff..."
ruff format app --check
