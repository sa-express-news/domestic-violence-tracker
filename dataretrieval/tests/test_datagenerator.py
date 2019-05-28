import unittest
import csv
from io import TextIOWrapper

import filename_map
from datagenerator import DataGenerator


class TestDataGenerator(unittest.TestCase):
    def test__get_cols(self):
        lookup = filename_map.get_data('nibrs_arrest_type.csv')
        row = {
            'merp': 'herro',
            'arrest_type_id': 47,
            'mop': 788888,
            'arrest_type_name': 'bad one',
        }

        data_generator = DataGenerator('KY', 2016)

        expected = {
            'arrest_type_id': 47,
            'arrest_type_name': 'bad one',
        }
        result = data_generator._filter_cols(lookup, row)

        self.assertDictEqual(expected, result)

    def test__map_filter_agency_cols(self):
        lookup = filename_map.get_data('cde_agencies.csv')
        row = {
            'merp': 'herro',
            'ori': 47,
            'mop': 788888,
            'primary_county': 'Mexicaliand',
        }

        data_generator = DataGenerator('TX', 2015)

        expected = {
            'ori': 47,
            'county_name': 'Mexicaliand',
        }
        result = data_generator._map_filter_agency_cols(lookup, row)

        self.assertDictEqual(expected, result)

    def test__add_to_dict(self):
        data_generator = DataGenerator('TX', 2013)
        for name, file in data_generator.extract_zip():
            if 'nibrs_victim.csv' in name.lower():
                lookup = filename_map.get_data(name)
                data_generator._add_to_dict(lookup, file)

        expected = 189139
        result = len(data_generator._dict['nibrs_victim'])
        self.assertEqual(expected, result)

        expected = ['age_id', 'incident_id', 'age_num', 'sex_code', 'race_id', 'ethnicity_id', 'victim_id', 'victim_type_id', 'victim_seq_num']
        result = list(data_generator._dict['nibrs_victim']['68950600'][0].keys())
        self.assertCountEqual(expected, result)

    def test_filter_dv_functions(self):
        data_generator = DataGenerator('SC', 2014)
        for incident in data_generator.run_generator():
            if incident['incident_id'] == '74287496':
                expected = True
                result = data_generator.is_classified_as_dv(data_generator._get_hash('nibrs_victim', incident['incident_id'])[0])
                self.assertEqual(expected, result)
            if incident['incident_id'] == '74633158':
                expected = True
                result = data_generator.is_violent_offense(incident)
                self.assertEqual(expected, result)
            if incident['incident_id'] == '73401906':
                expected = False

                result = data_generator.is_violent_offense(incident)
                self.assertEqual(expected, result)

                result = data_generator.is_domestic_violence(incident)
                self.assertEqual(expected, result)
            if incident['incident_id'] == '73389548':
                expected = True
                
                result = data_generator.is_related_to_offender(data_generator._get_hash('nibrs_victim', incident['incident_id'])[0])
                self.assertEqual(expected, result)

                result = data_generator.is_domestic_violence(incident)
                self.assertEqual(expected, result)
            if incident['incident_id'] == '79818151':
                expected = False
                result = data_generator.is_domestic_violence(incident)
                self.assertEqual(expected, result)
                

if __name__ == '__main__':
    unittest.main()
