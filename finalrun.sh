#!/bin/bash

# Configuration: Define the paths
FROM_PATH="/path/to/source"
TO_PATH="/path/to/destination"
ANOTHER_SCRIPT_1="/path/to/another_script1.sh"
ANOTHER_SCRIPT_2="/path/to/another_script2.sh"
ANOTHER_SCRIPT_3="/path/to/another_script3.sh"
ANOTHER_SCRIPT_4="/path/to/another_script4.sh"

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
    if grep -q "^${number}|" "$FROM_PATH/$fatest_file"; then
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
        grep "^${number}|" "$FROM_PATH/$fatest_file" > "$NEW_FILE_PATH"
      else
        grep "^${number}|" "$FROM_PATH/$fatest_file" >> "$NEW_FILE_PATH"
      fi
    fi
  fi
done < "$INPUT_FILE"

# Function to run a script and wait for it to finish
run_script() {
  local script_path=$1
  bash "$script_path" &
  wait $!
}

# Prompt to execute another command
echo "Select an option to run a script:"
echo "1. Run Script 1"
echo "2. Run Script 2"
echo "3. Run Script 3"
echo "4. Run Script 4"
echo "5. Run All Scripts Sequentially"
read -p "Enter your choice (1-5): " response

case $response in
  1)
    run_script "$ANOTHER_SCRIPT_1"
    ;;
  2)
    run_script "$ANOTHER_SCRIPT_2"
    ;;
  3)
    run_script "$ANOTHER_SCRIPT_3"
    ;;
  4)
    run_script "$ANOTHER_SCRIPT_4"
    ;;
  5)
    run_script "$ANOTHER_SCRIPT_1"
    run_script "$ANOTHER_SCRIPT_2"
    run_script "$ANOTHER_SCRIPT_3"
    run_script "$ANOTHER_SCRIPT_4"
    ;;
  *)
    echo "Invalid choice. Exiting."
    ;;
esac
