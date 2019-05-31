import os
import json
import requests
from csv import DictWriter
from urllib.parse import quote


def create_csv_dir(dir_name):
    if os.path.isdir(dir_name) is not True:
        os.mkdir(dir_name)


def export_to_csv(dir_name, name, table):
    create_csv_dir(dir_name)
    file_name = f'{name}.csv'
    keys = table[0].keys()
    with open(f'{dir_name}/{file_name}', 'w') as output_file:
        dict_writer = DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(table)


def get_api_key():
    with open('./credentials.json') as creds:
        credentials = json.load(creds)
        return credentials['DW_API_KEY']


def get_sql_query(name):
    return quote(f'SELECT * FROM {name}', safe='*')


def get_file_from_data_world(name, api_key):
    url = f'https://api.data.world/v0/sql/expressnews/domestic-violence-tracker?query={get_sql_query(name)}'
    return requests.get(
        url,
        headers={
            'Authorization': f'Bearer {api_key}',
        }
    )


def post_file_to_data_world(dir_name, file_name, api_key):
    url = 'https://api.data.world/v0/uploads/expressnews/domestic-violence-tracker/files'
    with open(f'./{dir_name}/{file_name}', 'r') as file:
        return requests.post(
            url,
            headers={
                'Authorization': f'Bearer {api_key}',
            },
            files={
                'file': (file_name, file)
            }
        )


def export_to_data_world(name, table, isfirst):
    file_name = f'{name}.csv'
    api_key = get_api_key()

    response = get_file_from_data_world(name.replace("-", "_"), api_key)

    if response.status_code == 200 and isfirst is not True:
        master = response.json() + table
    else:
        master = table

    export_to_csv('temp', name, master)
    response = post_file_to_data_world('temp', file_name, api_key)

    try:
        if response.status_code != 200:
            raise Exception('File did not upload correctly!!!')
        os.remove(f'./temp/{file_name}')
        print('Upload successful!!')
    except Exception as e:
        print(e)
