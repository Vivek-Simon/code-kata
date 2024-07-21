import time
import argparse
import logging
import constants as C
from spec_file import read_spec_file
from multi_processing import multi_processing
from data_generator import generate_fixed_width_file
from file_processing import (
                                        create_output_file,
                                        write_csv_to_temp_file,
                                        read_file_in_chunks
                                    )
        
def get_fixed_width_file(row_count,output_file_name,spec_data,process_count=C.NUM_PROCESSES,max_chunk_row_count=C.TEMP_FILE_ROW_LIMIT):
    """
    Orchestrates generating fixed width data and writes to a file

    :param row_count:           Total rows of data needed
    :param output_file_name:    Name for the output file
    :param spec_data:           function generates the file based on the spec supplied
    :param process_count:       Max number of processes that can be used during multi processing
    :param max_chunk_row_count: To avoid memory limits we restrict maximum rows that can be read at a time.
    """
    data = list(range(row_count))
    function_args=(spec_data)
    start_time = time.time()
    logging.info("Generating data for fixed width file")
    chunk_size = len(data) if len(data)<max_chunk_row_count else max_chunk_row_count
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    logging.debug(f"Chunk size: {chunk_size}")
    logging.debug(f"Number of chunks created: {len(chunks)}")

    temp_file_name = multi_processing(generate_fixed_width_file, function_args, process_count, chunks)
    duration = time.time() - start_time
    logging.debug(f"Execution time with {process_count} processes: {duration:.2f} seconds")
    create_output_file(temp_file_name, output_file_name)
    logging.info(f"Fixed width file '{output_file_name}' has been generated.")

def fixed_width_file_parser(chunk,spec_data):
    """
    Fixed width file parser function, parses the data based on the spec supplied.

    :param chunk:       Data to be parsed
    :param spec_data:   Parser uses this spec to correctly parse the data
    :return:            Path to the temporary file
    """
    widths = list(spec_data["offset"].values())
    dataset = []
    for line in chunk:
        line = line.rstrip('\n')
        start_index = 0
        segments = []
        for width in widths:
            segments.append(line[start_index:start_index+width].strip())
            start_index = start_index+width
        dataset.append(segments)
    return write_csv_to_temp_file(dataset)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate and process fixed-width files.")
    parser.add_argument('--spec_file', type=str, default="spec.json", help='Path to the json specification file')
    parser.add_argument('--output_file_name_txt', type=str, default="output/output.txt", help='Path for the generated text file')
    parser.add_argument('--output_file_name_csv', type=str, default="output/output.csv", help='Path for the final CSV output file')
    parser.add_argument('--row_count', type=int, default=100000, help='Number of rows to generate')
    
    args = parser.parse_args()
    

    # Read the specification file
    spec_data = read_spec_file(args.spec_file)

    # Generate the fixed-width file
    get_fixed_width_file(args.row_count, args.output_file_name_txt, spec_data)

    # Set up arguments for multiprocessing
    function_args = (spec_data)
    temp_file_names = multi_processing(
        fixed_width_file_parser,
        function_args,
        C.NUM_PROCESSES,
        read_file_in_chunks(args.output_file_name_txt)
    )

    # Create the final output CSV file
    create_output_file(temp_file_names, args.output_file_name_csv, headers=list(spec_data['offset'].keys()))


# # 100000 rows is ~ 11MB
# # 1000000 rows is ~ 100MB
# # 40000000 rows is 3.72 GB
if __name__ == '__main__':
    main()