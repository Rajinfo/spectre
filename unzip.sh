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
    diff "test${DYNAMIC_PART}test.csv" "test${DYNAMIC_PART}test.yester.csv" > report.txt

    echo "Difference saved in report.txt"

else
    echo "One or both of the required files are missing."
fi
