import os
import re
import csv
from lxml import etree

# Enhanced regex patterns for extracting tables and PLSQL objects
def extract_tables_from_sql(sql, operation_type):
    table_pattern = re.compile(r'\bfrom\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
    join_pattern = re.compile(r'\bjoin\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
    insert_pattern = re.compile(r'\binsert\s+into\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
    update_pattern = re.compile(r'\bupdate\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
    delete_pattern = re.compile(r'\bdelete\s+from\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
    call_pattern = re.compile(r'\bcall\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
    select_key_pattern = re.compile(r'\bselect\s+.*?\s+from\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)

    tables = set()
    if operation_type.lower() in ['insert', 'update', 'delete']:
        if operation_type.lower() == 'insert':
            tables.update(insert_pattern.findall(sql))
        elif operation_type.lower() == 'update':
            tables.update(update_pattern.findall(sql))
        elif operation_type.lower() == 'delete':
            tables.update(delete_pattern.findall(sql))
    else:
        tables.update(table_pattern.findall(sql))
        tables.update(join_pattern.findall(sql))
        tables.update(select_key_pattern.findall(sql))
        # Handle call statements separately
        tables.update(call_pattern.findall(sql))

    return tables

# Function to extract SQL from CDATA sections and regular tag text
def extract_sql_from_cdata(xml_fragment):
    cdata_pattern = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
    return cdata_pattern.findall(xml_fragment)

# Function to remove <include> tags from XML
def remove_includes(xml_content):
    include_pattern = re.compile(r'<include.*?>.*?</include>', re.DOTALL)
    return re.sub(include_pattern, '', xml_content)

# Process the XML mapper file to extract tables and PLSQL objects
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

        # Determine the operation type from the tag name
        tag_name = query_tag.tag.lower()
        if tag_name == 'selectkey':
            operation_type = 'selectKey'
        elif tag_name == 'select':
            # Special case for callable statements
            if query_tag.attrib.get('statementType', '').upper() == 'CALLABLE':
                operation_type = 'PLSQL'
            else:
                operation_type = 'Select'
        elif tag_name == 'insert':
            operation_type = 'Insert'
        elif tag_name == 'update':
            operation_type = 'Update'
        elif tag_name == 'delete':
            operation_type = 'Delete'
        else:
            operation_type = 'Unknown'

        # Extract tables from the SQL queries
        for sql in sql_statements:
            tables = extract_tables_from_sql(sql, operation_type)
            if operation_type == 'selectKey':
                for table in tables:
                    results.append((table, 'db', operation_type))
            else:
                for table in tables:
                    results.append((table, 'Table', operation_type))

    return results

# Function to process folders and extract info from .xml files
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
csv_output = 'D:/program/test/out-xml.csv'

process_xml_folders(csv_input, csv_output)
print("XML processing completed. Data saved to", csv_output)