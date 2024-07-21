import string
import os
import logging

# File Encoding while reading and writing
ENCODING="utf-8"
# Splits the data into 100MB files
TEMP_FILE_ROW_LIMIT = 1000000
# Gets the number of logical processors for the machine
NUM_PROCESSES = os.cpu_count()
# 100 MB chucks are easier to read
# based on system specification we can increase or decrease the chunk size
CHUNK_SIZE = 100*1024*1024
# The different characters that will be available when generating data
RANDOM_LETTERS = string.ascii_letters + string.digits + ' '


root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(name)s:%(levelname)s:[file-%(filename)s:line-%(lineno)d]:PID: %(process)d - %(message)s')
