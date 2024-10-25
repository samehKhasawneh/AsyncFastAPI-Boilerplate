#!/bin/sh -e
set -x

# Run ruff for linting and fixing issues
echo "Running ruff for linting and fixing..."
ruff check app scripts --fix

# Run ruff for formatting
echo "Running ruff for formatting..."
ruff format app scripts
