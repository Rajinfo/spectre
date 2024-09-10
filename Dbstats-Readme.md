MyBatis/iBATIS and SQL Table & Object Extractor
This Python script scans through directories listed in a CSV file, searches for MyBatis/iBATIS mapper XML and SQL files, and extracts table names, procedures, views, triggers, and operations. The extracted information is saved to an output CSV file.
Prerequisites
To run this script, ensure the following is installed on your machine:
1.	Python 3.x: If you don't have Python installed, download it from Software center.
2.	CSV Input: A CSV file containing folder names where the script should search for files.
3.	Required Python Libraries:
o	No external libraries are required as the script uses built-in Python libraries.
Installation
1.	Download and install Python 3 from the official website: https://www.python.org/.
2.	Clone or download the script into your working directory.
Running the Script
Step 1: Prepare Input CSV
•	Create a CSV file listing the directories you want to scan. Each row should contain the path to a folder, e.g., D:/projects/myfolder.
•	Example of the input CSV format (file-db.csv):
D:/projects/folder1
D:/projects/folder2
D:/projects/folder3
Step 2: Update Script Paths
•	Update the paths to your input CSV and output CSV in the script. Replace the values of csv_input and csv_output variables:
csv_input = 'D:/program/test/file-db.csv'  # Path to your input CSV
csv_output = 'D:/program/test/out-reponsedb.csv'  # Path for output CSV
Step 3: Running the Script
1.	Open a command prompt or terminal window.
2.	Navigate to the directory where the script is saved.
3.	Run the script using Python:
python mybatis_sql_extractor.py
Replace mybatis_sql_extractor.py with the actual filename of your script.
Step 4: Output CSV
Once the script has completed, the extracted information will be saved in the output CSV file. This file will have the following columns:
•	FolderName: The folder where the file is located.
•	FolderPath: Full path to the folder.
•	FilePath: Full path to the file.
•	FileName: Name of the XML or SQL file.
•	ObjectName: The name of the table, procedure, function, view, or trigger.
•	ObjectType: Type of object (Table, PLSQL, View, Trigger, Materialized View).
•	OperationType: Type of operation (create, alter, delete, update, select, insert, merge, etc.).
Example
Table names extracted and saved to D:/program/test/out-reponsedb.csv
Debugging and Logs
The script prints messages to the console, showing the folder names being processed and the objects and operations extracted from each file.

