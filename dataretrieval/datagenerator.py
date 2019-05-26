import csv
from collections import OrderedDict

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

    def _get_cols(self, lookup, row):
        """Filtered out only the columns wanted from each csv"""
        return OrderedDict((col, row[col]) for col in lookup['cols'])

    def _add_to_dict(self, name, file):
        """Add a CSV to the dictionary"""
        lookup = filename_map.get_data(name)
        self._dict[lookup['key']] = {}
        for row in csv.DictReader(file):
            try:
                self._dict[lookup['key']][row[lookup['uniq']]] = self._get_cols(lookup, row)
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
            if name == 'TX/NIBRS_incident.csv':  # by design, this is the last element in the list
                for row in csv.DictReader(file):
                    yield row
            elif filename_map.key_exists(name):
                self._add_to_dict(name, file)
        self._dict.clear()

    def is_classified_as_dv(self, victim):
        circumstance = self._get_hash('NIBRS_VICTIM_CIRCUMSTANCES', victim['VICTIM_ID'])
        if circumstance is not None:
            return circumstance['CIRCUMSTANCES_ID'] == '6'
        else:
            return False

    def is_related_to_offender(self, victim):
        relationship = self._get_hash('NIBRS_VICTIM_OFFENDER_REL', victim['VICTIM_ID'])
        if relationship is not None:
            dv_like_relationships = set([27, 3, 4, 6, 10, 11, 12, 13, 15, 17, 19, 20, 21, 22, 23, 26])
            return int(relationship['RELATIONSHIP_ID']) in dv_like_relationships
        else:
            return False

    def is_violent_offense(self, incident):
        offense = self._get_hash('NIBRS_OFFENSE', incident['INCIDENT_ID'])
        if offense is not None:
            violent_offenses = set([1, 3, 4, 27, 32, 36, 38, 43, 51])
            return int(offense['OFFENSE_TYPE_ID']) in violent_offenses
        else:
            return False

    def is_domestic_violence(self, incident):
        victim = self._get_hash('NIBRS_VICTIM', incident['INCIDENT_ID'])
        if victim is not None:
            return self.is_classified_as_dv(victim) or (self.is_related_to_offender(victim) and self.is_violent_offense(incident))
        else:
            return False
