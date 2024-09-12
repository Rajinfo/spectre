import os
import re
import csv

def read_in_chunks(file_object, chunk_size=1048576):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def extract_objects_from_sql(file_path):
    table_pattern = r'\b(?:FROM|JOIN|INTO|UPDATE|DELETE\s+FROM|MERGE\s+INTO)\s+([a-zA-Z0-9_\.]+)\s*(?:AS\s+)?([a-zA-Z0-9_]+)?'
    procedure_pattern = r'CREATE\s+OR\s+REPLACE\s+PROCEDURE\s+([a-zA-Z0-9_]+)\s*\('
    function_pattern = r'CREATE\s+OR\s+REPLACE\s+FUNCTION\s+([a-zA-Z0-9_]+)\s*\('
    view_pattern = r'CREATE\s+OR\s+REPLACE\s+VIEW\s+([a-zA-Z0-9_]+)'
    materialized_view_pattern = r'CREATE\s+MATERIALIZED\s+VIEW\s+([a-zA-Z0-9_]+)'
    create_pattern = r'CREATE\s+TABLE\s+([a-zA-Z0-9_]+)'
    alter_pattern = r'ALTER\s+TABLE\s+([a-zA-Z0-9_]+)'
    delete_pattern = r'DELETE\s+FROM\s+([a-zA-Z0-9_]+)'
    merge_pattern = r'MERGE\s+INTO\s+([a-zA-Z0-9_.]+)'
    trigger_pattern = r'CREATE\s+(OR\s+REPLACE\s+)?TRIGGER\s+([a-zA-Z0-9_]+)\s+.*?\s+ON\s+([a-zA-Z0-9_]+)'

    objects_and_operations = []
    content = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for chunk in read_in_chunks(file):
            chunk = re.sub(r'--.*', '', chunk)
            chunk = re.sub(r'/\*.*?\*/', '', chunk, flags=re.DOTALL)
            content.append(chunk)

    content = '\n'.join(content)

    for match in re.findall(trigger_pattern, content, re.IGNORECASE | re.DOTALL):
        trigger_name = match[1]
        table_name = match[2]
        objects_and_operations.append((trigger_name, 'Trigger', 'create'))
        objects_and_operations.append((table_name, 'Table', 'trigger'))

    for match in re.findall(table_pattern, content, re.IGNORECASE | re.DOTALL):
        table_name = match[0]
        alias = match[1]
        operation_type = 'default'
        if 'from' in content.lower() or 'join' in content.lower():
            operation_type = 'select'
        elif 'into' in content.lower():
            operation_type = 'insert'
        elif 'update' in content.lower():
            operation_type = 'update'
        elif 'delete from' in content.lower():
            operation_type = 'delete'
        elif 'merge into' in content.lower():
            operation_type = 'merge'

        objects_and_operations.append((table_name, 'Table', operation_type))

    for match in re.findall(create_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'create'))
    for match in re.findall(alter_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'alter'))
    for match in re.findall(delete_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'delete'))

    for match in re.findall(procedure_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'PLSQL', 'create or replace procedure'))
    for match in re.findall(function_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'PLSQL', 'create or replace function'))
    for match in re.findall(view_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'View', 'create or replace view'))
    for match in re.findall(materialized_view_pattern, content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'MaterializedView', 'create'))

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