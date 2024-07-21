import os
import csv
import pytest
from unittest import mock
from file_processing import (
                                write_csv_to_temp_file,
                                create_output_file,
                                read_file_in_chunks,
                                write_to_temp_file
                            )

def test_write_csv_to_temp_file_valid_data():
    data = [
        ['Name', 'Age', 'City'],
        ['User1', '30', 'Melbourne'],
        ['User2', '25', 'Canberra'],
        ['User3', '35', 'Sydney']
    ]
    
    temp_file_name = write_csv_to_temp_file(data)
    
    try:
        with open(temp_file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            read_data = list(reader)
        
        assert read_data == data, f"Expected {data}, but got {read_data}"
    finally:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

def test_write_csv_to_temp_file_empty_data():
    data = []
    
    temp_file_name = write_csv_to_temp_file(data)
    
    try:
        with open(temp_file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            read_data = list(reader)
        
        assert read_data == data, f"Expected {data}, but got {read_data}"
    finally:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

def test_write_csv_to_temp_file_special_characters():
    data = [
        ['Name', 'Age', 'City'],
        ['User1', '30', 'Melbou\nrne'],
        ['User2', '25', 'Canb,erra'],
        ['User3', '35', 'Sydn"ey']
    ]
    
    temp_file_name = write_csv_to_temp_file(data)
    
    try:
        with open(temp_file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            read_data = list(reader)
        
        assert read_data == data, f"Expected {data}, but got {read_data}"
    finally:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

def test_create_output_file_with_headers():
    """ Test creating an output file with headers """
    data = [["a", "b"], ["c", "d"]]
    headers = ["header1", "header2"]
    temp_file = write_csv_to_temp_file(data)
    output_file_name = 'output_with_headers.csv'
    
    create_output_file([temp_file], output_file_name, headers=headers)
    
    with open(output_file_name, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')
        assert content[0] == ','.join(headers)
        assert len(content) == len(data) + 1  # 1 header row + number of data rows
    
    os.remove(output_file_name)

def test_create_output_file_without_headers():
    """ Test creating an output file without headers """
    data = [["a", "b"], ["c", "d"]]
    temp_file = write_csv_to_temp_file(data)
    output_file_name = 'output_without_headers.csv'
    
    create_output_file([temp_file], output_file_name)
    
    with open(output_file_name, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')
        assert len(content) == len(data)  # Number of rows should match
    
    os.remove(output_file_name)

def test_create_output_file_empty_input():
    """ Test creating an output file with no temporary files """
    output_file_name = 'output_empty_input.csv'
    
    create_output_file([], output_file_name)
    
    assert os.path.exists(output_file_name)
    with open(output_file_name, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        assert content == ''  # File should be empty
    
    os.remove(output_file_name)

def test_create_output_file_empty_data():
    """ Test creating an output file with empty temporary files """
    temp_file = write_csv_to_temp_file([])
    output_file_name = 'output_empty_data.csv'
    
    create_output_file([temp_file], output_file_name)
    
    with open(output_file_name, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        assert content == ''  # File should be empty
    
    os.remove(output_file_name)

def test_readfile_in_chunks_basic():
    """ Test reading file in chunks with a small file and standard chunk size """
    file_content = "line1\nline2\nline3\nline4\nline5\n"
    file_path = 'test_file_basic.txt'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    chunk_size = 2
    expected_chunks = [
        ["line1\n", "line2\n"],
        ["line3\n", "line4\n"],
        ["line5\n"]
    ]
    
    chunks = list(read_file_in_chunks(file_path, chunk_size))
    
    assert chunks == expected_chunks, f"Expected {expected_chunks}, but got {chunks}"
    
    os.remove(file_path)

def test_write_to_temp_file_success():
    """ Test successful creation and writing to a temporary file """
    data = "This is a test data."
    temp_file_path = write_to_temp_file(data)
    
    # Check if the file exists and is not a directory
    assert os.path.isfile(temp_file_path), f"Expected file path, but got {temp_file_path}"
    
    # Verify the file content
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        assert file_content == data, f"Expected content '{data}', but got '{file_content}'"
    
    # Clean up
    os.remove(temp_file_path)

def test_write_to_temp_file_empty_data():
    """ Test writing an empty string to a temporary file """
    data = ""
    temp_file_path = write_to_temp_file(data)
    
    # Check if the file exists and is not a directory
    assert os.path.isfile(temp_file_path), f"Expected file path, but got {temp_file_path}"
    
    # Verify the file content
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        assert file_content == data, f"Expected content '{data}', but got '{file_content}'"
    
    # Clean up
    os.remove(temp_file_path)

def test_write_to_temp_file_error_handling():
    """ Test the behavior of the function when an error occurs """
    # Mock the tempfile.NamedTemporaryFile to raise an error
    with mock.patch('tempfile.NamedTemporaryFile', side_effect=OSError):
        with pytest.raises(OSError):
            write_to_temp_file("Some data")