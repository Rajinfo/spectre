import os
import re
import csv

def find_files(directory, extensions):
    """Find files with given extensions in the specified directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                yield os.path.join(root, file)

def extract_with_as(content):
    """Extract single word between WITH and AS."""
    pattern = re.compile(r'WITH\s+(\w+)\s+AS', re.IGNORECASE)
    matches = pattern.findall(content)
    return matches

def extract_key_value(content):
    """Extract the word between KEY and VALUE, removing hyphens."""
    pattern = re.compile(r'KEY\s+\'?(\w+?)\'?\s+VALUE', re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(content)
    return [match.replace('-', '') for match in matches]

def main(directory, output_csv):
    extensions = ['.sql', '.xml']
    data = []

    for file_path in find_files(directory, extensions):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            with_as_matches = extract_with_as(content)
            key_value_matches = extract_key_value(content)

            if with_as_matches:
                for match in with_as_matches:
                    data.append([file_path, 'WITH-AS', match.strip()])

            if key_value_matches:
                for match in key_value_matches:
                    data.append([file_path, 'KEY-VALUE', match.strip()])

    # Write data to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Path', 'Type', 'Extracted Text'])
        csvwriter.writerows(data)

    print(f"Data saved to {output_csv}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    output_csv = input("Enter the output CSV file path: ")
    main(directory, output_csv)
