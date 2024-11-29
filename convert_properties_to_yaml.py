import yaml

def properties_to_dict(properties_file):
    """Convert properties file to a nested dictionary."""
    result = {}
    with open(properties_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            keys = key.split('.')
            d = result
            for k in keys[:-1]:
                if k not in d:
                    d[k] = {}
                d = d[k]
            d[keys[-1]] = value
    return result

def dict_to_yaml(data_dict, yaml_file):
    """Convert dictionary to YAML and save to a file."""
    with open(yaml_file, 'w') as file:
        yaml.dump(data_dict, file, default_flow_style=False)

def convert_properties_to_yaml(properties_file, yaml_file):
    """Convert properties file to YAML file."""
    data_dict = properties_to_dict(properties_file)
    dict_to_yaml(data_dict, yaml_file)

# Example usage
properties_file = 'example.properties'
yaml_file = 'example.yaml'
convert_properties_to_yaml(properties_file, yaml_file)
