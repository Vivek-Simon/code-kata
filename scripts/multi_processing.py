import logging
import constants as C
import multiprocessing


def multi_processing(function, function_args, process_count, chunks):
    """
    Perform multi-processing on the given data using the specified worker function.

    :param function:        Worker function reference
    :param function_args:   Arguments that need to be passed to the worker function
    :param process_count:   Number of processes that need to run in parallel
    :param chunks:          Data to be processed
    :return:                List of results from the worker function
    """
    
    logging.debug(f"Function arguments: {function_args}")

    with multiprocessing.Pool(process_count) as pool:
        logging.info(f"Starting {process_count} processes for function {function.__name__}")
        results = pool.starmap(function, [(chunk, function_args) for chunk in chunks])
    
    logging.info(f"All the processes completed execution for {function.__name__}")
    return results