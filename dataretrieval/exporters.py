import os
from csv import DictWriter


def create_csv_dir(dir_name):
    if os.path.isdir(dir_name) is not True:
        os.mkdir(dir_name)


def export_to_csv(dir_name, file_name, table):
    create_csv_dir(dir_name)
    keys = table[0].keys()
    with open(f'{dir_name}/{file_name}.csv', 'w') as output_file:
        dict_writer = DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(table)
