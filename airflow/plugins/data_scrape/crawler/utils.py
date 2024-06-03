import yaml

def read_yaml(filename:str):
    with open(filename, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as ex:
            print(ex)