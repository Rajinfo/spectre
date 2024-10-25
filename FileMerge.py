import re
import csv
import shutil
from datetime import datetime
from difflib import unified_diff

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

def normalize_sql(sql_content):
    sql_content = re.sub(r'\s+', ' ', sql_content)
    sql_content = re.sub(r'\s*;\s*', ';', sql_content)
    sql_content = re.sub(r'\s*\(\s*', '(', sql_content)
    sql_content = re.sub(r'\s*\)\s*', ')', sql_content)
    sql_content = re.sub(r'\s*,\s*', ',', sql_content)
    sql_content = re.sub(r'\s*=\s*', '=', sql_content)
    return sql_content.strip()

def reformat_sql(sql_content):
    sql_content = re.sub(r'\s*;\s*', ';\n', sql_content)
    sql_content = re.sub(r'\s*\(\s*', ' (\n', sql_content)
    sql_content = re.sub(r'\s*\)\s*', '\n)', sql_content)
    sql_content = re.sub(r'\s*,\s*', ',\n', sql_content)
    sql_content = re.sub(r'\s*=\s*', ' = ', sql_content)
    return sql_content.strip()

def merge_sql_files(base_sql, new_sql):
    base_sql_normalized = normalize_sql(base_sql)
    new_sql_normalized = normalize_sql(new_sql)

    base_statements = extract_statements(base_sql_normalized)
    new_statements = extract_statements(new_sql_normalized)

    base_statements_set = set(base_statements)
    new_statements_set = set(new_statements)

    added_statements = new_statements_set - base_statements_set

    merged_statements = base_statements_set.union(added_statements)

    merged_sql_normalized = '; '.join(merged_statements) + ';'
    merged_sql = reformat_sql(merged_sql_normalized)

    return merged_sql, added_statements

def extract_statements(sql_content):
    statements = re.split(r';\s*', sql_content)
    return [stmt.strip() for stmt in statements if stmt.strip()]

def generate_diff_report(base_sql, merged_sql, report_file_path):
    base_lines = base_sql.splitlines()
    merged_lines = merged_sql.splitlines()
    diff = unified_diff(base_lines, merged_lines, fromfile='base.sql', tofile='merged.sql')

    with open(report_file_path, 'w') as report_file:
        report_file.write('\n'.join(diff))

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

                backup_sql_file(base_sql_file)

                merged_sql, added_statements = merge_sql_files(base_sql, new_sql)

                write_sql_file(base_sql_file, merged_sql)

                report_file_path = f"{base_sql_file}_changes_report.txt"
                generate_diff_report(base_sql, merged_sql, report_file_path)

                print(f'Merged SQL changes applied to {base_sql_file}')
                print(f'Report generated: {report_file_path}')
            except Exception as e:
                print(f"Error processing files {base_sql_file}, {new_sql_file}: {e}")

if __name__ == '__main__':
    csv_file_path = 'files.csv'
    process_csv(csv_file_path)
