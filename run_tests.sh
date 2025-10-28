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

# Check if "utils" argument is provided
if [ "$1" = "utils" ]; then
    echo "Running utils tests (test_html_widget.py and test_weather_endpoint.py)..."
    # Run both utils test files
    TEST_FILES="test_html_widget test_weather_endpoint"
else
    echo "Running tests to check your work..."
    # Find all test files that start with "test" but not the utils test files
    TEST_FILES=$(find . -name "test*.py" -not -name "test_html_widget.py" -not -name "test_weather_endpoint.py" -type f | sed 's|^\./||' | sed 's|\.py$||' | tr '\n' ' ')
fi

# Run each test file
for test_file in $TEST_FILES; do
    echo "Running $test_file..."
    python -m unittest $test_file -v
done