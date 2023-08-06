import json
import yaml

def open_yaml(file_path, file_name):
    yaml_file=file_path + file_name
    with open(yaml_file) as openfile:
        yaml_object=yaml.load(openfile,Loader=yaml.FullLoader)
        return yaml_object # retourne un dictionnaire


def open_json(file_path, file_name):
    
    json_file=file_path + file_name
    
    with open(json_file,'r') as openfile:
        json_object=json.load(openfile)
        return json_object

        

def save_yaml(path, decoded_dictionary, yaml_file_name):
    
    yaml_file= path + yaml_file_name
    
    with open (yaml_file, "w") as outfile:
        yaml.dump(decoded_dictionary, outfile, default_flow_style=False)

def save_json(path, decoded_dictionary, json_file_name):
    
    my_file= path + json_file_name
    with open(my_file, "w") as outfile:
        json.dump(decoded_dictionary, outfile, indent=2)

