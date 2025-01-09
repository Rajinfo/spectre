import openpyxl
import yaml
import os
import shutil
from datetime import datetime

# Load the Excel file
excel_file = 'configurations.xlsx'
wb = openpyxl.load_workbook(excel_file)
sheet = wb['Configurations']

# Read the first row as headers
headers = [cell.value for cell in sheet[1]]
configurations = {header: None for header in headers}

# Read the configurations from the second row
for i, cell in enumerate(sheet[2]):
    configurations[headers[i]] = cell.value

# Load the YAML template
template_file = 'template.yml'
with open(template_file, 'r') as file:
    yaml_content = yaml.safe_load_all(file)
    yaml_docs = list(yaml_content)

# Update the YAML content with values from the configurations
for doc in yaml_docs:
    if doc['kind'] == 'AppProject':
        doc['metadata']['name'] = configurations['application_namespace']
        doc['spec']['destinations'][0]['namespace'] = configurations['application_namespace']
    elif doc['kind'] == 'Application':
        doc['metadata']['name'] = configurations['repo_name']
        doc['spec']['destination']['namespace'] = configurations['application_namespace']
        doc['source']['repoURL'] = configurations['app_repo_url']
        doc['spec']['source']['targetRevision'] = configurations['targetRevision']
        doc['project'] = configurations['application_namespace']

        # Update the helm valueFiles based on targetRevision
        target_revision = configurations['targetRevision']
        value_files_key = f"valueFiles_{target_revision}"
        if value_files_key in configurations and configurations[value_files_key]:
            value_files = configurations[value_files_key].split(', ')
            doc['spec']['source']['helm']['valueFiles'] = value_files

# Determine the output file path
relative_path = configurations['file_path']
output_file = os.path.join(relative_path, configurations['output_file'])

# Ensure the directory exists
os.makedirs(relative_path, exist_ok=True)

# Check if the output file already exists
if os.path.exists(output_file):
    # Create a backup directory if it doesn't exist
    backup_dir = 'c:/tmp'
    os.makedirs(backup_dir, exist_ok=True)

    # Generate a timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

    # Move the existing file to the backup directory
    backup_file = os.path.join(backup_dir, f"{os.path.basename(output_file).split('.')[0]}_{timestamp}.yml")
    shutil.move(output_file, backup_file)
    print(f"Existing file moved to {backup_file}")

# Save the updated YAML content to the specified output file
with open(output_file, 'w') as file:
    yaml.dump_all(yaml_docs, file)

print(f"Updated YAML file saved as {output_file}")
