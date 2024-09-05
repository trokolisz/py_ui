
''' parsing config file '''
import configparser 


# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the INI file
config.read('config/config.ini')

# Example: Accessing a specific section and key
def get_config_value(section, key):
    try:
        return config[section][key]
    except KeyError:
        return None

# Example usage:
if __name__ == "__main__":
    section_name = 'data_csv'
    key_name = 'path'
    value = get_config_value(section_name, key_name)
    if value:
        print(f"The value of '{key_name}' in section '{section_name}' is: {value}")
    else:
        print(f"'{key_name}' not found in section '{section_name}'")