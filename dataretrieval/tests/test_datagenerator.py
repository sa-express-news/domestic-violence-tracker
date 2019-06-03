import unittest

import filename_map
from datagenerator import DataGenerator


class TestDataGenerator(unittest.TestCase):
    def test__get_cols(self):
        lookup = filename_map.get_data('nibrs_location_type.csv')
        row = {
            'merp': 'herro',
            'location_id': 47,
            'mop': 788888,
            'location_name': 'bad one',
        }

        data_generator = DataGenerator('KY', 2016)

        expected = {
            'location_id': 47,
            'location_name': 'bad one',
        }
        result = data_generator._filter_cols(lookup, row)

        self.assertDictEqual(expected, result)

    def test__map_filter_cols(self):
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
        result = data_generator._map_filter_cols(lookup, row)

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

        expected = ['incident_id', 'age_num', 'sex_code', 'race_id', 'ethnicity_id', 'victim_id', 'victim_type_id', 'victim_seq_num']
        result = list(data_generator._dict['nibrs_victim']['68950600'][0].keys())
        self.assertCountEqual(expected, result)

    def test__add_to_dict_with__map_filter_cols(self):
        data_generator = DataGenerator('TX', 2000)
        for name, file in data_generator.extract_zip():
            if 'cde_agencies.csv' in name.lower():
                lookup = filename_map.get_data(name)
                data_generator._add_to_dict(lookup, file)

        self.maxDiff = None

        expected = ['agency_id', 'ori', 'ncic_agency_name', 'state_id', 'state_abbr', 'population', 'population_group_code', 'population_group_desc', 'nibrs_start_date', 'county_name']
        result = list(data_generator._dict['agencies']['19089'][0].keys())
        self.assertCountEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
