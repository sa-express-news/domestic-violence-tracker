from functools import reduce

from datagenerator import DataGenerator


class TableBuilder():
    def __init__(self, state, year):
        self._data_generator = DataGenerator(state, year)
        self._tables = {}

    def __getattr__(self, attr):
        return getattr(self._data_generator, attr)

    def run_data_generator(self):
        """Just syntactical sugar"""
        return self.run_generator()
    
    def is_classified_as_dv(self, victim):
        circumstances = self._get_hash_arr('nibrs_victim_circumstances', victim['victim_id'])
        if circumstances is not None:
            return (any(circumstance['circumstances_id'] == '6' for circumstance in circumstances))
        else:
            return False

    def is_related_to_offender(self, victim):
        relationships = self._get_hash_arr('nibrs_victim_offender_rel', victim['victim_id'])
        if relationships is not None:
            dv_like_relationships = set([27, 3, 4, 6, 10, 11, 12, 13, 15, 17, 19, 20, 21, 22, 23, 26])
            return any(int(relationship['relationship_id']) in dv_like_relationships for relationship in relationships)
        else:
            return False

    def is_violent_offense(self, incident):
        offenses = self._get_hash_arr('nibrs_offense', incident['incident_id'])
        if offenses is not None:
            violent_offenses = set([1, 3, 4, 27, 32, 36, 38, 43, 51])
            return any(int(offense['offense_type_id']) in violent_offenses for offense in offenses)
        else:
            return False

    def victim_is_person(self, victim):
        return victim['victim_type_id'] == '4' or victim['victim_type_id'] == '5'

    def is_domestic_violence(self, incident):
        victims = self._get_hash_arr('nibrs_victim', incident['incident_id'])
        if victims is not None:
            for victim in victims:
                if (self.victim_is_person(victim) and
                   (self.is_classified_as_dv(victim) or (self.is_related_to_offender(victim) and self.is_violent_offense(incident)))):
                    return True
            return False
        else:
            return False

    def _merge_hashes(self, *argv):
        return reduce(lambda x, y: {**x, **y}, argv, {})

    def _make_int(self, prop):
        try:
            prop = int(prop)
        except:
            print(f'Prop: {prop} is not an interger!')
        finally:
            return prop

    def _get_ref_hash(self, key, uniq):
        arr = self._get_hash_arr(key, uniq)
        if arr is not None:
            return arr[0]
        else:
            return {}

    def _get_agency_fields(self, id):
        agency = self._get_hash_arr('agencies', id)[0]
        return {
            'agency_name': agency.get('ncic_agency_name'),
            'ori': agency.get('ori'),
            'county_name': agency.get('county_name'),
            'state_id': agency.get('state_id'),
            'state_abbr': agency.get('state_abbr'),
            'population': agency.get('population'),
            'population_group_code': agency.get('population_group_code'),
            'population_group_desc': agency.get('population_group_desc'),
            'nibrs_start_date': agency.get('nibrs_start_date'),
        }

    def _get_relationship_fields(self, victim_id):
        victim_offender_rel = self._get_ref_hash('nibrs_victim_offender_rel', victim_id)
        if victim_offender_rel is not None and 'relationship_id' in victim_offender_rel:
            return self._get_ref_hash('nibrs_relationship', victim_offender_rel['relationship_id'])

    def _get_injury_fields(self, victim_id):
        nibrs_victim_injury = self._get_ref_hash('nibrs_victim_injury', victim_id)
        if nibrs_victim_injury is not None and 'injury_id' in nibrs_victim_injury:
            return self._get_ref_hash('nibrs_injury', nibrs_victim_injury['injury_id'])

    def _get_circumstance_fields(self, victim_id):
        nibrs_victim_circumstances = self._get_ref_hash('nibrs_victim_circumstances', victim_id)
        if nibrs_victim_circumstances is not None and 'circumstances_id' in nibrs_victim_circumstances:
            return self._get_ref_hash('nibrs_circumstances', nibrs_victim_circumstances['circumstances_id'])

    def add_incident_row(self, raw):
        if 'incidents' not in self._tables:
            self._tables['incidents'] = []

        try:
            incident = {
                'id': self._make_int(raw.get('incident_id')),
                'cleared_except_id': self._make_int(raw.get('cleared_except_id')),
                'cleared_except_desc': None,
                'agency_id': self._make_int(raw.get('agency_id')),
                'data_year': self._make_int(raw.get('data_year')),
                'submission_date': raw.get('submission_date'),
                'incident_date': raw.get('incident_date'),
            }

            cleared_except = self._get_ref_hash('nibrs_cleared_except', 'cleared_except_id')

            agency_fields = self._get_agency_fields(raw.get('agency_id'))

            self._tables['incidents'].append(
                self._merge_hashes(
                    incident,
                    cleared_except,
                    agency_fields
                )
            )
        except Exception as e:
            print(f'Failed to add row with id: {raw["incident_id"]} to incident table due to: {e}')

    def add_victim_rows(self, incident):
        if 'victims' not in self._tables:
            self._tables['victims'] = []

        try:
            victims = self._get_hash_arr('nibrs_victim', incident['incident_id'])
            if victims is not None:
                for raw in victims:
                    victim = {
                        'id': self._make_int(raw.get('victim_id')),
                        'incident_id': self._make_int(raw.get('incident_id')),
                        'offense_id': self._make_int(raw.get('offense_id')),
                        'age_num': self._make_int(raw.get('age_num')),
                        'sex_code': raw.get('sex_code'),
                        'race_id': self._make_int(raw.get('race_id')),
                        'race_desc': None,
                        'ethnicity_id': self._make_int(raw.get('ethnicity_id')),
                        'ethnicity_desc': None,
                        'victim_seq_num': self._make_int(raw.get('victim_seq_num')),
                        'injury_id': self._make_int(raw.get('injury_id')),
                        'injury_name': None,
                        'relationship_id': self._make_int(raw.get('relationship_id')),
                        'relationship_name': None,
                        'circumstance_id': self._make_int(raw.get('circumstance_id')),
                        'circumstance_name': None,
                    }

                    race = self._get_ref_hash('ref_race', raw.get('race_id'))
                    ethnicity = self._get_ref_hash('nibrs_ethnicity', raw.get('ethnicity_id'))
                    injury = self._get_injury_fields(raw.get('victim_id'))
                    relationship = self._get_relationship_fields(raw.get('victim_id'))
                    circumstance = self._get_circumstance_fields(raw.get('victim_id'))

                    self._tables['victims'].append(
                        self._merge_hashes(
                            victim,
                            race,
                            ethnicity,
                            injury,
                            relationship,
                            circumstance
                        )
                    )
        except Exception as e:
            print(f'Failed to add row with id: {incident["incident_id"]} to victims table due to: {e}')
