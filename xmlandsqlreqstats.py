import os
import csv

# Helper function to check if an XML file is MyBatis or iBatis
def is_mybatis_or_ibatis(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        content = file.read()
        if '<!DOCTYPE sqlMap' in content or '<sqlMap' in content:  # iBatis check
            return 'ibatis'
        elif '<mapper' in content:  # MyBatis check
            return 'mybatis'
    return None

# Helper function to check SQL files (custom logic can be added here if needed)
def is_sql_file(sql_file):
    return sql_file.endswith('.sql')

# Function to process folders and extract XML and SQL file counts and names
def process_xml_sql_folders(csv_file, output_csv):
    with open(csv_file, 'r', encoding='utf-8') as file:
        folder_names = [row[0] for row in csv.reader(file)]

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Folder', 'XML Count', 'iBatis Files', 'MyBatis Files', 'SQL Count', 'SQL Files'])

        for folder in folder_names:
            xml_count = 0
            ibatis_files = []
            mybatis_files = []
            sql_count = 0
            sql_files = []

            for root, _, files in os.walk(folder):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    # Process XML files
                    if file_name.endswith('.xml'):
                        result = is_mybatis_or_ibatis(file_path)
                        if result == 'ibatis':
                            ibatis_files.append(file_name)
                            xml_count += 1
                        elif result == 'mybatis':
                            mybatis_files.append(file_name)
                            xml_count += 1
                    # Process SQL files
                    elif is_sql_file(file_name):
                        sql_count += 1
                        sql_files.append(file_name)

            writer.writerow([
                folder,
                xml_count,
                ';'.join(ibatis_files) if ibatis_files else '',
                ';'.join(mybatis_files) if mybatis_files else '',
                sql_count,
                ';'.join(sql_files) if sql_files else ''
            ])

# Replace with actual CSV paths
csv_input = 'D:/program/test/file-db.csv'
csv_output = 'D:/program/test/out-xml-sql.csv'

process_xml_sql_folders(csv_input, csv_output)
print("XML and SQL processing completed. Data saved to", csv_output)
