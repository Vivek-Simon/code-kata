import os
import pytest
from unittest.mock import patch
from data_generator import (
    generate_random_string,
    generate_fixed_width_file
)

# Test for generating a random string of the correct length
@patch('random.choices')
def test_generate_random_string_length(mock_choices):
    length = 10
    # Mock the return value of random.choices
    mock_choices.return_value = ['A'] * length
    result = generate_random_string(length)
    assert len(result) == length, f"Expected length {length}, but got {len(result)}"

# Test for generating a random string with the correct content
@patch('random.choices')
def test_generate_random_string_content(mock_choices):
    length = 5
    # Mock the return value of random.choices
    mock_choices.return_value = ['A', 'B', 'C', 'D', 'E']
    result = generate_random_string(length)
    assert result == 'ABCDE', f"Expected 'ABCDE', but got {result}"

# Test for generating an empty string when length is 0
def test_generate_random_string_empty():
    length = 0
    result = generate_random_string(length)
    assert result == '', "Expected empty string for length 0"

# Test for generating a random string with invalid length
def test_generate_random_string_invalid_length():
    length = -5
    result = generate_random_string(length)
    assert result == '', "Expected empty string for negative length"

# Black box testing on the generate_fixed_width_file function
def test_generate_fixed_width_file():
    data_to_process = [0,1,2]
    spec_data = {
        "offset": {
            "field1": 10,
            "field2": 5
        }
    }
    tmp_file_name = generate_fixed_width_file(data_to_process, spec_data)
    try:
        with open(tmp_file_name, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
        # Check if all lines have exactly 15 characters (excluding newline)
        for line in lines:
            line = line.rstrip('\n')
            assert len(line) == sum(spec_data["offset"].values()), f"Line length is not 15 characters. Length: {len(line)}. Line: {line}"
    finally:
        # Clean up: remove the temporary file
        if os.path.exists(tmp_file_name):
            os.remove(tmp_file_name)

def test_generate_fixed_width_file_exception():
    data_to_process = [0, 1, 2]
    spec_data = {
        "offset": {
            "field1": '10a',
            "field2": '5b'
        }
    }     
    # Ensure that the exception is raised and logged
    with pytest.raises(Exception, match="'str' object cannot be interpreted as an integer"):
        generate_fixed_width_file(data_to_process, spec_data)