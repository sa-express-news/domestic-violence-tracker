from sys import argv

import getdata

def main():
    try:
        state, year = argv[1:]
    except IndexError as e:
        print('Please pass a state and year to get data')
    
    datalist = getdata.build_datalist(state, year)

if __name__ == "__main__":
    main()