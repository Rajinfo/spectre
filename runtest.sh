#!/bin/bash

# Configuration: Define the paths
FROM_PATH="/path/to/source"
TO_PATH="/path/to/destination"
BTO_PATH="/path/to/destination"
ANOTHER_SCRIPT="/path/to/another_script.sh"

# Input file
INPUT_FILE="input.csv"

# Read the input file
while IFS=, read -r file1 file2 file3 condition; do
  if [ "$condition" == "true" ]; then
    # Copy the files
    cp "$FROM_PATH/$file1" "$TO_PATH/"
    cp "$FROM_PATH/$file2" "$BTO_PATH/"
  fi
done < "$INPUT_FILE"

# Prompt to execute another command
read -p "Do you want to execute another command to run another shell script? (yes/no): " response
if [ "$response" == "yes" ]; then
  bash "$ANOTHER_SCRIPT"
fi
