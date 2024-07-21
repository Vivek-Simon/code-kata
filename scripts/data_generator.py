import random
import constants as C
import logging
from retry_mechanism import retry
from file_processing import write_to_temp_file

@retry()
def generate_random_string(length):
    """ 
    Generates a random string of a specified length. 
    
    :param: length: Length of the generated string
    :return:        Return a string of specific length
    """
    logging.debug(f'Generating random numbers for length {length}.')
    return ''.join(random.choices(C.RANDOM_LETTERS, k=length))


@retry()
def generate_fixed_width_file(data_to_process, spec_data):
    """ 
    Generates a fixed width file based on the given data and field lengths.
    
    :param: data_to_process:    A list of values supplied, this data is dummy. 
                                This is used to determine the dimension of the dataset during multi processing
    :param: spec_data:          Data generated based on the spec supplied here
    :return:                    Temporary file path
    """
    logging.debug('Starting to generate fixed width file.')
    rows = []

    try:
        for _ in data_to_process:
            row_processed = ''.join(generate_random_string(col_spec) for col_spec in spec_data["offset"].values())
            rows.append(row_processed)
        data = '\n'.join(rows) + '\n'  
    except Exception as e:
        logging.error(f'Error processing data: {e}')
        raise e
    logging.debug('Finished generating fixed width file.')
    return write_to_temp_file(data)
