import requests
import io
import zipfile

import filename_map


class ZipGenerator():
    """Get the data in zipped CSVs from the FBI"""

    new_base_path = 'http://s3-us-gov-west-1.amazonaws.com/cg-d4b776d0-d898-4153-90c8-8336f86bdfec'

    old_base_path = 'http://s3-us-gov-west-1.amazonaws.com/cg-d3f0433b-a53e-4934-8b94-c678aa2cbaf3'

    def __init__(self, state, year):
        self.state = state
        self._url = self._build_url(state, year)
        self._response = None

    @classmethod
    def _build_url(cls, state, year):
        """FBI URL structure as of 5/21/2019"""
        base = cls.new_base_path if year > 2015 else cls.old_base_path
        return f'{base}/{year}/{state}-{year}.zip'

    def _get_incidents_idx(self, lst):
        for zip in lst:
            if 'nibrs_incident.csv' in zip.filename.lower():
                return lst.index(zip)
        return None

    def _move_incidents_to_end_of_list(self, infolist):
        """Intention here is to make sure the incidents CSV yields
        last by moving it to end of list
        """
        try:
            infolist.append(infolist.pop(self._get_incidents_idx(infolist)))
        except(e):
            print(e)
        finally:
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
