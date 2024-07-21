import csv
import tempfile
import os
import logging
import itertools
import constants as C
from retry_mechanism import retry

def write_csv_to_temp_file(data):
    """
    Write a list of lists to a temporary CSV file.

    :param data:    List of lists where each inner list represents a row
    :return:        Path to the temporary file
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8') as temp_file:
        # Create a CSV writer object
        writer = csv.writer(temp_file)
        
        # Write all rows to the temporary file
        writer.writerows(data)
        
        # Return the path to the temporary file
        return temp_file.name
    
def create_output_file(file_names, output_file_name, max_bytes=C.CHUNK_SIZE, headers=None):
    """
    Creates an output file after fixed width data is generated to be consumed by parser

    :param file_names:          List of temporary file names  where data is stored.
    :param output_file_name:    Name for the output file
    :param max_bytes:           To avoid memory limits we restrict maximum bytes that can be read at a time.
    :param headers:             Column headers for the file
    """
    # Creates final output file from temp files
    logging.info(f'Creating output file {output_file_name}.')
    with open(output_file_name, 'w', encoding=C.ENCODING) as output_file:
        if headers:
            header_line = ','.join(headers) + '\n'
            output_file.write(header_line)

        for file_name in file_names:
            # The function does not crash even if the temp file is large in size
            with open(file_name, 'r', encoding=C.ENCODING) as temp_file:
                while True:
                    chunk = temp_file.read(max_bytes)
                    if not chunk:
                        break
                    output_file.write(chunk)
            # removing the temporary file
            os.remove(file_name)

def read_file_in_chunks(file_path, chunk_size_per_process=C.TEMP_FILE_ROW_LIMIT):
    """
    Read a large text file in chunks using itertools.islice.
    
    :param file_path:   Path to the text file
    :param chunk_size:  Number of lines per chunk
    :return:            Generator yielding chunks of lines
    """
    with open(file_path, 'r', encoding=C.ENCODING) as file:
        while True:
            logging.debug(f'Reading {chunk_size_per_process} lines of data from {file_path} file.')
            lines = list(itertools.islice(file, chunk_size_per_process))
            if not lines:
                break
            yield lines

@retry()
def write_to_temp_file(data):
    """ 
    Writes data to a temporary file 
    
    :param: data:   Data to be written
    :return:        Temporary file path
    """
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
        temp_file.write(data)
        temp_file.close()
        return temp_file.name
    except Exception as e:
        logging.error(f'Error writing to temporary file: {e}')
        raise e