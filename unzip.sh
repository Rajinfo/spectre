#!/bin/bash

# Read the dynamic part from the CSV file
CSV_FILE="yourfile.csv"
DYNAMIC_PART=$(awk -F '|' '{print $1}' $CSV_FILE) # Assuming the dynamic part is in the first column

# Set date formats for today and yesterday
TODAY=$(date +%Y%m%d)
YESTERDAY=$(date -d "yesterday" +%Y%m%d)

# Define file names based on today and yesterday's dates and the dynamic part
TODAY_FILE="test${DYNAMIC_PART}test.${TODAY}.gz"
YESTERDAY_FILE="test${DYNAMIC_PART}test.${YESTERDAY}.gz"

# Define output CSV file and report file name
OUTPUT_CSV="output.csv"
REPORT_FILE="report_${DYNAMIC_PART}_${TODAY}.txt"

# Check if both today and yesterday's .gz files exist
if [[ -f "$TODAY_FILE" && -f "$YESTERDAY_FILE" ]]; then
    echo "Both today and yesterday's files found."

    # Unzip the files
    gunzip -k "$TODAY_FILE"
    gunzip -k "$YESTERDAY_FILE"

    # Define the CSV filenames after unzipping
    TODAY_CSV="test${DYNAMIC_PART}test.${TODAY}.csv"
    YESTERDAY_CSV="test${DYNAMIC_PART}test.${YESTERDAY}.csv"

    # Copy today file to test123test.csv and yesterday file to test123test.yester.csv
    cp "$TODAY_CSV" "test${DYNAMIC_PART}test.csv"
    cp "$YESTERDAY_CSV" "test${DYNAMIC_PART}test.yester.csv"

    # Find the difference between today's and yesterday's files
    diff "test${DYNAMIC_PART}test.csv" "test${DYNAMIC_PART}test.yester.csv" > "$REPORT_FILE"

    echo "Difference saved in $REPORT_FILE"
else
    echo "One or both of the required files are missing."
fi

# Extract lines from summaryfile where the first field matches any number in summaryinputfile and save to output.csv
SUMMARY_FILE="summaryfile"
SUMMARY_INPUT_FILE="summaryinputfile"

if [[ -f "$SUMMARY_FILE" && -f "$SUMMARY_INPUT_FILE" ]]; then
    echo "Processing summaryfile and summaryinputfile"

    # Extract matching lines and save them to output.csv
    grep -F -f "$SUMMARY_INPUT_FILE" "$SUMMARY_FILE" > "$OUTPUT_CSV"
    echo "Filtered summary data saved in $OUTPUT_CSV"

else
    echo "Either summaryfile or summaryinputfile is missing."
    exit 1
fi

# Execute the testrun.sh script
if [[ -f "testrun.sh" ]]; then
    echo "Executing testrun.sh..."
    bash testrun.sh
else
    echo "testrun.sh script not found."
    exit 1
fi

# Query SQLPlus for specific IDs from summaryinputfile and append count results to output.csv
SQL_QUERY_IDS=$(awk '{print $1}' "$SUMMARY_INPUT_FILE" | paste -sd ',' -) # Converts IDs to "200,300" format

if [[ ! -z "$SQL_QUERY_IDS" ]]; then
    echo "Querying SQLPlus for IDs: $SQL_QUERY_IDS"

    # Assuming you have SQLPlus configured and can use it directly.
    # Replace YOUR_DB_USERNAME, YOUR_DB_PASSWORD, and YOUR_DB_SID with actual values
    SQL_QUERY="SELECT id, COUNT(*) FROM your_table WHERE id IN (${SQL_QUERY_IDS}) GROUP BY id;"

    sqlplus -s YOUR_DB_USERNAME/YOUR_DB_PASSWORD@YOUR_DB_SID <<EOF | while read -r LINE
SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
$SQL_QUERY
EXIT;
EOF
do
    # Append SQL result to the output.csv file
    echo "$LINE" >> "$OUTPUT_CSV"
done

    echo "SQL query result appended to $OUTPUT_CSV"
else
    echo "No IDs found in summaryinputfile for SQL query."
fi
