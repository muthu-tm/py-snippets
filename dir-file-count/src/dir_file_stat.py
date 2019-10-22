import os
import time
import json
from datetime import datetime

start_time = time.time()

script_dir = os.path.dirname(__file__)
configuration = json.load(open(os.path.join(script_dir, 'config.json'),"r"))
dir_location = configuration["dir_location"]
output_file_name = configuration["output_file_name"]

number_of_files = 0
number_of_dir = 0

def write_mapping_json_file(output_dir, data):
    global output_file_name
    file_name = output_file_name
    with open(output_dir + file_name, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

def get_file_extension(file_name):
    if len(file_name.split(os.extsep,1)) < 2:
        ext = 'None'
    else:
        ext = file_name.split(os.extsep,1)[-1]
    return ext


def update_counts(file_extension, path, dir_json):
    if file_extension in dir_json:
        total = dir_json[file_extension].get("count")
        dir_json[file_extension]["count"] = total + 1
        dir_json[file_extension]["paths"].append(path)
    else:
        ext = {
            "count": 1,
            "paths": []
        }
        dir_json[file_extension] = ext
        dir_json[file_extension]["paths"].append(path)


def update_dir_count(dir_json, sub_dir_json):
    for file_extension in sub_dir_json:
        if file_extension in dir_json:
            total = sub_dir_json[file_extension].get("count")
            dir_total = dir_json[file_extension].get("count")
            dir_json[file_extension]["count"] = dir_total + total
            for path in sub_dir_json[file_extension]["paths"]:
                dir_json[file_extension]["paths"].append(path)
        else:
            total = sub_dir_json[file_extension].get("count")
            ext = {
                "count": total,
                "paths": sub_dir_json[file_extension]["paths"]
            }
            dir_json[file_extension] = ext



def get_sub_dir_stat(project_location, number_of_files, number_of_dir):
    sub_dir_json = {}

    for root, dirs, files in os.walk(project_location, topdown=True):
        for file in files:
            path = os.path.join(root, file)
            file_extension = get_file_extension(file)
            number_of_files = number_of_files + 1
            update_counts(file_extension, path, sub_dir_json)

        for dir in dirs:
            path = os.path.join(root, dir)
            number_of_dir = number_of_dir + 1
            get_sub_dir_stat(path, number_of_files, number_of_dir)

    return sub_dir_json


def main():
    global number_of_files, number_of_dir

    for input in dir_location:
        dir_json = {}
        for root, dirs, files in os.walk(input["path"], topdown=True):
            for file in files:
                path = os.path.join(root, file)
                number_of_files = number_of_files + 1
                file_extension = get_file_extension(file)
                update_counts(file_extension, path, dir_json)

            for dir in dirs:
                number_of_dir = number_of_dir + 1
                path = os.path.join(root, dir)
                sub_dir_stat = get_sub_dir_stat(path, number_of_files, number_of_dir)
                update_dir_count(dir_json, sub_dir_stat)


        write_mapping_json_file(input["path"], dir_json)
        print("Processed the dir - " + input["path"])


print("Starting the dir_file_count service!")
main()
print("Number of FILES - "+ str (number_of_files))
print("Number of DIRECTORIES - "+ str (number_of_dir))

print("Total time took for the execution - "+ str((time.time() - start_time)/60) + " minutes")