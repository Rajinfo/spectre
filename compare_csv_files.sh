#!/bin/bash

# Configuration: Define the paths
FROM_PATH="/path/to/source"
TO_PATH="/path/to/destination"
INPUT_FILE="input.csv"
OUTPUT_FILE="output_diff.csv"

# Initialize the output CSV file with headers
echo "Source File,Destination File,Line Count" > "$OUTPUT_FILE"

# Read the input file
while IFS=, read -r file1 file2 file3 condition; do
  if [ "$condition" == "true" ]; then
    # Decompress the gz file
    gunzip -c "$FROM_PATH/$file2" > "$TO_PATH/temp_$file2"

    # Find the differences and count the differing lines
    diff_output=$(diff "$FROM_PATH/$file1" "$TO_PATH/temp_$file2")
    diff_count=$(echo "$diff_output" | wc -l)

    # Capture the result in the output CSV file
    echo "$FROM_PATH/$file1,$FROM_PATH/$file2,$diff_count" >> "$OUTPUT_FILE"

    # Clean up temporary file
    rm "$TO_PATH/temp_$file2"
  fi
done < "$INPUT_FILE"
