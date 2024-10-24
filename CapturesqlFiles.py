import os
import csv

def find_db_folder_and_capture_files(root_folder, output_csv):
    # List to hold the file information
    file_info_list = []

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Check if the current directory is the 'db' folder
        if 'db' in dirnames:
            db_folder_path = os.path.join(dirpath, 'db')
            # Walk through the 'db' folder and its subfolders
            for db_dirpath, db_dirnames, db_filenames in os.walk(db_folder_path):
                for filename in db_filenames:
                    # Capture file information
                    file_location = os.path.join(db_dirpath, filename)
                    file_name, file_extension = os.path.splitext(filename)
                    previous_folder_name = os.path.basename(os.path.dirname(file_location))
                    file_info_list.append([file_location, file_name, file_extension, previous_folder_name])

    # Write the file information to a CSV file
    with open(output_csv, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File Location', 'File Name', 'File Extension', 'Previous Folder Name'])
        csv_writer.writerows(file_info_list)

# Example usage
root_folder = 'c:/test/repo'
output_csv = 'output.csv'
find_db_folder_and_capture_files(root_folder, output_csv)
