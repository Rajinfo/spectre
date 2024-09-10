#!/bin/bash

# Base directories
BASE_DIRECTORY="/path/to/base_directory"
CSVFILE="$BASE_DIRECTORY/file.csv"
NO_JACOCO_FILE="$BASE_DIRECTORY/projects_no_jacoco.csv"
TEST_RESULTS_FILE="$BASE_DIRECTORY/projects_test_results.csv"

# Clear output files if they already exist
: > "$NO_JACOCO_FILE"
: > "$TEST_RESULTS_FILE"

# Function to extract the project name from URL
get_project_name_from_url() {
    local url="$1"
    # Extract project name from URL
    echo "${url##*/}" | cut -d',' -f1
}

# Function to extract coverage information from HTML file
extract_coverage_info() {
    local html_file="$1"

    # Convert single-line HTML to multiple lines with tags on new lines
    awk 'BEGIN { RS = "" } { gsub(/>[^<]*/,"&\n", $0); gsub(/<\/[^>]*>/, "&\n", $0); print $0 }' "$html_file" |
    sed -n '/<tfoot>/,/<\/tfoot>/p' |
    awk 'NR == 8 { gsub(/<\/td>/, "", $0); print }'
}

# Function to process each build.gradle file found
process_build_gradle() {
    local project_name="$1"
    local project_path="$2"
    local gradle_file_path="$project_path/build.gradle"

    if [ -f "$gradle_file_path" ]; then
        echo "Processing $project_name in $project_path..."

        # Check if build.gradle contains 'jacoco'
        if grep -q 'jacoco' "$gradle_file_path"; then
            echo "'jacoco' found in $gradle_file_path"

            # Attempt to use gradlew first
            local gradlew_path="$project_path/gradlew"
            if [ ! -f "$gradlew_path" ]; then
                echo "gradlew not found in $project_path. Trying with 'gradle' command..."
                local gradle_cmd="gradle"  # Fallback to global 'gradle' command
            else
                local gradle_cmd="$gradlew_path"
            fi

            local gradle_args=("clean" "test" "jacocoTestReport")
            if ! "${gradle_cmd}" "${gradle_args[@]}" -p "$project_path" > "$project_path/gradle_output_test.txt" 2>&1; then
                echo "$project_name;$project_path;Test failed;N/A" >> "$NO_JACOCO_FILE"
                cat "$project_path/gradle_output_test.txt" >> "$NO_JACOCO_FILE"
                return
            fi

            # If tests pass, extract coverage information
            echo "Tests passed for $project_name. Extracting coverage..."
            local coverage_file="$project_path/build/reports/jacoco/test/html/index.html"
            if [ -f "$coverage_file" ]; then
                local total_coverage
                total_coverage=$(extract_coverage_info "$coverage_file")
                if [ -n "$total_coverage" ]; then
                    echo "$project_name;$project_path;Test passed;$total_coverage" >> "$TEST_RESULTS_FILE"
                else
                    echo "$project_name;$project_path;Test passed;Coverage Not Found" >> "$TEST_RESULTS_FILE"
                fi
            else
                echo "$project_name;$project_path;Test passed;Coverage File Not Found" >> "$TEST_RESULTS_FILE"
            fi
        else
            echo "'jacoco' not found in $gradle_file_path. Skipping..."
            echo "$project_name;$project_path;no JaCoCo" >> "$NO_JACOCO_FILE"
        fi
    fi
}

# Main logic to loop through each project
while IFS=',' read -r url _; do
    project_name=$(get_project_name_from_url "$url")
    project_dir="$BASE_DIRECTORY/$project_name"

    if [ -d "$project_dir" ]; then
        # Search for build.gradle in the main directory and all subdirectories
        find "$project_dir" -type f -name "build.gradle" | while read -r gradle_file; do
            project_path=$(dirname "$gradle_file")
            process_build_gradle "$project_name" "$project_path"
        done
    else
        echo "Directory $project_dir does not exist. Skipping..."
        echo "$project_name;$project_dir;Directory $project_dir does not exist" >> "$NO_JACOCO_FILE"
    fi
done < "$CSVFILE"

echo "JaCoCo check and test execution completed."
echo "Results saved to $NO_JACOCO_FILE and $TEST_RESULTS_FILE."
