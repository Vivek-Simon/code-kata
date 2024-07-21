# Data Engineering Coding Challenges

## Judgment Criteria

- Beauty of the code (beauty lies in the eyes of the beholder)
- Testing strategies
- Basic Engineering principles

## Problem 1

### Parse fixed width file

- Generate a fixed width file using the provided spec (offset provided in the spec file represent the length of each field).
- Implement a parser that can parse the fixed width file and generate a delimited file, like CSV for example.
- DO NOT use python libraries like pandas for parsing. You can use the standard library to write out a csv file (If you feel like)
- Language choices (Python or Scala)
- Deliver source via github or bitbucket
- Bonus points if you deliver a docker container (Dockerfile) that can be used to run the code (too lazy to install stuff that you might use)
- Pay attention to encoding

## Problem 2

### Data processing

- Generate a csv file containing first_name, last_name, address, date_of_birth
- Process the csv file to anonymise the data
- Columns to anonymise are first_name, last_name and address
- You might be thinking  that is silly
- Now make this work on 2GB csv file (should be doable on a laptop)
- Demonstrate that the same can work on bigger dataset
- Hint - You would need some distributed computing platform

## Choices

- Any language, any platform
- One of the above problems or both, if you feel like it.

## Solution Overview

The "Parse Fixed Width File" problem has been successfully addressed. Follow the instructions below to run the solution and execute the test cases.

### Running the Solution

1. **Navigate to the Repository Root Directory:**
   Ensure you are in the repository's root directory. This is necessary for the Docker commands to function correctly.

2. **Start the Solution:**
   Use the following command to start the solution:
   ```bash
   docker compose up task
   ```

### Running Tests and Generating Reports

1. **Execute Test Cases:**
   To run the test cases and generate an HTML report, use:
   ```bash
   docker compose up test
   ```
