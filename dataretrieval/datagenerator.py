from io import TextIOWrapper
import csv
import itertools

import filename_map
from zipgenerator import ZipGenerator


class DataGenerator():
    """ Run a generator that will iterator over all the incidents in the data
        and, while generator runs, provide hashes to access the related data
    """

    def __init__(self, state, year):
        self.zip_generator = ZipGenerator(state, year)
        self._dict = {}  # A lookup used for binding offenders, victims, etc to incidents

    def __getattr__(self, attr):
        return getattr(self.zip_generator, attr)

    def _filter_cols(self, lookup, row):
        """Filtered out only the columns wanted from each csv"""
        return {col: row[col] for col in lookup['cols'] if col in row}

    def _map_filter_cols(self, lookup, row):
        """Since agency files differ between years, we need to map to matching values and filter.
            This is achieved by adding a 'map_col_names_to' property to the filename_map for files produced
            before 2016 and mapping their column names to the names on the newer files
        """
        hash = dict()
        for idx, col in enumerate(lookup['cols']):
            if col in row:
                key = filename_map.map_col_name(lookup, idx)
                hash[key] = row[col]
        return hash

    def _lowercase_first_row(self, iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    def _byte_to_text(self, file):
        return self._lowercase_first_row(TextIOWrapper(file, encoding="utf-8"))

    def _add_to_dict(self, lookup, file):
        """Add a CSV to the dictionary to be referenced while iterating incidents
            This is expensive, but I think the lookup time saved by building a
            reference hash is worth it overall
        """
        self._dict[lookup['key']] = {}

        filter = self._map_filter_cols if 'map_cols_to' in lookup else self._filter_cols

        for row in csv.DictReader(self._byte_to_text(file)):
            try:
                uniqID = row[lookup['uniq']]
                rowHash = filter(lookup, row)
                if uniqID in self._dict[lookup['key']]:
                    self._dict[lookup['key']][uniqID].append(rowHash)
                else:
                    self._dict[lookup['key']][uniqID] = [rowHash]
            except:
                print('error with %s' % (name))

    def _get_hash_arr(self, key, uniq):
        arr = None
        try:
            arr = self._dict[key][uniq]
        finally:
            return arr

    def run_generator(self):
        """This is the main method, it yields the incidents and places the related data in hashes"""
        for name, file in self.extract_zip():
            if 'nibrs_incident.csv' in name.lower():  # by design, this is the last element in the list
                for row in csv.DictReader(self._byte_to_text(file)):
                    yield row
            elif filename_map.key_exists(name):
                lookup = filename_map.get_data(name)
                self._add_to_dict(lookup, file)
        self._dict.clear()
