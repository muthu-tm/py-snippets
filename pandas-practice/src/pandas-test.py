import os
import time
import json
import pandas as pd
import traceback

start_time = time.time()

script_dir = os.path.dirname(__file__)
configuration = json.load(open(os.path.join(script_dir, 'config.json'),"r"))
dir_location = configuration["dir_location"]

number_of_files = 0

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path, skip_blank_lines=True, error_bad_lines=False)
        return data
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(file_path)
        print('Failed to load CSV file: ', e)


def main():
    global number_of_files

    for input in dir_location:
        file_path = input["path"]
        number_of_files = number_of_files + 1
        data = load_csv(file_path)
        rows, cols = data.shape
        print("ROWS count: ", rows)
        print("COLS count: ", cols)

        for index in data.iterrows():
            try:
                row_data = index
                print(row_data)
            except Exception as e:
                print(e)
                traceback.print_tb(e.__traceback__)
                print(traceback.print_tb(e.__traceback__))



print("Starting the service!")
main()
print("Number of FILES processed - "+ str (number_of_files))
print("Total time took for the execution - "+ str((time.time() - start_time)/60) + " minutes")