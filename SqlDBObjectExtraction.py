import os
import re
import csv

def read_in_chunks(file_object, chunk_size=1048576):  # 1 MB chunk size
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def remove_into_clauses(content):
    # Pattern to find 'INTO' in SELECT statements and remove them
    into_pattern = r'SELECT\s+.*?\s+INTO\s+.*?(?=FROM|$)'  # Matches SELECT ... INTO ... FROM
    content = re.sub(into_pattern, lambda m: m.group(0).split('INTO')[0].strip(), content, flags=re.IGNORECASE)
    return content

def extract_objects_from_sql(file_path):
    # Patterns to capture table names for different SQL operations
    table_pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z0-9_\.]+)\s*(?:AS\s+)?([a-zA-Z0-9_]+)?(?:\s*,\s*([a-zA-Z0-9_\.]+))*'
    insert_pattern = r'INSERT\s+INTO\s+([a-zA-Z0-9_\.]+)\s*\('
    update_pattern = r'UPDATE\s+([a-zA-Z0-9_\.]+)'

    procedure_pattern = r'CREATE\s+OR\s+REPLACE\s+PROCEDURE\s+([a-zA-Z0-9_]+)\s*\('
    function_pattern = r'CREATE\s+OR\s+REPLACE\s+FUNCTION\s+([a-zA-Z0-9_]+)\s*\('
    view_pattern = r'CREATE\s+OR\s+REPLACE\s+(?:FORCE\s+)?VIEW\s+([a-zA-Z0-9_\.]+)'
    materialized_view_pattern = r'CREATE\s+MATERIALIZED\s+VIEW\s+([a-zA-Z0-9_]+)'
    create_pattern = r'CREATE\s+TABLE\s+([a-zA-Z0-9_]+)'
    alter_pattern = r'ALTER\s+TABLE\s+([a-zA-Z0-9_]+)'
    delete_pattern = r'DELETE\s+FROM\s+([a-zA-Z0-9_]+)'
    merge_pattern = r'MERGE\s+INTO\s+([a-zA-Z0-9_.]+)'

    # Updated trigger pattern to capture both trigger name and table name after ON clause
    trigger_pattern = r'CREATE\s+OR\s+REPLACE\s+TRIGGER\s+([a-zA-Z0-9_]+).*?\s+ON\s+([a-zA-Z0-9_]+)'
    drop_procedure_pattern = r'DROP\s+PROCEDURE\s+([a-zA-Z0-9_]+)'
    drop_trigger_pattern = r'DROP\s+TRIGGER\s+([a-zA-Z0-9_]+)'
    drop_view_pattern = r'DROP\s+VIEW\s+([a-zA-Z0-9_\.]+)'

    objects_and_operations = []
    content = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for chunk in read_in_chunks(file):
            chunk = re.sub(r'--.*', '', chunk)  # Remove comments
            chunk = re.sub(r'/\*.*?\*/', '', chunk, flags=re.DOTALL)  # Remove multi-line comments
            content.append(chunk)

    content = '\n'.join(content)
    content = remove_into_clauses(content)  # Remove INTO clauses before processing

    # Capture tables with or without aliases and handle comma-separated tables
    for match in re.findall(table_pattern, content, re.IGNORECASE | re.DOTALL):
        primary_table = match[0]  # First table
        alias = match[1] if match[1] else ''  # Alias for first table (optional)
        secondary_table = match[2] if match[2] else None  # Additional table after a comma

        objects_and_operations.append((primary_table, 'Table', 'select'))  # Operation type defaulted to 'select'
        if secondary_table:
            objects_and_operations.append((secondary_table, 'Table', 'select'))

    # Capture INSERT INTO statements
    for match in re.findall(insert_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'insert'))

    # Capture UPDATE statements
    for match in re.findall(update_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'update'))

    # Capture DDL and DML operations
    for match in re.findall(create_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'create'))
    for match in re.findall(alter_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'alter'))
    for match in re.findall(delete_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'delete'))

    # Capture PLSQL objects
    for match in re.findall(procedure_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'PLSQL', 'create or replace procedure'))
    for match in re.findall(function_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'PLSQL', 'create or replace function'))

    # Capture views
    for match in re.findall(view_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'View', 'create or replace view'))
    for match in re.findall(materialized_view_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'MaterializedView', 'create'))

    # Capture triggers and the table they affect
    for match in re.findall(trigger_pattern, content, re.IGNORECASE | re.DOTALL):
        trigger_name = match[0]
        table_name = match[1]
        objects_and_operations.append((trigger_name, 'Trigger', 'create or replace trigger'))
        objects_and_operations.append((table_name, 'Table', 'trigger'))

    # Capture DROP operations
    for match in re.findall(drop_procedure_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'PLSQL', 'drop procedure'))
    for match in re.findall(drop_trigger_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Trigger', 'drop trigger'))
    for match in re.findall(drop_view_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'View', 'drop view'))

    return objects_and_operations

def process_sql_folders(csv_file, output_csv):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        folder_names = [row[0] for row in reader]

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['FolderName', 'FolderPath', 'FilePath', 'FileName', 'ObjectName', 'ObjectType', 'OperationType'])

        for folder in folder_names:
            for root, _, files in os.walk(folder):
                for file_name in files:
                    if file_name.endswith('.sql'):
                        file_path = os.path.join(root, file_name)
                        objects_and_operations = extract_objects_from_sql(file_path)
                        if objects_and_operations:
                            for object_name, object_type, operation_type in objects_and_operations:
                                writer.writerow([folder, root, file_path, file_name, object_name, object_type, operation_type])

csv_input = 'D:/program/test/file-db.csv'
csv_output = 'D:/program/test/out-sql.csv'
process_sql_folders(csv_input, csv_output)
print("SQL processing completed. Data saved to", csv_output)
