import cx_Oracle
import pandas as pd

def check_db_objects(input_file, output_file, connection_string):
    # Connect to the Oracle database
    connection = cx_Oracle.connect(connection_string)
    cursor = connection.cursor()

    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Prepare the output DataFrame
    output_df = pd.DataFrame(columns=['RepoName', 'ObjectName', 'ObjectType', 'IsAvailable'])

    # SQL queries to check the existence of different DB objects
    queries = {
        'table': "SELECT COUNT(*) FROM all_tables WHERE table_name = :name",
        'view': "SELECT COUNT(*) FROM all_views WHERE view_name = :name",
        'trigger': "SELECT COUNT(*) FROM all_triggers WHERE trigger_name = :name",
        'procedure': "SELECT COUNT(*) FROM all_procedures WHERE object_name = :name AND object_type = 'PROCEDURE'",
        'package': "SELECT COUNT(*) FROM all_objects WHERE object_name = :name AND object_type = 'PACKAGE'",
        'sequence': "SELECT COUNT(*) FROM all_sequences WHERE sequence_name = :name"
    }

    # Check each DB object
    for index, row in df.iterrows():
        repo_name = row['RepoName']
        name = row['ObjectName'].upper()
        obj_type = row['ObjectType'].lower()
        query = queries.get(obj_type)

        if query:
            cursor.execute(query, name=name)
            count = cursor.fetchone()[0]
            is_available = 'Yes' if count > 0 else 'No'
        else:
            is_available = 'Invalid Object Type'

        output_df = output_df.append({
            'RepoName': repo_name,
            'ObjectName': row['ObjectName'],
            'ObjectType': row['ObjectType'],
            'IsAvailable': is_available
        }, ignore_index=True)

    # Write the output DataFrame to a CSV file
    output_df.to_csv(output_file, index=False)

    # Close the database connection
    cursor.close()
    connection.close()

# Example usage
input_file = 'input.csv'
output_file = 'output.csv'
connection_string = 'username/password@hostname:port/service_name'
check_db_objects(input_file, output_file, connection_string)
