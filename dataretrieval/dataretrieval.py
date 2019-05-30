from sys import argv

from tablebuilder import TableBuilder
from exporters import export_to_csv


def main():
    try:
        state, year = argv[1:]
    except IndexError as e:
        print('Please pass a state and year to get data')

    table_builder = TableBuilder(state, year)

    for incident in table_builder.run_data_generator():
        if table_builder.is_domestic_violence(incident) is True:
            table_builder.populate_tables(incident)
    
    for file in table_builder.eject_all_tables():
        export_to_csv(file['name'], file['table'])


if __name__ == "__main__":
    main()
