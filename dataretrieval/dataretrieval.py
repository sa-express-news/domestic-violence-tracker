from sys import argv

from datagenerator import DataGenerator


def main():
    try:
        state, year = argv[1:]
    except IndexError as e:
        print('Please pass a state and year to get data')
    
    data_generator = DataGenerator(state, year)

    itr = 0

    for incident in data_generator.run_generator():
        if data_generator.is_domestic_violence(incident) is True:
            itr += 1
    print(itr)


if __name__ == "__main__":
    main()