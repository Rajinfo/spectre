#!/bin/bash

# Configuration: Define the paths
FROM_PATH="/path/to/source"
TO_PATH="/path/to/destination"
ANOTHER_SCRIPT="/path/to/another_script.sh"

# Input file
INPUT_FILE="input.csv"

# Dictionary to track backups
declare -A backup_done

# Read the input file
while IFS=, read -r file1 file2 file3 condition number fatest_file; do
  if [ "$condition" == "true" ]; then
    # Copy the files
    cp "$FROM_PATH/$file1" "$TO_PATH/"
    cp "$FROM_PATH/$file2" "$TO_PATH/"
    
    # Check for the condition with number and fatest_file
    if grep -q "${number}|" "$FROM_PATH/$fatest_file"; then
      NEW_FILE="${fatest_file%.org}"
      NEW_FILE_PATH="$TO_PATH/$NEW_FILE"
      
      # Backup existing file if it exists and hasn't been backed up yet
      if [ ! "${backup_done[$NEW_FILE]}" = true ] && [ -f "$NEW_FILE_PATH" ]; then
        TIMESTAMP=$(date +%Y%m%d%H%M%S)
        cp "$NEW_FILE_PATH" "${NEW_FILE_PATH}_backup_$TIMESTAMP"
        backup_done[$NEW_FILE]=true
      fi
      
      # Copy content from fatest_file to NEW_FILE
      if [ ! -f "$NEW_FILE_PATH" ]; then
        grep "${number}|" "$FROM_PATH/$fatest_file" > "$NEW_FILE_PATH"
      else
        grep "${number}|" "$FROM_PATH/$fatest_file" >> "$NEW_FILE_PATH"
      fi
    fi
  fi
done < "$INPUT_FILE"

# Prompt to execute another command
read -p "Do you want to execute another command to run another shell script? (yes/no): " response
if [ "$response" == "yes" ]; then
  bash "$ANOTHER_SCRIPT"
fi
