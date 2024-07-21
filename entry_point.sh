#!/bin/sh

# Ensure the script exits on error
set -e

# Print the environment for debugging purposes
echo "Running entrypoint.sh"

echo "Installing packages specified in the requirements file."
pip install -r ../requirements.txt

echo "Running test cases and generating html report."
coverage run -m pytest && coverage html

echo "Test report available in code-kata\scripts\htmlcov\index.html"