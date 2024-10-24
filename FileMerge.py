import re
import csv
import shutil
from datetime import datetime

def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_sql_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def backup_sql_file(file_path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file_path = f"{file_path}.org.{timestamp}"
    shutil.copy(file_path, backup_file_path)
    print(f"Backup created: {backup_file_path}")

def extract_statements(sql_content):
    # This regex assumes that each statement ends with a semicolon
    statements = re.split(r';\s*', sql_content)
    return [stmt.strip() for stmt in statements if stmt.strip()]

def merge_sql_files(base_sql, new_sql):
    base_statements = extract_statements(base_sql)
    new_statements = extract_statements(new_sql)
    
    base_statements_set = set(base_statements)
    new_statements_set = set(new_statements)
    
    # Find statements that are in new_sql but not in base_sql
    added_statements = new_statements_set - base_statements_set
    # Find statements that are in base_sql but not in new_sql
    removed_statements = base_statements_set - new_statements_set
    
    # Merge changes
    merged_statements = base_statements_set.union(added_statements) - removed_statements
    
    return ';\n'.join(merged_statements) + ';'

def process_csv(csv_file_path):
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue
            
            base_sql_file, new_sql_file = row
            try:
                base_sql = read_sql_file(base_sql_file)
                new_sql = read_sql_file(new_sql_file)
                
                # Backup the base SQL file
                backup_sql_file(base_sql_file)
                
                merged_sql = merge_sql_files(base_sql, new_sql)
                
                # Write the merged content back to the base SQL file
                write_sql_file(base_sql_file, merged_sql)
                print(f'Merged SQL changes applied to {base_sql_file}')
            except Exception as e:
                print(f"Error processing files {base_sql_file}, {new_sql_file}: {e}")

if __name__ == '__main__':
    csv_file_path = 'files.csv'
    process_csv(csv_file_path)
