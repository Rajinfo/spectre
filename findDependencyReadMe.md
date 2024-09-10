# Batch Script to Process Git Repositories and Analyze Dependencies

## Overview

This script processes a list of Git repository URLs from a CSV file. For each repository, it:
- Clones the repository to a local folder .
- Searches for build files (`build.gradle`, `pom.xml`, `package.json`).
- Determines the type of project (Gradle, Maven, Angular, etc.).
- Analyzes Gradle dependencies and checks for specific `.jar` and `.wsdl` files.
- Logs output to various CSV files for dependencies, errors, and project types.

## Prerequisites

1. **Git**: Ensure Git is installed and accessible from the command line.
2. **Gradle**: The script uses Gradle to fetch dependencies. Make sure Gradle is installed and added to the system's PATH.
3. **Java**: Java must be installed and available since the script processes Java-based repositories.

## File Structure (example)

- `D:\program\test\file.csv`: Input CSV file containing a list of repository URLs.
- `D:\program\test\gw_all_projects_dependencies.csv`: Output CSV file containing project dependencies.
- `D:\program\test\gw_dependency_errors.txt`: Output text file containing errors encountered during processing.
- `D:\program\test\gw_no_dependency.csv`: Output CSV file listing projects that don't contain any dependencies.
- `D:\program\test\gw_repo_type.csv`: Output CSV file listing project types (Gradle, Maven, Angular, etc.).

## Script Files

- **Input CSV (`file.csv`)**: This file contains a list of Git URLs, one per line.
https://github.com/user/project1,
https://github.com/user/project2,
...

csharp
Copy code

## Script Setup

1. **Edit the `base_directory`**: Set the base directory in the script where the repositories will be cloned or searched. 
 In this case, it is:
 ```batch
 set "base_directory=D:\program\test\"
Input CSV File: Prepare the file.csv with Git URLs in the specified directory (D:\program\test\file.csv).

Output Files: The output files will be automatically created or overwritten:

gw_all_projects_dependencies.csv: Logs dependencies found in each project.
gw_dependency_errors.txt: Logs errors encountered while processing projects.
gw_no_dependency.csv: Logs projects where no dependencies were found.
gw_repo_type.csv: Logs the type of repository (Gradle, Maven, Angular, etc.).


Running the Script
Steps:
Open a command prompt.
Navigate to the folder containing the batch script.
Run the script by typing the following command:
FindDependency.bat
Ensure that FindDependency.bat matches the filename of the script you saved.

What the Script Does:
Reads Git URLs from the file.csv file.
For each URL, it extracts the project name and checks if the folder exists.
Searches for build.gradle and CmnBuild.gradle files to extract dependencies.
If any .jar or .wsdl files are present, they are logged.
Checks the type of project based on the presence of certain files (build.gradle, pom.xml, package.json).
Output Files:
gw_all_projects_dependencies.csv: Contains the following columns:

Project Name
Project Path
Dependency Details
Dependency Jar/WSDL Name

gw_dependency_errors.txt: Contains detailed error logs encountered during the process.

gw_no_dependency.csv: Contains a list of projects without any recognized dependencies.

gw_repo_type.csv: Contains the following columns:

Project Name
Project Path
Type (Gradle, Maven, Angular, etc.)

Troubleshooting
If the script does not run, ensure that the batch file is correctly formatted and paths to git, gradle, and java are correctly set in your environment.
Make sure the input CSV file is properly formatted and saved in the correct location.
If any errors occur, check the gw_dependency_errors.txt file for details.