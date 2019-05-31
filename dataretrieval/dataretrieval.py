import argparse

from tablebuilder import TableBuilder
from exporters import export_to_csv, export_to_data_world

parser = argparse.ArgumentParser()
parser.add_argument('state', help='Targeted state')
parser.add_argument('year', help='Targeted year')
parser.add_argument('--outdir', help='Path to output directory if creating CSVs, will be created if necessary')
parser.add_argument('--dest', help='Format and destination for data output', choices=['api', 'csv'])
parser.add_argument('--isfirst', help='Used by apimultiretrieval to clear old data from data.world dataset', action='store_true')


def main():
    args = parser.parse_args()
    outdir = args.outdir if args.outdir is not None else './output'

    print(f'Building tables for state: {args.state}, year: {args.year}')

    table_builder = TableBuilder(args.state, args.year)

    for incident in table_builder.run_data_generator():
        if table_builder.is_domestic_violence(incident) is True:
            table_builder.populate_tables(incident)

    for file in table_builder.eject_all_tables():
        if args.dest == 'api':
            print(f'Exporting {file["filename"]}')
            export_to_data_world(file['name'], file['table'], args.isfirst)
        else:
            export_to_csv(outdir, file['filename'], file['table'])

if __name__ == "__main__":
    main()
