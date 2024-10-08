#!/bin/bash

# Define the base SQL query with placeholders
base_query="SELECT COUNT(*), '?' FROM ? WHERE id=?;"

# Read the input CSV file and replace placeholders
queries=""
while IFS=, read -r col1 col2 col3
do
  query=${base_query//\?/$col1}
  query=${query//\?/$col2}
  query=${query//\?/$col3}
  queries="${queries}${query}\n"
done < input.csv

# Save the combined queries into a .sql file
echo -e "$queries" > query.sql

# Connect to SQL*Plus and execute the .sql file, saving the output to a temporary file
sqlplus -s username/password@database @query.sql > output_raw.txt

# Format the output file
awk '
BEGIN {
    print "TOTREC,SCRIPT"
}
{
    if ($1 ~ /^[0-9]+$/) {
        gsub(/^[ \t]+|[ \t]+$/, "", $0)  # Trim leading/trailing spaces
        print $1 "," $2
    }
}
' output_raw.txt > formatted_output.csv

# Clean up temporary files
rm query.sql output_raw.txt

echo "Formatted output saved to formatted_output.csv"
