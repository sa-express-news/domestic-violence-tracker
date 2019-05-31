import argparse

from tablebuilder import TableBuilder
from exporters import export_to_csv

parser = argparse.ArgumentParser()
parser.add_argument('state', help='Targeted state')
parser.add_argument('year', help='Targeted year')


def main():
    args = parser.parse_args()

    table_builder = TableBuilder(args.state, args.year)

    for incident in table_builder.run_data_generator():
        if table_builder.is_domestic_violence(incident) is True:
            table_builder.populate_tables(incident)

    for file in table_builder.eject_all_tables():
        export_to_csv(file['name'], file['table'])

if __name__ == "__main__":
    main()
