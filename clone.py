# Python
import pandas as pd
import git
import os
from urllib.parse import urlparse

# Load the Excel file
excel_file = 'path_to_your_excel_file.xlsx'
df = pd.read_excel(excel_file)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    repo_url = row['Repo URL']
    branch_name = row['Branch Name']
    backup_branch_name = row['Backup Branch Name']

    # Parse the repo name from the URL
    parsed_url = urlparse(repo_url)
    repo_name = os.path.basename(parsed_url.path).replace('.git', '')

    # Use the repo name as the directory
    repo_dir = repo_name
    if not os.path.exists(repo_dir):
        repo = git.Repo.clone_from(repo_url, repo_dir)
    else:
        repo = git.Repo(repo_dir)

    # Checkout to the specified branch
    repo.git.checkout(branch_name)

    # Create a backup branch
    repo.git.checkout('-b', backup_branch_name)

    # Push the backup branch to the remote repository
    repo.git.push('origin', backup_branch_name)

    print(f'Repo {repo_url} processed: switched to {branch_name} and backup branch {backup_branch_name} created and pushed.')
pip install pandas gitpython openpyxl
