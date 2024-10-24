import os
import csv

def find_db_and_crudb_folders_and_capture_files(root_folder, output_csv):
    # List to hold the file information
    file_info_list = []

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Check if the current directory contains 'db' or 'crudb' folder
        for folder in ['db', 'crudb']:
            if folder in dirnames:
                target_folder_path = os.path.join(dirpath, folder)
                # Walk through the target folder and its subfolders
                for target_dirpath, target_dirnames, target_filenames in os.walk(target_folder_path):
                    for filename in target_filenames:
                        # Capture file information
                        file_location = os.path.join(target_dirpath, filename)
                        file_name, file_extension = os.path.splitext(filename)
                        previous_folder_name = os.path.basename(os.path.dirname(file_location))
                        root_folder_name = os.path.basename(os.path.dirname(target_dirpath))
                        file_info_list.append([root_folder_name, file_location, file_name, file_extension, previous_folder_name])

    # Write the file information to a CSV file
    with open(output_csv, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Root Folder', 'File Location', 'File Name', 'File Extension', 'Previous Folder Name'])
        csv_writer.writerows(file_info_list)

# Example usage
root_folder = 'c:/test/repo'
output_csv = 'output.csv'
find_db_and_crudb_folders_and_capture_files(root_folder, output_csv)
