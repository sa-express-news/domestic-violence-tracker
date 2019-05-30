import unittest

from tablebuilder import TableBuilder


class TestTableBuilder(unittest.TestCase):
    def test_filter_dv_functions(self):
        table_builder = TableBuilder('SC', 2014)
        for incident in table_builder.run_data_generator():
            if incident['incident_id'] == '74287496':
                expected = True
                result = table_builder.is_classified_as_dv(table_builder._get_hash('nibrs_victim', incident['incident_id'])[0])
                self.assertEqual(expected, result)
            if incident['incident_id'] == '74633158':
                expected = True
                result = table_builder.is_violent_offense(incident)
                self.assertEqual(expected, result)
            if incident['incident_id'] == '73401906':
                expected = False

                result = table_builder.is_violent_offense(incident)
                self.assertEqual(expected, result)

                result = table_builder.is_domestic_violence(incident)
                self.assertEqual(expected, result)
            if incident['incident_id'] == '73389548':
                expected = True

                result = table_builder.is_related_to_offender(table_builder._get_hash('nibrs_victim', incident['incident_id'])[0])
                self.assertEqual(expected, result)

                result = table_builder.is_domestic_violence(incident)
                self.assertEqual(expected, result)
            if incident['incident_id'] == '79818151':
                expected = False
                result = table_builder.is_domestic_violence(incident)
                self.assertEqual(expected, result)

    def test_add_incident_row(self):
        table_builder = TableBuilder('TX', 2009)
        gen = table_builder.run_data_generator()
        incident = next(gen)
        while table_builder.is_domestic_violence(incident) is False:
            incident = next(gen)
        else:
            table_builder.add_incident_row(incident)

            expected = {
                'agency_id': 18798,
                'agency_name': None,
                'cleared_except_desc': '6',
                'cleared_except_id': 6,
                'county_name': None,
                'data_year': None,
                'id': 51580918,
                'incident_date': '2009-01-04 00:00:00',
                'nibrs_start_date': None,
                'ori': 'TX0140700',
                'population': '71780',
                'population_group_code': '3',
                'population_group_desc': 'Cities from 50,000 thru 99,000',
                'state_abbr': 'TX',
                'state_id': '48',
                'submission_date': ''
            }

            result = table_builder._tables['incidents'][0]

            self.assertDictEqual(expected, result)

    def test_add_victim_rows(self):
        table_builder = TableBuilder('CO', 2017)
        gen = table_builder.run_data_generator()
        incident = next(gen)
        while table_builder.is_domestic_violence(incident) is False:
            incident = next(gen)
        else:
            table_builder.add_victim_rows(incident)

            expected = {
                'agency_id': 18798,
            }

            result = table_builder._tables['victims'][0]

            self.maxDiff = None
            self.assertDictEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
