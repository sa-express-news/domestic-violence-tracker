from io import TextIOWrapper
import csv

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

    def _map_filter_agency_cols(self, lookup, row):
        """Since agency files differ between years, we need to map to matching values and filter.
            This is achieved by adding a 'map_cols_to' property to files produced before 2016
            and mapping their column names to the names on the newer files
        """
        hash = dict()
        for idx, col in enumerate(lookup['cols']):
            if col in row:
                key = filename_map.map_col_name(lookup, idx)
                hash[key] = row[col]
        return hash

    def _add_to_dict(self, lookup, file):
        """Add a CSV to the dictionary"""
        self._dict[lookup['key']] = {}
        filter = self._map_filter_agency_cols if 'map_cols_to' in lookup else self._filter_cols
        for row in csv.DictReader(TextIOWrapper(file, encoding="utf-8")):
            try:
                uniqID = row[lookup['uniq']]
                rowHash = filter(lookup, row)
                if uniqID in self._dict[lookup['key']]:
                    self._dict[lookup['key']][uniqID].append(rowHash)
                else:
                    self._dict[lookup['key']][uniqID] = [rowHash]
            except:
                print('error with %s' % (name))

    def _get_hash(self, key, uniq):
        hash = None
        try:
            hash = self._dict[key][uniq]
        finally:
            return hash

    def run_generator(self):
        """This is the main method, it yields the incidents and places the related data in hashes"""
        for name, file in self.extract_zip():
            if 'nibrs_incident.csv' in name.lower():  # by design, this is the last element in the list
                for row in csv.DictReader(TextIOWrapper(file, encoding="utf-8")):
                    yield row
            elif filename_map.key_exists(name):
                lookup = filename_map.get_data(name)
                self._add_to_dict(lookup, file)  # this is expensive, but I think the time saved by building a reference hash is worth it overall
        self._dict.clear()

    def is_classified_as_dv(self, victim):
        circumstances = self._get_hash('nibrs_victim_circumstances', victim['victim_id'])
        if circumstances is not None:
            return (any(circumstance['circumstances_id'] == '6' for circumstance in circumstances))
        else:
            return False

    def is_related_to_offender(self, victim):
        relationships = self._get_hash('nibrs_victim_offender_rel', victim['victim_id'])
        if relationships is not None:
            dv_like_relationships = set([27, 3, 4, 6, 10, 11, 12, 13, 15, 17, 19, 20, 21, 22, 23, 26])
            return any(int(relationship['relationship_id']) in dv_like_relationships for relationship in relationships)
        else:
            return False

    def is_violent_offense(self, incident):
        offenses = self._get_hash('nibrs_offense', incident['incident_id'])
        if offenses is not None:
            violent_offenses = set([1, 3, 4, 27, 32, 36, 38, 43, 51])
            return any(int(offense['offense_type_id']) in violent_offenses for offense in offenses)
        else:
            return False

    def is_domestic_violence(self, incident):
        victims = self._get_hash('nibrs_victim', incident['incident_id'])
        if victims is not None:
            for victim in victims:
                if self.is_classified_as_dv(victim) or (self.is_related_to_offender(victim) and self.is_violent_offense(incident)):
                    return True
            return False
        else:
            return False
