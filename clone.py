# Python
import pandas as pd
import git
import os
from urllib.parse import urlparse

# Load the Excel file
excel_file = 'path_to_your_excel_file.xlsx'
df = pd.read_excel(excel_file)

# Prepare a list to store the results
results = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    repo_url = row['Repo URL']
    branch_name = row['Branch Name']
    backup_branch_name = row['Backup Branch Name']
    tpc_branch_name = row['TPC Branch']
    isbranch_backup = row['isbranch_backup']

    # Parse the repo name from the URL
    parsed_url = urlparse(repo_url)
    repo_name = os.path.basename(parsed_url.path).replace('.git', '')

    # Use the repo name as the directory
    repo_dir = repo_name
    try:
        if not os.path.exists(repo_dir):
            repo = git.Repo.clone_from(repo_url, repo_dir)
        else:
            repo = git.Repo(repo_dir)

        # Fetch all branches to ensure we have the latest references
        repo.remotes.origin.fetch()

        backup_success = False
        if isbranch_backup:
            # Create a backup branch from the remote branch
            repo.git.branch(backup_branch_name, f'origin/{branch_name}')
            
            # Push the backup branch to the remote repository
            repo.git.push('origin', backup_branch_name)
            backup_success = True

        # Switch to the specified tpc-branch
        repo.git.checkout(tpc_branch_name)
        switch_success = True

    except Exception as e:
        switch_success = False
        backup_success = False
        print(f"Error processing repo {repo_url}: {e}")

    # Append the result for this repo
    results.append({
        'Repo URL': repo_url,
        'Switch to TPC Branch Success': switch_success,
        'Backup Branch Success': backup_success
    })

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_csv = 'git_operations_report.csv'
results_df.to_csv(results_csv, index=False)

print(f'Report generated: {results_csv}')
pip install pandas gitpython openpyxl
