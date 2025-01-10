import openpyxl
import os
import shutil
from datetime import datetime

# Load the Excel file
excel_file = 'configurations.xlsx'
wb = openpyxl.load_workbook(excel_file)
sheet = wb['Sheet1']

# Load the Dockerfile template from a file
with open('dockerfile_template', 'r') as template_file:
    dockerfile_template = template_file.read()

# Get headers from the first row
headers = [cell.value for cell in sheet[1]]

# Iterate over each row in the sheet starting from the second row
for row in sheet.iter_rows(min_row=2, values_only=True):
    # Create a dictionary with header names as keys and cell values as values
    row_data = {headers[i]: cell for i, cell in enumerate(row)}

    # Replace placeholders in the Dockerfile template with actual values
    dockerfile_content = dockerfile_template
    for key, value in row_data.items():
        placeholder = f"<{key}>"
        dockerfile_content = dockerfile_content.replace(placeholder, str(value) if value is not None else "")

    # Get the file path and repo name from the current row
    dockerfile_path = row_data.get('dockerfilepath')
    repo_name = row_data.get('repo_name')  # Ensure this column exists in your Excel sheet

    # Ensure the directory exists
    if dockerfile_path:
        # Check if the Dockerfile already exists
        if os.path.exists(dockerfile_path):
            # Create a timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Define the new directory path
            new_dir = f"c:/tmp/{repo_name}{timestamp}"
            os.makedirs(new_dir, exist_ok=True)
            # Move the existing Dockerfile to the new directory
            shutil.move(dockerfile_path, os.path.join(new_dir, os.path.basename(dockerfile_path)))
            print(f"Existing Dockerfile moved to {new_dir}")

        # Write the updated Dockerfile content to the specified path
        os.makedirs(os.path.dirname(dockerfile_path), exist_ok=True)
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_content)

        print(f"Updated Dockerfile saved at {dockerfile_path}")
