'''
Create a complex list.  writie it out to a file with yaml and json.
'''

import yaml
import json

def main():

    yaml_file = 'my_test.yml'
    json_file = 'my_test.json'

    # Create a dictionary
    my_dict = {
        'Flower': 'Orchid',
        'Tree': 'Aspen',
        'Grass': 'Zoysia'
    }

    #Create a list
    my_list = [
    'some string',
    'another string',
    99,
    14,
    my_dict,
    'the last string'
    ]

    with open(yaml_file, "w") as f:
        f.write(yaml.dump(my_list, default_flow_style=False))

    with open(json_file, "w") as f:
        json.dump(my_list, f)

if __name__ == '__main__':
    main()
