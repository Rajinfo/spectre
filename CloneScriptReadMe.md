Batch Script to Clone Git Repositories from CSV
This script automates the process of cloning multiple Git repositories and switching to specific branches, using a CSV file as input. Each line in the CSV should include a repository URL and the branch name you want to switch to.

Prerequisites:
Before running the script, ensure the following prerequisites are met:
1.	Git: Make sure Git is installed on your machine. You can download and install it from here.
2.	CSV File Format: You need a CSV file where each line contains:
o	The repository URL
o	The branch name to switch to after cloning The format should be as follows:
repo_url,branch_name
https://github.com/user/repo1,main
https://github.com/user/repo2,develop
3.	CSV File Path: Update the script to point to the correct path of your CSV file.
How to Set Up
1.	Clone the script: Save the provided script to a .bat file, for example, clone_repos.bat.
2.	Update the script:
o	Modify the csv_file variable to the path where your CSV file is located.
o	Modify the base_dir variable to the directory where you want to clone the repositories.
Example:
:: Set the path to your CSV file
set "csv_file=D:\program\test\file.csv"

:: Set the base directory where repositories will be cloned
set "base_dir=D:\program\test"
3.	CSV File Structure: Create or update your CSV file with the format mentioned in the prerequisites section. Each line should represent a repository and the branch to switch to after cloning.
Steps to Run
1.	Open Command Prompt:
o	Press Windows + R, type cmd, and press Enter.
2.	Navigate to Script Location:
o	Use the cd command to change the directory to the location where the script is saved. For example:
cd D:\path\to\your\script
3.	Run the Script:
o	Type the name of your .bat file and press Enter. For example:
clone_repos.bat
What the Script Does
•	Reads the CSV file.
•	For each repository URL and branch:
1.	It clones the repository from the given URL.
2.	It extracts the repository name from the URL.
3.	It switches to the specified branch.
•	After processing each repository, it returns to the base directory to start the process for the next repository.
Troubleshooting
•	Ensure Git is installed and properly configured in your system's PATH.
•	Verify the CSV file is formatted correctly and located at the specified path.
•	Check that the base directory exists and has write permissions.
Example CSV File
repo_url,branch_name
https://github.com/user/repo1,main
https://github.com/user/repo2,develop
Script Details
•	Variables:
o	csv_file: Path to the CSV file.
o	base_dir: Directory where repositories will be cloned.
•	Main Process:
o	Clones the repository URL from the CSV.
o	Switches to the specified branch.
o	Resets to the base directory after each repository operation.