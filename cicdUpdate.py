import os
import shutil
import json
import csv

def copy_folder(src, dest):
    try:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('.git', '.gitignore'))
        print(f"Copied {src} to {dest}")
    except Exception as e:
        print(f"Error copying folder: {e}")

def update_config_file(config_file_path, artfVer, rootProjNm):
    try:
        with open(config_file_path, 'r') as file:
            lines = file.readlines()

        with open(config_file_path, 'w') as file:
            for line in lines:
                if 'artfVer=' in line:
                    file.write(f'    artfVer="{artfVer}"\n')
                elif 'rootProjNm=' in line:
                    file.write(f'    rootProjNm="{rootProjNm}"\n')
                else:
                    file.write(line)
        print(f"Updated config file at {config_file_path}")
    except Exception as e:
        print(f"Error updating config file: {e}")

def add_script_entry_if_db_folder_exists(root_folder_path, data, schemas):
    db_folder_path = os.path.join(root_folder_path, 'db')
    if os.path.exists(db_folder_path) and os.path.isdir(db_folder_path):
        for subfolder in os.listdir(db_folder_path):
            subfolder_path = os.path.join(db_folder_path, subfolder)
            if os.path.isdir(subfolder_path) and any(os.path.isfile(os.path.join(subfolder_path, f)) for f in os.listdir(subfolder_path)):
                new_script_entry = {
                    "script": f"/db/{subfolder}/*",
                    "schemas": [schemas]
                }
                for item in data:
                    item['scripts'].append(new_script_entry)
                break

def update_json_files(folder_path, updates, schemas):
    for update in updates:
        file_name = update['FileName']
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            for item in data:
                item['tnsEntry'] = update['tnsEntry']
                item['dbInstance'] = update['dbInstance']
            
            add_script_entry_if_db_folder_exists(folder_path, data, schemas)
            
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Updated {file_path}")
        else:
            print(f"File {file_name} not found in {folder_path}")

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def main():
    folders_csv = input("Enter the path of the CSV file containing folder paths: ")
    updates_csv = input("Enter the path of the CSV file containing updates: ")
    schemas = input("Enter the schemas value: ")
    artfVer = input("Enter the artfVer value: ")

    # Read folder paths
    folders = read_csv(folders_csv)
    for folder in folders:
        src_folder = folder['src_folder']
        dest_folder = folder['dest_folder']
        root_folder = folder['rootfolder']

        # Copy the .cicd folder
        copy_folder(src_folder, dest_folder)

        # Update config file
        config_file_path = os.path.join(dest_folder, 'config.groovy')
        update_config_file(config_file_path, artfVer, root_folder)

        # Read updates
        updates = read_csv(updates_csv)

        # Update JSON files in the copied folder
        cicd_folder_path = os.path.join(dest_folder, '.cicd')
        update_json_files(cicd_folder_path, updates, schemas)

if __name__ == "__main__":
    main()
