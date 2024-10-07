#!/bin/bash

# Configuration: Define the paths
FROM_PATH="/path/to/source"
TO_PATH="/path/to/destination"
ANOTHER_SCRIPT_1="/path/to/another_script1.sh 0 >> out.txt"
ANOTHER_SCRIPT_2="/path/to/another_script2.sh"
ANOTHER_SCRIPT_3="/path/to/another_script3.sh"
ANOTHER_SCRIPT_4="/path/to/another_script4.sh"

# Database configuration
DB_USER="your_db_user"
DB_PASS="your_db_password"
DB_HOST="your_db_host"
DB_SID="your_db_sid"

# Input file
INPUT_FILE="input.csv"

# Dictionary to track backups
declare -A backup_done

# Function to execute SQL query and return output
execute_sql_query() {
  local query=$1
  sqlplus -s "$DB_USER/$DB_PASS@$DB_HOST/$DB_SID" <<EOF
SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
$query;
EXIT;
EOF
}

# Function to execute multiple SQL queries and save combined output to a single CSV
run_combined_sql_queries() {
  local queries=$1
  local output_file=$2
  echo "Executing combined SQL queries and saving output to $output_file"
  sqlplus -s "$DB_USER/$DB_PASS@$DB_HOST/$DB_SID" <<EOF
SET PAGESIZE 50000
SET LINESIZE 32767
SET FEEDBACK OFF
SET ECHO OFF
SET COLSEP ","
SPOOL $output_file
$queries
SPOOL OFF
EXIT
EOF
}

# Function to capture the script
capture_script() {
  local first_query=$1
  echo "Saving the script: $first_query"
  combined_queries+="$first_query;"
}

# Initialize combined_queries variable
combined_queries=""

# Read the input file
while IFS=, read -r file1 file2 file3 condition number fatest_file first_query; do
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

    # Capture the first query
    capture_script "$first_query"

  fi
done < "$INPUT_FILE"

# Run the combined queries and save the output to a single file
output_file="combined_output.csv"
run_combined_sql_queries "$combined_queries" "$output_file"

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
    eval "$ANOTHER_SCRIPT_1"
    ;;
  2)
    eval "$ANOTHER_SCRIPT_2"
    ;;
  3)
    eval "$ANOTHER_SCRIPT_3"
    ;;
  4)
    eval "$ANOTHER_SCRIPT_4"
    ;;
  5)
    eval "$ANOTHER_SCRIPT_1"
    eval "$ANOTHER_SCRIPT_2"
    eval "$ANOTHER_SCRIPT_3"
    eval "$ANOTHER_SCRIPT_4"
    ;;
  *)
    echo "Invalid choice. Exiting."
    ;;
esac
