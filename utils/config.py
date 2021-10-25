import yaml
from dotted_dict import DottedDict

def load_config():
    with open("config.yaml") as file:
        config = yaml.safe_load(file)
    return DottedDict(config)