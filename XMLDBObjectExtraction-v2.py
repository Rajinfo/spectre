import os
import re
import csv
from lxml import etree

# Function to extract SQL from CDATA content within XML
def extract_sql_from_cdata(xml_string):
    # Check for CDATA in the XML string
    cdata_pattern = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
    matches = cdata_pattern.findall(xml_string)
    
    if matches:
        # Return all CDATA content as SQL statements
        return matches
    else:
        # If no CDATA, just return the text content as a fallback
        return [xml_string]

# Enhanced regex patterns from the SQL processing
table_pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z0-9_.]+)\s*(?:AS\s+)?([a-zA-Z0-9_]+)?(?:\s*,\s*([a-zA-Z0-9_.]+)\s*(?:AS\s+)?([a-zA-Z0-9_]+)?)*'
insert_pattern = r'INSERT\s+INTO\s+([a-zA-Z0-9_\.]+)\s*\('
update_pattern = r'UPDATE\s+([a-zA-Z0-9_\.]+)'
delete_pattern = r'DELETE\s+FROM\s+([a-zA-Z0-9_\.]+)'
procedure_pattern = r'CREATE\s+OR\s+REPLACE\s+PROCEDURE\s+([a-zA-Z0-9_]+)\s*\('
function_pattern = r'CREATE\s+OR\s+REPLACE\s+FUNCTION\s+([a-zA-Z0-9_]+)\s*\('
package_pattern = r'CREATE\s+OR\s+REPLACE\s+PACKAGE\s+([a-zA-Z0-9_\.]+)\s+AS'
view_pattern = r'CREATE\s+OR\s+REPLACE\s+VIEW\s+([a-zA-Z0-9_\.]+)\s+AS'
merge_pattern = r'MERGE\s+INTO\s+([a-zA-Z0-9_.]+)'
trigger_pattern = r'CREATE\s+OR\s+REPLACE\s+TRIGGER\s+([a-zA-Z0-9_]+).*?\s+ON\s+([a-zA-Z0-9_]+)'
call_pattern = re.compile(r'\bcall\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
select_key_pattern = re.compile(r'\bselect\s+.*?\s+from\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)

# Function to extract SQL patterns (tables, PLSQL objects) from SQL statements
def extract_objects_from_sql(sql_content, operation_type=None):
    objects_and_operations = []

    # Capture tables from various SQL operations
    for match in re.findall(table_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        primary_table = match[0]
        secondary_table = match[2] if match[2] else None
        objects_and_operations.append((primary_table, 'Table', operation_type or 'select'))
        if secondary_table:
            objects_and_operations.append((secondary_table, 'Table', operation_type or 'select'))

    # Capture INSERT, UPDATE, DELETE
    for match in re.findall(insert_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'insert'))
    for match in re.findall(update_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'update'))
    for match in re.findall(delete_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Table', 'delete'))

    # Capture PLSQL objects (procedures, functions, etc.)
    for match in re.findall(procedure_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'PLSQL', 'create or replace procedure'))
    for match in re.findall(function_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'PLSQL', 'create or replace function'))
    for match in re.findall(package_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'Package', 'create or replace package'))
    for match in re.findall(view_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match, 'View', 'create or replace view'))
    for match in re.findall(trigger_pattern, sql_content, re.IGNORECASE | re.DOTALL):
        objects_and_operations.append((match[0], 'Trigger', 'create or replace trigger'))
        objects_and_operations.append((match[1], 'Table', 'trigger'))

    # Capture CALLABLE statements
    for match in re.findall(call_pattern, sql_content):
        objects_and_operations.append((match, 'PLSQL', 'call'))

    return objects_and_operations

# Function to remove <include> tags from XML
def remove_includes(xml_content):
    include_pattern = re.compile(r'<include.*?>.*?</include>', re.DOTALL)
    return re.sub(include_pattern, '', xml_content)

# Process the XML mapper file to extract tables and PLSQL objects using SQL pattern matching
def process_xml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    # Remove <include> tags before processing
    cleaned_xml_content = remove_includes(xml_content)

    # Convert to bytes to handle encoding declarations
    xml_content_bytes = cleaned_xml_content.encode('utf-8')
    tree = etree.fromstring(xml_content_bytes)

    results = []

    # Process <select>, <insert>, <update>, <delete>, and <selectKey> tags
    for query_tag in tree.xpath('//select | //insert | //update | //delete | //selectKey'):
        sql_statements = extract_sql_from_cdata(etree.tostring(query_tag, encoding='unicode', pretty_print=True))
        if not sql_statements:  # If no CDATA, get the tag's text content directly
            sql_statements = [query_tag.text] if query_tag.text else []

        # Special case for callable statements
        if query_tag.attrib.get('statementType', '').upper() == 'CALLABLE':
            operation_type = 'PLSQL'
        else:
            operation_type = 'Select' if query_tag.tag == 'select' else query_tag.tag

        # Apply SQL pattern matching to each SQL statement found
        for sql in sql_statements:
            objects = extract_objects_from_sql(sql, operation_type)
            results.extend(objects)

    return results

# Function to process folders and extract info from .xml files with SQL patterns included
def process_xml_folders(csv_file, output_csv):
    with open(csv_file, 'r', encoding='utf-8') as file:
        folder_names = [row[0] for row in csv.reader(file)]

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['FolderName', 'FolderPath', 'FilePath', 'FileName', 'ObjectName', 'ObjectType', 'OperationType'])

        for folder in folder_names:
            for root, _, files in os.walk(folder):
                for file_name in files:
                    if file_name.endswith('.xml'):
                        file_path = os.path.join(root, file_name)
                        results = process_xml_file(file_path)
                        if results:
                            for object_name, object_type, operation_type in results:
                                writer.writerow([folder, root, file_path, file_name, object_name, object_type, operation_type])


# Replace with actual CSV paths
csv_input = 'D:/program/test/file-db.csv'
csv_output = 'D:/program/test/out-xml-rep.csv'

process_xml_folders(csv_input, csv_output)
print("XML processing completed. Data saved to", csv_output)
