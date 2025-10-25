#!/bin/bash

# Simple test runner for She Codes Python Project 2.0
# Activates virtual environment and runs tests

set -e  # Exit on any error

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to project directory
cd "$SCRIPT_DIR"

echo "Activating virtual environment..."
source .venv/bin/activate

# Add the src directory to Python path
export PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH"

# Change to tests directory and run tests
cd tests

# Check if "check_widget" argument is provided
if [ "$1" = "check_widget" ]; then
    echo "Running only test_html_widget.py..."
    # Only run the widget test file
    TEST_FILES="test_html_widget"
else
    echo "Running tests to check your work..."
    # Find all test files that start with "test" but not "test_html_widget"
    TEST_FILES=$(find . -name "test*.py" -not -name "test_html_widget.py" -type f | sed 's|^\./||' | sed 's|\.py$||' | tr '\n' ' ')
fi

# Run each test file
for test_file in $TEST_FILES; do
    echo "Running $test_file..."
    python -m unittest $test_file -v
done