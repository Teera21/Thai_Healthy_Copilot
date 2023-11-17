import json

import os.path



def read_name():
    # Opening JSON file
    path = 'information.json'
    check_file = os.path.isfile(path)
    if check_file:
        f = open('information.json')
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        if 'name' in data:
            if data['name'] != "":
                return data['name']
        else:
            return ''
