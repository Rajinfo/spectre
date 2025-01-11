import openpyxl
import os
import shutil
from datetime import datetime

# Load the Excel file
excel_file = 'configurations.xlsx'
wb = openpyxl.load_workbook(excel_file)
master_sheet = wb['Master Configuration']

# Get headers from the first row of the Master Configuration sheet
headers_master = [cell.value for cell in master_sheet[1]]

# Iterate over each row in the Master Configuration sheet starting from the second row
for row in master_sheet.iter_rows(min_row=2, values_only=True):
    # Create a dictionary with header names as keys and cell values as values
    row_data_master = {headers_master[i]: cell for i, cell in enumerate(row)}

    # Check if the delete_cluem value is TRUE
    if row_data_master.get('delete_cluem') == True:
        # Define paths to move
        directories_to_move = ['test/ioc/', 'test/.ci/']
        file_to_move = 'git.yml'

        # Generate a timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Get the repository name from the row data
        repo_name = row_data_master.get('repo_name', 'default_repo')

        # Define the backup directory path
        backup_dir = os.path.join('c:/tmp', f"{repo_name}_{timestamp}")

        # Ensure the backup directory exists
        os.makedirs(backup_dir, exist_ok=True)

        # Move specified directories
        for directory in directories_to_move:
            if os.path.exists(directory):
                shutil.move(directory, os.path.join(backup_dir, os.path.basename(directory)))
                print(f"Moved directory: {directory} to {backup_dir}")
            else:
                print(f"Directory not found: {directory}")

        # Move specified file
        if os.path.exists(file_to_move):
            shutil.move(file_to_move, os.path.join(backup_dir, os.path.basename(file_to_move)))
            print(f"Moved file: {file_to_move} to {backup_dir}")
        else:
            print(f"File not found: {file_to_move}")

    else:
        print("Skipping row as delete_cluem is not TRUE")
