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

def copy_file(src_file, dest_file):
    try:
        shutil.copy2(src_file, dest_file)
        print(f"Copied {src_file} to {dest_file}")
    except Exception as e:
        print(f"Error copying file: {e}")

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

def write_csv(file_path, data):
    fieldnames = ['rootFolder', 'CICD Status']
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def delete_folder(folder_path):
    try:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")
    except Exception as e:
        print(f"Error deleting folder: {e}")

def main():
    folders_csv = input("Enter the path of the CSV file containing folder paths: ")
    updates_csv = input("Enter the path of the CSV file containing updates: ")
    output_csv = input("Enter the path of the output CSV file: ")
    schemas = input("Enter the schemas value: ")
    artfVer = input("Enter the artfVer value: ")

    # Read folder paths
    folders = read_csv(folders_csv)
    output_data = []

    for folder in folders:
        src_folder = folder['src_folder']
        dest_folder = folder['dest_folder']
        root_folder = folder['rootfolder']
        tobeprocess = folder['tobeprocess'].lower() == 'true'

        if tobeprocess:
            # Delete .jenkins folder if it exists in the destination
            jenkins_folder_path = os.path.join(dest_folder, '.jenkins')
            delete_folder(jenkins_folder_path)

            # Check if .cicd folder exists in destination
            cicd_folder_path = os.path.join(dest_folder, '.cicd')
            if not os.path.exists(cicd_folder_path):
                # Copy the .cicd folder
                copy_folder(os.path.join(src_folder, '.cicd'), cicd_folder_path)

                # Update config file
                config_file_path = os.path.join(dest_folder, 'config')
                update_config_file(config_file_path, artfVer, root_folder)

                # Read updates
                updates = read_csv(updates_csv)

                # Update JSON files in the copied folder
                update_json_files(cicd_folder_path, updates, schemas)

                output_data.append({'rootFolder': root_folder, 'CICD Status': 'Done'})
            else:
                print(f".cicd folder already exists in {dest_folder}, skipping copy and update.")
                output_data.append({'rootFolder': root_folder, 'CICD Status': 'AlreadyAvailable'})

            # Check if .gitlab-ci.yml file exists in destination
            gitlab_ci_file_path = os.path.join(dest_folder, '.gitlab-ci.yml')
            if not os.path.exists(gitlab_ci_file_path):
                # Copy the .gitlab-ci.yml file
                copy_file(os.path.join(src_folder, '.gitlab-ci.yml'), gitlab_ci_file_path)
            else:
                print(f".gitlab-ci.yml file already exists in {dest_folder}, skipping copy.")
        else:
            print(f"Skipping folder {root_folder} as tobeprocess is false.")
            output_data.append({'rootFolder': root_folder, 'CICD Status': 'Skipped'})

    # Write the output CSV file
    write_csv(output_csv, output_data)

if __name__ == "__main__":
    main()
