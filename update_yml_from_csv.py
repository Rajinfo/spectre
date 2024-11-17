import yaml
import csv

def set_nested_value(data, key_path, new_value):
    """
    Sets a nested value in a dictionary based on a dot-separated key path.
    """
    keys = key_path.split(".")
    current = data
    for key in keys[:-1]:
        current = current.setdefault(key, {})
    current[keys[-1]] = new_value

def update_yml_from_csv(yml_file_path, csv_file_path):
    """
    Updates a YAML file with keys and values from a CSV file.
    
    Args:
    - yml_file_path (str): Path to the application.yml file.
    - csv_file_path (str): Path to the CSV file containing keys and values.
    """
    try:
        # Load the YAML file
        with open(yml_file_path, 'r') as yml_file:
            config = yaml.safe_load(yml_file)

        # Read the CSV file
        with open(csv_file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            # Ensure the CSV contains 'key' and 'value' columns
            if 'key' not in reader.fieldnames or 'value' not in reader.fieldnames:
                print("CSV file must contain 'key' and 'value' columns.")
                return
            
            # Update the YAML structure with CSV values
            for row in reader:
                key = row['key']
                value = row['value']
                set_nested_value(config, key, value)
                print(f"Updated '{key}' to '{value}'.")

        # Write the updated YAML back to the file
        with open(yml_file_path, 'w') as yml_file:
            yaml.safe_dump(config, yml_file)

        print(f"YAML file '{yml_file_path}' updated successfully.")
    
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except yaml.YAMLError as exc:
        print(f"Error processing YAML file: {exc}")
    except Exception as exc:
        print(f"An error occurred: {exc}")

# Example usage
yml_file_path = 'application.yml'  # Path to the application.yml file
csv_file_path = 'update_keys.csv'  # Path to the CSV file

update_yml_from_csv(yml_file_path, csv_file_path)
