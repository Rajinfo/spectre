#!/bin/bash

# Database connection details
DB_USER="username"
DB_PASSWORD="password"
DB_HOST="hostname"
DB_PORT="port"
DB_SERVICE="service_name"

# Input and output files
INPUT_FILE="input.csv"
OUTPUT_FILE="output.csv"

# Temporary file to store SQL*Plus output
TEMP_FILE="temp_output.txt"

# Function to check the existence of a DB object
check_db_object() {
    local object_name=$1
    local object_type=$2

    case $object_type in
        table)
            sql_query="SELECT COUNT(*) FROM all_tables WHERE table_name = UPPER('$object_name');"
            ;;
        view)
            sql_query="SELECT COUNT(*) FROM all_views WHERE view_name = UPPER('$object_name');"
            ;;
        trigger)
            sql_query="SELECT COUNT(*) FROM all_triggers WHERE trigger_name = UPPER('$object_name');"
            ;;
        procedure)
            sql_query="SELECT COUNT(*) FROM all_procedures WHERE object_name = UPPER('$object_name') AND object_type = 'PROCEDURE';"
            ;;
        package)
            sql_query="SELECT COUNT(*) FROM all_objects WHERE object_name = UPPER('$object_name') AND object_type = 'PACKAGE';"
            ;;
        sequence)
            sql_query="SELECT COUNT(*) FROM all_sequences WHERE sequence_name = UPPER('$object_name');"
            ;;
        *)
            echo "Invalid Object Type"
            return
            ;;
    esac

    echo "$sql_query" | sqlplus -s "$DB_USER/$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_SERVICE" > $TEMP_FILE
    count=$(grep -o '[0-9]*' $TEMP_FILE)
    
    if [ "$count" -gt 0 ]; then
        echo "Yes"
    else
        echo "No"
    fi
}

# Initialize the output file
echo "RepoName,ObjectName,ObjectType,IsAvailable" > $OUTPUT_FILE

# Read the input CSV file and process each line
tail -n +2 $INPUT_FILE | while IFS=, read -r repo_name object_name object_type
do
    is_available=$(check_db_object "$object_name" "$object_type")
    echo "$repo_name,$object_name,$object_type,$is_available" >> $OUTPUT_FILE
done

# Clean up temporary file
rm -f $TEMP_FILE

echo "Check completed. Results are saved in $OUTPUT_FILE"
