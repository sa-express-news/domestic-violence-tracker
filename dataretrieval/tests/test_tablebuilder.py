import unittest

from tablebuilder import TableBuilder


class TestTableBuilder(unittest.TestCase):
    def test_filter_dv_functions(self):
        table_builder = TableBuilder('SC', 2014)
        for incident in table_builder.run_data_generator():
            if incident['incident_id'] == '74287496':
                expected = True
                result = table_builder.is_classified_as_dv(table_builder._get_hash('nibrs_victim', incident['incident_id']))
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

                result = table_builder.is_related_to_offender(table_builder._get_hash('nibrs_victim', incident['incident_id']))
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
                'cleared_except_desc': None,
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
        table_builder = TableBuilder('CO', 2014)
        gen = table_builder.run_data_generator()
        incident = next(gen)
        while table_builder.is_domestic_violence(incident) is False:
            incident = next(gen)
        else:
            table_builder.add_victim_rows(incident)

            expected = {
                'age_num': 21,
                'circumstance_id': None,
                'circumstance_name': None,
                'ethnicity_id': '3',
                'ethnicity_name': 'Unknown',
                'id': 82582711,
                'incident_id': 75938498,
                'injury_id': '5',
                'injury_name': 'None',
                'race_desc': 'White',
                'race_id': '1',
                'relationship_id': '3',
                'relationship_name': 'Victim Was Boyfriend/Girlfriend',
                'sex_code': 'F',
                'victim_seq_num': 1
            }

            result = table_builder._tables['victims'][0]

            self.assertDictEqual(expected, result)

    def test_add_offender_rows(self):
        table_builder = TableBuilder('TX', 2000)
        gen = table_builder.run_data_generator()
        incident = next(gen)
        while table_builder.is_domestic_violence(incident) is False:
            incident = next(gen)
        else:
            table_builder.add_offender_rows(incident)

            expected = {
                'age_num': 48,
                'ethnicity_id': '',
                'ethnicity_name': None,
                'id': 14200760,
                'incident_id': 12604845,
                'offender_seq_num': 1,
                'race_desc': 'White',
                'race_id': '1',
                'sex_code': 'M'
            }

            result = table_builder._tables['offenders'][0]

            self.assertDictEqual(expected, result)

    def test_add_offense_rows(self):
        table_builder = TableBuilder('TX', 2017)
        gen = table_builder.run_data_generator()
        incident = next(gen)
        while table_builder.is_domestic_violence(incident) is False:
            incident = next(gen)
        else:
            table_builder.add_offense_rows(incident)

            expected = {
                'id': 114121911,
                'incident_id': 91852187,
                'location_id': '20',
                'location_name': 'Residence/Home',
                'offense_name': 'Simple Assault',
                'offense_type_id': '51',
                'suspect_using_id': '4',
                'suspect_using_name': 'Not Applicable',
                'weapon_id': '12',
                'weapon_name': 'Personal Weapons'
            }

            result = table_builder._tables['offenses'][0]

            self.assertDictEqual(expected, result)

    def test_add_arrestee_rows(self):
        table_builder = TableBuilder('VT', 2006)
        gen = table_builder.run_data_generator()
        incident = next(gen)
        while table_builder.is_domestic_violence(incident) is False:
            incident = next(gen)
        else:
            table_builder.add_arrestee_rows(incident)

            expected = {
                'age_num': 44,
                'arrest_date': '2006-03-30 00:00:00',
                'arrestee_seq_num': 1,
                'ethnicity_id': '2',
                'ethnicity_name': 'Not Hispanic or Latino',
                'id': 9553880,
                'incident_id': 36212421,
                'multiple_indicator': 'N',
                'offender_seq_num': None,
                'offense_name': 'Aggravated Assault',
                'offense_type_id': '27',
                'race_desc': 'White',
                'race_id': '1',
                'sex_code': 'M'
            }

            result = table_builder._tables['arrestees'][0]

            self.assertDictEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
