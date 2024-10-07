#!/bin/bash

# Read File 1 into an associative array
declare -A file1_data
while IFS=, read -r id value; do
    file1_data[$id]=$value
done < file1.csv

# Read File 2 into an associative array
declare -A file2_data
while IFS=, read -r id value; do
    file2_data[$id]=$value
done < file2.csv

# Combine data and write to combined.csv
{
    echo "Identifier,File1_Value,File2_Value,Match_Status"
    for id in "${!file1_data[@]}" "${!file2_data[@]}"; do
        if [[ -n "${file1_data[$id]}" ]] [[ -n "${file2_data[$id]}" ]]; then
            value1=${file1_data[$id]:-N/A}
            value2=${file2_data[$id]:-N/A}
            if [[ "$value1" == "$value2" ]]; then
                match_status="Matching"
            else
                match_status="Not Matching"
            fi
            echo "$id,$value1,$value2,$match_status"
        fi
    done | sort -t, -k1,1
} > combined.csv

echo "Combined CSV file has been created successfully."
