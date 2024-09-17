import os
import re
import pandas as pd
import gzip
import shutil

# Function to count SQL statements in a given file
def count_sql_statements(file_path):
    with open(file_path, 'r') as file:
        sql_content = file.read().upper()
    
    counts = {
        'INSERT': len(re.findall(r'\bINSERT\b', sql_content)),
        'UPDATE': len(re.findall(r'\bUPDATE\b', sql_content)),
        'DELETE': len(re.findall(r'\bDELETE\b', sql_content)),
        'CREATE': len(re.findall(r'\bCREATE\b', sql_content)),
        'DROP': len(re.findall(r'\bDROP\b', sql_content))
    }
    
    return counts

# Function to write counts to an Excel file
def write_counts_to_excel(counts, output_file):
    df = pd.DataFrame(counts)
    df.to_csv(output_file, index=False, sep=',')

# Function to extract gzip files
def extract_gzip(file_path, extract_to):
    with gzip.open(file_path, 'rb') as f_in:
        with open(extract_to, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Function to iterate through folders and subfolders
def process_folders(folder_list):
    all_counts = []
    
    for folder in folder_list:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.sql'):
                    counts = count_sql_statements(file_path)
                    counts['File'] = file_path
                    all_counts.append(counts)
                elif file.endswith('.gz'):
                    extracted_file_path = file_path[:-3]  # Remove .gz extension
                    extract_gzip(file_path, extracted_file_path)
                    if extracted_file_path.endswith('.sql'):
                        counts = count_sql_statements(extracted_file_path)
                        counts['File'] = extracted_file_path
                        all_counts.append(counts)
    
    return all_counts

# Main function
def main():
    input_excel_path = 'D:/program/test/file-db.xlsx'  # Replace with your input Excel file path
    output_excel_path = 'D:/program/test/output-statsv1.csv'   # Replace with your desired output file path
    
    # Read folder names from Excel
    folder_df = pd.read_excel(input_excel_path)
    print(f" {output_excel_path}", folder_df)
    folder_list = folder_df['Folder'].tolist()
    
    # Process each folder and its subfolders
    all_counts = process_folders(folder_list)
    
    # Write counts to Excel
    write_counts_to_excel(all_counts, output_excel_path)
    print(f"Counts written to {output_excel_path}")

if __name__ == "__main__":
    main()
