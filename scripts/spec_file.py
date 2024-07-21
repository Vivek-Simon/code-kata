import json
import logging
import constants as C
from retry_mechanism import retry

@retry()
def read_spec_file(spec_file):
    """Reads the specification file and returns a list of field lengths.
    
    :param spec_file:   location of the spec file
    :returns:           data ingested from spec file
    """
    with open(spec_file, 'r', encoding=C.ENCODING) as file:
        logging.debug("Reading data from spec file.")
        spec_file_data = json.load(file)
        logging.debug("Reading data from spec file completed.")
    return spec_file_data