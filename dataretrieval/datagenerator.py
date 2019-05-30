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
        """Add a CSV row to the dictionary to be referenced while iterating incidents.
            Rows are stored in an array to accomodate multiples. For instance, two victims
            of one incident. This operation is expensive, but I think the lookup time
            saved by building a reference hash is worth it overall
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

    def _get_hash_list(self, key, uniq):
        """Grab a list of dictionaries from a csv (key) with a unique ID (uniq)
            For instance, uniq could be a victim_id or offense_id. A list is returned instead
            of a single hash because, occassionally, incidents will involve multiple victims,
            offenders, etc. If you know for sure you are pulling a list with one value
            (eg a reference like 'agencies' or 'race_ref') use self._get_hash instead.
        """
        arr = None
        try:
            arr = self._dict[key][uniq]
        finally:
            return arr

    def _get_hash(self, key, uniq):
        """Grab a single victim, offender, etc hash. These are stored in lists (see self._get_hash_list)
            and this method should be used when you are sure only one value exists in the list. If more than
            one hash exists in the selected array, an exception is raised
        """
        arr = self._get_hash_list(key, uniq)
        if arr is not None:
            try:
                if len(arr) > 1:
                    raise Exception(f'List in key: {key} and uniq: {uniq} has more than one element: {arr}')
            except Exception as e:
                print(e)
            finally:
                return arr[0]
        else:
            return {}

    def _get_hash_through_reference(self, ref_key, ref_uniq, hash_key, hash_uniq):
        """Obtain a hash when you don't have its unique ID for, but do have the unique ID for another
            hash that references the desired hash. Thus, this is a way of stepping through an intermidiary
            to a hash
        """
        refs = self._get_hash_list(ref_key, ref_uniq)
        if refs is not None:
            for ref in refs:
                if ref_uniq in ref and hash_uniq in ref:
                    return self._get_hash(hash_key, ref[hash_uniq])
            return {}  # This should be unreachable but, just to be safe...
        else:
            return {}

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
