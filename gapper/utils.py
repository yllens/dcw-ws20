"""
Author: yllens
Last edited: 24th April 2021 
Desription: Helper functons getting file paths and generating file paths.
"""

import os
import json


def get_file_paths(root_dir):
    """ Get paths of all files in raw directory.

    :param root_dir:  Directory in which to look for files
    :return:          List of file paths
    """
    file_paths = []
    for subdir, dirs, files in os.walk(root_dir, topdown=True):
        for file in files:
            path = os.path.join(subdir, file)
            file_paths.insert(0, path)

    file_paths = [path for path in file_paths if not path.endswith('.DS_Store')]

    return file_paths


def generate_json(source_directory, target_file):
    """"
    Generates .js file for all texts saved in the source_directory.
    """
    gap_id = 1
    formated_data = []
    for filename in os.listdir(source_directory):
        if filename.endswith('.txt'):
            file_data = []
            with open('{}/{}'.format(source_directory, filename), 'r') as f:
                content = f.readline().split(' ')
                for token in content:
                    if '[gap]' in token:
                        token = token.split('[gap]')
                        gap = token[1].split('[/gap]')[0] # necessary bc 'eit[/gap].' is not striped correctly otherwise
                        entry = {"gap_id": "gap_{}".format(str(gap_id)),
                                 "gap": True,
                                 "correctAnswer": gap,
                                 "token": token[0]}
                        gap_id += 1
                    else:
                        entry = {"gap_id": "none",
                                 "gap": False,
                                 "correctAnswer": "",
                                 "token": token}
                    file_data.append(entry)
            formated_data.append(file_data)
    with open(target_file, 'w') as f:
        json.dump(formated_data, f, indent=4, ensure_ascii=False)
