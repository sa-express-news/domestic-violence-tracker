import requests
import io
import zipfile
import csv

def download_extract_zip(url):
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        for zipinfo in thezip.infolist():
            with thezip.open(zipinfo) as thefile:
                yield zipinfo.filename, thefile

def build_url(state, year):
    base = 'http://s3-us-gov-west-1.amazonaws.com/cg-d4b776d0-d898-4153-90c8-8336f86bdfec'
    ext = '.zip'
    return f'{base}/{year}/{state}-{year}.zip'

def build_datalist(state, year):
    for name, file in download_extract_zip(build_url(state, year)):
        if name[-4:] == '.csv':
            if name == 'TX/NIBRS_PROP_DESC_TYPE.csv':
                data = io.TextIOWrapper(io.BytesIO(file.read()))
                for row in data:
                    print(row)
