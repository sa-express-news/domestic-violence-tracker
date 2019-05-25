import requests
import io
import zipfile

import filename_map


class ZipGenerator():
    """Get the data in zipped CSVs from the FBI"""

    base_path = 'http://s3-us-gov-west-1.amazonaws.com/cg-d4b776d0-d898-4153-90c8-8336f86bdfec'

    def __init__(self, state, year):
        self.state = state
        self._url = self._build_url(state, year)
        self._response = None

    @classmethod
    def _build_url(cls, state, year):
        """FBI URL structure as of 5/21/2019"""
        return f'{cls.base_path}/{year}/{state}-{year}.zip'

    def _get_incidents_idx(self, lst):
        for zip in lst:
            if zip.filename == f'{self.state}/NIBRS_incident.csv':
                return lst.index(zip)
        return None

    def _move_incidents_to_end_of_list(self, infolist):
        """Intention here is to make sure the incidents CSV yields
        last by moving it to end of list
        """
        infolist.append(infolist.pop(self._get_incidents_idx(infolist)))
        return infolist

    def download_zip(self):
        self._response = requests.get(self._url)

    def extract_zip(self):
        """Yield all of the files contained in the zip for a single state and year"""
        if self._response is None:
            self.download_zip()
        with zipfile.ZipFile(io.BytesIO(self._response.content)) as thezip:
            for zipinfo in self._move_incidents_to_end_of_list(thezip.infolist()):
                with thezip.open(zipinfo) as thefile:
                    yield zipinfo.filename, io.TextIOWrapper(thefile, encoding="utf-8")
