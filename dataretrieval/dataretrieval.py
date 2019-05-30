from sys import argv

from tablebuilder import TableBuilder
# from exporttable import ExportTable


def main():
    try:
        state, year = argv[1:]
    except IndexError as e:
        print('Please pass a state and year to get data')

    table_builder = TableBuilder(state, year)

    itr = 0

    for incident in table_builder.run_data_generator():
        if table_builder.is_domestic_violence(incident) is True:
            itr += 1
    print(itr)


if __name__ == "__main__":
    main()
